# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

import threading
import six

from . import zmq
from . import TimeoutError, UserInterrupt, GetMonotonicTime

import logging
log = logging.getLogger(__name__)


class ZmqSocketPool(object):

    _url = None  # url that sockets should connect to
    _ctx = None  # the context to use
    _ctxown = None  # the context owned exclusively
    _timeout = None  # timeout waiting for either send on receive while a socket is in the polling state
    _limit = None  # limit on number of socket alive at any time, None means unlimited

    _isok = False  # whether it is time to terminate
    _poller = None  # znq poller that tracks sockets in self._pollingsockets
    _sockets = None  # all sockets alive, a dictionary mapping from socket to True
    _pollingsockets = None  # sockets that are in the polling state, waiting for send or receive, a dictionary mapping from socket to timestamp when added to the poller
    _availablesockets = None  # list of sockets that are ready for use immediately

    _acquirecount = 0  # number of times a socket is acuired
    _releasecount = 0  # number of times a socket is released
    _opencount = 0  # number of times we opened a new socket
    _closecount = 0  # number of times we closed a socket

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

        # log.debug('sockets: opened = %d, closed = %d, acquired = %d, released = %d', self._opencount, self._closecount, self._acquirecount, self._releasecount)

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
            raise UserInterrupt(u'Interrupted while opening new socket, ZMQ socket pool is stopping')

        socket = self._ctx.socket(zmq.REQ)
        socket.setsockopt(zmq.TCP_KEEPALIVE, 1) # turn on tcp keepalive, do these configuration before connect
        socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 2) # the interval between the last data packet sent (simple ACKs are not considered data) and the first keepalive probe; after the connection is marked to need keepalive, this counter is not used any further
        socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 2) # the interval between subsequential keepalive probes, regardless of what the connection has exchanged in the meantime
        socket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 2) # the number of unacknowledged probes to send before considering the connection dead and notifying the application layer
        socket.connect(self._url)
        assert(socket not in self._sockets)
        self._sockets[socket] = True
        self._opencount += 1

        # log.debug('opened a socket, url = %s opened = %d, closed = %d', self._url, self._opencount, self._closecount)
        return socket

    def _CloseSocket(self, socket):
        assert(socket in self._sockets)
        self._closecount += 1
        del self._sockets[socket]
        try:
            # make sure we do not linger when closing socket
            socket.close(linger=0)
        except Exception as e:
            log.exception('caught exception when closing socket: %s', e)

    def _StartPollingSocket(self, socket):
        assert(socket not in self._pollingsockets)
        self._pollingsockets[socket] = GetMonotonicTime()
        self._poller.register(socket, zmq.POLLIN | zmq.POLLOUT)

    def _StopPollingSocket(self, socket):
        assert(socket in self._pollingsockets)
        self._poller.unregister(socket)
        del self._pollingsockets[socket]

    def _Poll(self, timeout=0):
        """spin once and does internal polling of sockets
        """
        now = GetMonotonicTime()

        # poll for receives, non blocking if timeout is 0
        for socket, event in self._poller.poll(timeout):
            if (event & zmq.POLLIN) == zmq.POLLIN:
                # log.debug('a socket is ready for receive, url = %s, polling = %d, availble = %d', self._url, len(self._pollingsockets), len(self._availablesockets))

                # at least one message can be received without blocking
                try:
                    socket.recv(zmq.NOBLOCK)
                except Exception as e:
                    # when error occur, throw the socket away
                    log.exception('caught exception when recv: %s', e)
                    self._StopPollingSocket(socket)
                    self._CloseSocket(socket)
                    continue

                # reset the timestamp since we just called recv
                self._pollingsockets[socket] = now

        # poll again for send, non blocking if timeout is 0, some previously in recv state socket may now be available for sending
        for socket, event in self._poller.poll(timeout):
            if (event & zmq.POLLOUT) == zmq.POLLOUT:
                # log.debug('a socket is ready for send, url = %s, polling = %d, availble = %d', self._url, len(self._pollingsockets), len(self._availablesockets))

                # at least one message can be sent to socket without blocking
                self._StopPollingSocket(socket)
                self._availablesockets.append(socket)

        # check for socket that stayed in the polling state for too long
        timedoutsockets = []
        for socket, timestamp in six.iteritems(self._pollingsockets):
            if now - timestamp > self._timeout:
                timedoutsockets.append(socket)

        # close timed out sockets
        while len(timedoutsockets) > 0:
            socket = timedoutsockets.pop()
            self._StopPollingSocket(socket)
            self._CloseSocket(socket)

    def AcquireSocket(self, timeout=None, checkpreemptfn=None):
        """acquire a socket from the list of availble sockets for sending
        """
        # first we try a non blocking poll
        self._Poll(timeout=0)

        starttime = GetMonotonicTime()
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
            elapsedtime = GetMonotonicTime() - starttime
            if timeout is not None and elapsedtime > timeout:
                raise TimeoutError(u'Timed out waiting for a socket to %s to become available after %f seconds' % (self._url, elapsedtime))

            if checkpreemptfn is not None:
                checkpreemptfn()

            # otherwise, wait by a small blocking poll
            self._Poll(timeout=50)

        raise UserInterrupt(u'Interrupted while acquiring socket, ZMQ socket pool is stopping')

    def ReleaseSocket(self, socket, reuse=True):
        """release a socket after use, if caller did not call recv, the pool will take care of that
        """
        if socket is not None:
            self._releasecount += 1
            if self._isok and reuse:
                self._StartPollingSocket(socket)
            else:
                self._CloseSocket(socket)


class ZmqClient(object):

    _hostname = None
    _port = None
    _url = None
    _pool = None
    _socket = None
    _isok = False
    _callerthread = None  # last caller thread
    _callercontext = None # the context of the last caller

    def __init__(self, hostname='', port=0, ctx=None, limit=100, url=None, checkpreemptfn=None, reusetimeout=10.0):
        """creates a new zmq client, uses zmq req socket over tcp

        :param hostname: hostname or ip to connect to
        :param port: port to connect to
        :param ctx: optionally specifies a zmq context to use, if not provided, a new zmq context will be created
        :param limit: defaults to 100, limit the number of underlying zmq socket to create, usually one socket will actually be used, but if server times out frequently and you use fireandforget, then this limit caps the number of sockets we can use
        :param url: allow passing of zmq socket url instead of hostname and port
        """

        self._hostname = hostname
        self._port = int(port)
        self._url = url
        if self._url is None:
            self._url = 'tcp://%s:%d' % (self._hostname, self._port)

        self._pool = ZmqSocketPool(self._url, ctx=ctx, limit=limit, timeout=reusetimeout)
        self._socket = None
        self._isok = True
        self._checkpreemptfn = checkpreemptfn

    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self.SetDestroy()

        if self._pool is not None:
            self._ReleaseSocket()
            self._pool.Destroy()
            self._pool = None

    def SetDestroy(self):
        self._isok = False
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

    # TODO: this is for backward compatibility, remove once all callers are updated
    @property
    def hostname(self):
        return self._hostname

    # TODO: this is for backward compatibility, remove once all callers are updated
    @property
    def port(self):
        return self._port
    
    def _CheckCallerThread(self, context=None):
        """catch bad caller who use zmq client from multiple threads and causes random race conditions.
        """
        callerthread = repr(threading.current_thread())
        oldcallerthread = self._callerthread
        oldcallercontext = self._callercontext
        self._callerthread = callerthread
        self._callercontext = context
        if oldcallerthread is not None:
            # assert oldcallerthread == callerthread, 'zmqclient used from multiple threads: previously = %s, now = %s' % (oldcallerthread, callerthread)
            if oldcallerthread != callerthread:
                log.error('zmqclient used from multiple threads, this is a bug in the caller: previously = %s, now = %s, previous context = %s, new context = %s', oldcallerthread, callerthread, repr(oldcallercontext)[:100], repr(context)[:100])
    
    def _AcquireSocket(self, timeout=None, checkpreempt=True):
        # if we were holding on to a socket before, release it before acquiring one
        self._ReleaseSocket()
        self._socket = self._pool.AcquireSocket(timeout=timeout, checkpreemptfn=self._checkpreemptfn if checkpreempt else None)

    def _ReleaseSocket(self):
        if self._socket is not None:
            self._pool.ReleaseSocket(self._socket)
            self._socket = None
    
    def SetPreemptFn(self, checkpreemptfn):
        self._checkpreemptfn = checkpreemptfn
    
    def SendCommand(self, command, timeout=10.0, blockwait=True, fireandforget=False, sendjson=True, recvjson=True, checkpreempt=None):
        """sends command via established zmq socket

        :param command: command in json format
        :param timeout: if None, block. If >= 0, use as timeout
        :param blockwait: if True (default), will call receive also, otherwise, caller needs to call ReceiveCommand later
        :param fireandforget: if True, will send command and immediately return without trying to receive, blockwait will be set to False
        :param sendjson: if True (default), will send data as json
        :param recvjson: if True (default), will parse received data as json

        :return: returns the response from the zmq server in json format if blockwait is True
        """
        # log.debug('Sending command via ZMQ: %s', command)
        if checkpreempt is None:
            log.warn(u'Need to specify checkpreempt to zmq client for command %r', command)
        
        self._CheckCallerThread(command)

        if fireandforget:
            blockwait = False

        # acquire a socket for sending
        self._AcquireSocket(timeout=timeout, checkpreempt=checkpreempt)

        # we may be exiting, the pool refused to give us a socket
        if not self._isok:
            raise UserInterrupt(u'Interrupted after acquiring socket, ZMQ client is stopping')

        releasesocket = True
        try:
            # send phase
            starttime = GetMonotonicTime()
            while self._isok:
                # timeout checking
                elapsedtime = GetMonotonicTime() - starttime
                if timeout is not None and elapsedtime > timeout:
                    raise TimeoutError(u'Timed out trying to send to %s after %f seconds' % (self._url, elapsedtime))

                if checkpreempt and self._checkpreemptfn is not None:
                    self._checkpreemptfn()

                # poll to see if we can send, if not, loop
                waitingevents = self._socket.poll(50, zmq.POLLOUT)
                if (waitingevents & zmq.POLLOUT) != zmq.POLLOUT:
                    continue

                if sendjson:
                    self._socket.send_json(command, zmq.NOBLOCK)
                else:
                    self._socket.send(command, zmq.NOBLOCK)

                # break when successfully sent
                break

            # for fire and forget, no need to receive
            if fireandforget:
                return None

            # keep the socket and let caller call receive
            if not blockwait:
                releasesocket = False
                return None

            # receive
            return self.ReceiveCommand(timeout=timeout, recvjson=recvjson, checkpreempt=checkpreempt)

        finally:
            # release socket
            if releasesocket:
                self._ReleaseSocket()

        raise UserInterrupt(u'Interrupted while waiting to send, ZMQ client is stopping')

    def IsWaitingReply(self):
        return self._socket is not None

    def ReceiveCommand(self, timeout=10.0, recvjson=True, checkpreempt=True):
        """receive response to a previous SendCommand call, SendCommand must be called with blockwait=False and fireandforget=False

        :param timeout: if None, block. If >= 0, use as timeout
        :param recvjson: if True (default), will parse received data as json

        :return: returns the recv or recv_json response
        """
        self._CheckCallerThread('ReceiveCommand')
        
        # should have called SendCommand with blockwait=False first
        assert(self._socket is not None)
        
        try:
            # receive phase
            starttime = GetMonotonicTime()
            pollms = 1 if timeout else 0 # if timeout is 0, then return immediately. 1ms poll time for faster response
            while self._isok:
                # poll to see if something has been received, if received nothing, loop
                startpolltime = GetMonotonicTime()
                waitingevents = self._socket.poll(pollms, zmq.POLLIN)
                endpolltime = GetMonotonicTime()
                if endpolltime - startpolltime > 0.2:  # due to python delays sometimes this can be 0.11s
                    log.critical('polling time took %fs!', endpolltime - startpolltime)
                if (waitingevents & zmq.POLLIN) != zmq.POLLIN:
                    continue
                
                if recvjson:
                    return self._socket.recv_json(zmq.NOBLOCK)
                else:
                    return self._socket.recv(zmq.NOBLOCK)
                
                # do timeout checking at the end
                elapsedtime = GetMonotonicTime() - starttime
                if timeout is not None and elapsedtime > timeout:
                    raise TimeoutError(u'Timed out to get response from %s after %f seconds (timeout=%f)' % (self._url, elapsedtime, timeout))
                
                if checkpreempt and self._checkpreemptfn is not None:
                    self._checkpreemptfn()
        
        finally:
            # release socket
            self._ReleaseSocket()

        raise UserInterrupt(u'Interrupted while waiting for response, ZMQ client is stopping')
