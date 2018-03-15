# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

# logging
import time
import zmq
import weakref

from . import TimeoutError, UserInterrupt

import logging
log = logging.getLogger(__name__)

class ZmqSocketPool(object):

    _url = None # url that sockets should connect to
    _ctx = None # the context to use
    _ctxown = None # the context owned exclusively
    _timeout = None # timeout waiting for either send on receive while a socket is in the polling state
    _limit = None # limit on number of socket alive at any time, None means unlimited

    _isok = False # whether it is time to terminate
    _poller = None # znq poller that tracks sockets in self._pollingsockets
    _sockets = None # all sockets alive, a dictionary mapping from socket to True
    _pollingsockets = None # sockets that are in the polling state, waiting for send or receive, a dictionary mapping from socket to timestamp when added to the poller
    _availablesockets = None # list of sockets that are ready for use immediately

    _acquirecount = 0 # number of times a socket is acuired
    _releasecount = 0 # number of times a socket is released
    _opencount = 0 # number of times we opened a new socket
    _closecount = 0 # number of times we closed a socket

    def __init__(self, url, ctx=None, timeout=10.0, limit=None):
        """creates a socket pool, the pool can lease out socket for send and recv.
        if caller only does send but not recv, the socket will not be reused until internally the pool recv data and discard them.

        :param url: url for sockets to connect to
        :param ctx: optionally force socket to use provided zmq context instead of creating a new zmq context
        :param timeout: defaults to 10 seconds, specifies how long should we be polling the socket, until we consider it to be dead, note this is not a blocking timeout.
        :param limit: limit on number of socket alive at any time, None means unlimited
        """
        self._url = url
        self._ctx = ctx
        if self._ctx is None:
            self._ctxown = zmq.Context()
            self._ctx = self._ctxown
        self._timeout = timeout
        self._limit = limit

        self._isok = True
        self._poller = zmq.Poller()
        self._sockets = {}
        self._pollingsockets = {}
        self._availablesockets = []

        self._acquirecount = 0
        self._releasecount = 0
        self._opencount = 0
        self._closecount = 0

    def __del__(self):
        self.Destroy()
        
    def Destroy(self):
        self.SetDestroy()

        # at this point, all sockets should have been released
        assert(self._acquirecount == self._releasecount)
        sockets = list(self._pollingsockets.keys())
        while len(sockets) > 0:
            self._StopPollingSocket(sockets.pop())

        # close all socket ever created
        sockets = list(self._sockets.keys())
        while len(sockets) > 0:
            self._CloseSocket(sockets.pop())
        assert(self._opencount == self._closecount)

        log.verbose('sockets: opened = %d, closed = %d, acquired = %d, released = %d', self._opencount, self._closecount, self._acquirecount, self._releasecount)
        
        if self._ctxown is not None:
            try:
                self._ctxown.destroy()
            except Exception:
                log.exception('caught exception when destroying context')
            self._ctxown = None
        self._ctx = None

    def SetDestroy(self):
        # make sure no new socket can be created
        self._isok = False

        # make sure no one can acquire a socket now
        self._availablesockets = []

    def _OpenSocket(self):
        if not self._isok:
            raise UserInterrupt(u'Cannot open socket to %s, pool is going away' % (self._url,))

        socket = self._ctx.socket(zmq.REQ)
        socket.connect(self._url)
        assert(socket not in self._sockets)
        self._sockets[socket] = True
        self._opencount += 1

        log.verbose('opened a socket, url = %s opened = %d, closed = %d', self._url, self._opencount, self._closecount)
        return socket

    def _CloseSocket(self, socket):
        assert(socket in self._sockets)
        self._closecount += 1
        del self._sockets[socket]
        try:
            # make sure we do not linger when closing socket
            socket.close(linger=0)
        except:
            log.exception('caught exception when closing socket')

    def _StartPollingSocket(self, socket):
        assert(socket not in self._pollingsockets)
        self._pollingsockets[socket] = time.time()
        self._poller.register(socket, zmq.POLLIN|zmq.POLLOUT)

    def _StopPollingSocket(self, socket):
        assert(socket in self._pollingsockets)
        self._poller.unregister(socket)
        del self._pollingsockets[socket]            

    def _Poll(self, timeout=0):
        """spin once and does internal polling of sockets
        """
        now = time.time()

        # poll for receives, non blocking if timeout is 0
        for socket, event in self._poller.poll(timeout):
            if (event & zmq.POLLIN) == zmq.POLLIN:
                log.verbose('a socket is ready for receive, url = %s, polling = %d, availble = %d', self._url, len(self._pollingsockets), len(self._availablesockets))

                # at least one message can be received without blocking
                try:
                    socket.recv(zmq.NOBLOCK)
                except:
                    # when error occur, throw the socket away
                    log.exception('caught exception when recv')
                    self._StopPollingSocket(socket)
                    self._CloseSocket(socket)
                    continue

                # reset the timestamp since we just called recv
                self._pollingsockets[socket] = now

        # poll again for send, non blocking if timeout is 0, some previously in recv state socket may now be available for sending
        for socket, event in self._poller.poll(timeout):
            if (event & zmq.POLLOUT) == zmq.POLLOUT:
                log.verbose('a socket is ready for send, url = %s, polling = %d, availble = %d', self._url, len(self._pollingsockets), len(self._availablesockets))

                # at least one message can be sent to socket without blocking
                self._StopPollingSocket(socket)
                self._availablesockets.append(socket)

        # check for socket that stayed in the polling state for too long
        timedoutsockets = []
        for socket, timestamp in self._pollingsockets.iteritems():
            if now - timestamp > self._timeout:
                timedoutsockets.append(socket)

        # close timed out sockets
        while len(timedoutsockets) > 0:
            socket = timedoutsockets.pop()
            self._StopPollingSocket(socket)
            self._CloseSocket(socket)

    def AcquireSocket(self, timeout=None):
        """acquire a socket from the list of availble sockets for sending
        """
        # first we try a non blocking poll
        self._Poll(timeout=0)

        starttime = time.time()
        while self._isok:

            # if a socket is available, use it
            if len(self._availablesockets) > 0:
                socket = self._availablesockets.pop()
                self._acquirecount += 1
                return socket

            # if we don't have available socket but we have quota to create new socket, create a new one
            if self._limit is None or len(self._availablesockets) + len(self._pollingsockets) < self._limit:
                socket = self._OpenSocket()
                self._acquirecount += 1
                return socket

            # check for timeout
            elapsedtime = time.time() - starttime
            if timeout is not None and elapsedtime > timeout:
                raise TimeoutError(u'Timed out waiting for a socket to %s to become available after %f seconds' % (self._url, elapsedtime))

            # otherwise, wait by a small blocking poll
            self._Poll(timeout=50)

        raise UserInterrupt(u'Interrupted when waiting for a socket to %s to become available, pool is going away' % (self._url,))

    def ReleaseSocket(self, socket, reuse=True):
        """release a socket after use, if caller did not call recv, the pool will take care of that
        """
        if socket is not None:
            self._releasecount += 1
            if self._isok and reuse:
                self._StartPollingSocket(socket)
            else:
                self._CloseSocket(socket)

class ZmqClientHandle(object):

    _isok = False
    _client = None # weakref to ZmqClient
    _socket = None # raw zmq socket to be returned back to the pool

    def __init__(self, client, socket):
        self._client = client
        self._socket = socket
        self._isok = True

    def __del__(self):
        self.Destroy()

    def SetDestroy(self):
        self._isok = False

    def Destroy(self):
        self.SetDestroy()

        if self._client is not None:
            self._client.CloseHandle(self)
            self._client = None
        if self._socket is not None:
            log.warn('a leftover socket was not returned to the pool, closing immediately: %r', self._socket)
            self._socket.close(linger=0)
            self._socket = None

    def Close(self):
        self.Destroy()
    
    def SendCommand(self, command, timeout=10.0, sendjson=True):
        """sends command via established zmq socket

        :param command: command in json format
        :param timeout: if None, block. If >= 0, use as timeout
        :param sendjson: if True (default), will send data as json
        """

        # send phase
        starttime = time.time()
        while self._isok:
            # timeout checking
            elapsedtime = time.time() - starttime
            if timeout is not None and elapsedtime > timeout:
                raise TimeoutError(u'Timed out trying to send to %s after %f seconds' % (self._client.GetURL(), elapsedtime))
            
            # poll to see if we can send, if not, loop
            if self._socket.poll(50, zmq.POLLOUT) == 0:
                continue

            if sendjson:
                self._socket.send_json(command, zmq.NOBLOCK)
            else:
                self._socket.send(command, zmq.NOBLOCK)

            # break when successfully sent
            return

        raise UserInterrupt(u'Interrupted during send to %s' % (self._client.GetURL(),))

    def ReceiveResponse(self, timeout=10.0, recvjson=True):
        """receive response to a previous SendCommand call, SendCommand must be called with blockwait=False and fireandforget=False

        :param timeout: if None, block. If >= 0, use as timeout
        :param recvjson: if True (default), will parse received data as json

        :return: returns the recv or recv_json response
        """

        # receive phase
        starttime = time.time()
        while self._isok:
            # timeout checking
            elapsedtime = time.time() - starttime
            if timeout is not None and elapsedtime > timeout:
                raise TimeoutError(u'Timed out to get response from %s after %f seconds (timeout=%f)' % (self._client.GetURL(), elapsedtime, timeout))
            
            # poll to see if something has been received, if received nothing, loop
            startpolltime = time.time()
            waitingevents = self._socket.poll(50, zmq.POLLIN)
            endpolltime = time.time()
            if endpolltime - startpolltime > 0.2: # due to python delays sometimes this can be 0.11s
                log.critical('polling time took %fs!', endpolltime - startpolltime)
            if waitingevents == 0:
                continue
            
            if recvjson:
                return self._socket.recv_json(zmq.NOBLOCK)
            else:
                return self._socket.recv(zmq.NOBLOCK)

        raise UserInterrupt(u'Interrupted during receive to %s' % (self._client.GetURL(),))

class ZmqClient(object):

    _hostname = None
    _port = None
    _url = None
    _pool = None
    _handles = None # (list of weakref.proxy)
    _isok = False
    
    def __init__(self, hostname, port, ctx=None, limit=100):
        """creates a new zmq client, uses zmq req socket over tcp

        :param hostname: hostname or ip to connect to
        :param port: port to connect to
        :param ctx: optionally specifies a zmq context to use, if not provided, a new zmq context will be created
        :param limit: defaults to 100, limit the number of underlying zmq socket to create, usually one socket will actually be used, but if server times out frequently and you use fireandforget, then this limit caps the number of sockets we can use
        """

        self._hostname = hostname
        self._port = int(port)
        self._url = 'tcp://%s:%d' % (self._hostname, self._port)

        self._pool = ZmqSocketPool(self._url, ctx=ctx, limit=limit)
        self._handles = []
        self._isok = True
    
    def __del__(self):
        self.Destroy()
    
    def Destroy(self):
        self.SetDestroy()

        for handle in (self._handles or []):
            if handle is not None:
                handle.Destroy()
        self._handles = None
        if self._pool is not None:
            self._pool.Destroy()
            self._pool = None

    def SetDestroy(self):
        self._isok = False
        for handle in (self._handles or []):
            if handle is not None:
                handle.SetDestroy()
        if self._pool is not None:
            self._pool.SetDestroy()

    def GetHostname(self):
        """returns the hostname given when constructing the client
        """
        return self._hostname

    def GetPort(self):
        """returns the port given when constructing the client
        """
        return self._port

    def GetURL(self):
        """returns the url socket is connected to
        """
        return self._url

    # TODO: this is for backward compatibility, remove once all callers are updated
    @property
    def hostname(self):
        return self._hostname

    # TODO: this is for backward compatibility, remove once all callers are updated
    @property
    def port(self):
        return self._port

    def SendCommand(self, command, timeout=10.0, blockwait=True, fireandforget=False, sendjson=True, recvjson=True):
        """sends command via established zmq socket

        :param command: command in json format
        :param timeout: if None, block. If >= 0, use as timeout
        :param blockwait: if True (default), will call receive also, otherwise, caller needs to call ReceiveResponse later on the returned handle
        :param fireandforget: if True, will send command and immediately return without trying to receive, blockwait will be set to False
        :param sendjson: if True (default), will send data as json
        :param recvjson: if True (default), will parse received data as json
        
        :return: returns the response from the zmq server in json format if blockwait is True
        """

        handle = self.OpenHandle(timeout=timeout)

        handle.SendCommand(command, timeout=timeout, sendjson=sendjson)

        if fireandforget:
            return
        if not blockwait:
            return handle

        return handle.ReceiveResponse(timeout=timeout, recvjson=recvjson)

    def OpenHandle(self, timeout=10.0):
        """acquire a handle to communicate

        :param timeout: if None, block. If >= 0, use as timeout
        """
        socket = self._pool.AcquireSocket(timeout=timeout)
        handle = ZmqClientHandle(weakref.proxy(self), socket)
        self._handles.append(weakref.proxy(handle))
        return handle

    def CloseHandle(self, handle):
        """closes a handle, returns its socket to the pool
        """
        if handle not in self._handles:
            return
        if handle._socket is not None:
            self._pool.ReleaseSocket(handle._socket)
        handle._isok = False
        handle._client = None
        handle._socket = None
        self._handles.remove(handle)
        
        

