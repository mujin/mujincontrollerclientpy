# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

# logging
import time
import zmq

from . import TimeoutError

import logging
log = logging.getLogger(__name__)


class ZmqClient(object):

    class ZmqSocketPool(object):

        class UseScope(object):
            """To be used by with statement to automatically acquire and release socket.
            """
            _pool = None
            _socket = None

            def __init__(self, pool):
                self._pool = pool
                self._socket = None

            def __enter__(self):
                socket = self._pool.AcquireSocket()
                self._socket = socket
                return socket

            def __exit__(self, type, value, traceback):
                reuse = True
                # when exception is thrown using this socket, it should not go back to the pool
                if value is not None:
                    reuse = False
                self._pool.ReleaseSocket(self._socket, reuse=reuse)

        _url = None # url that sockets should connect to
        _ctx = None # the context to use
        _ctxown = None # the context owned exclusively
        _timeout = None # timeout waiting for either send on receive while a socket is in the polling state

        _isok = False # whether it is time to terminate
        _poller = None # znq poller that tracks sockets in self._pollingsockets
        _sockets = None # all sockets alive, a dictionary mapping from socket to True
        _pollingsockets = None # sockets that are in the polling state, waiting for send or receive, a dictionary mapping from socket to timestamp when added to the poller
        _availablesockets = None # list of sockets that are ready for use immediately

        _acquirecount = 0 # number of times a socket is acuired
        _releasecount = 0 # number of times a socket is released
        _opencount = 0 # number of times we opened a new socket
        _closecount = 0 # number of times we closed a socket

        def __init__(self, url, ctx=None, timeout=10.0):
            """creates a socket pool, the pool can lease out socket for send and recv.
            if caller only does send but not recv, the socket will not be reused until internally the pool recv data and discard them.

            :param url: url for sockets to connect to
            :param ctx: optionally force socket to use provided zmq context instead of creating a new zmq context
            :param timeout: defaults to 10 seconds, specifies how long should we be polling the socket, until we consider it to be dead, note this is not a blocking timeout.
            """
            self._url = url
            self._ctx = ctx
            if self._ctx is None:
                self._ctxown = zmq.Context()
                self._ctx = self._ctxown
            self._timeout = timeout

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

            log.debug('sockets: created = %d, closed = %d, acquired = %d, released = %d', self._opencount, self._closecount, self._acquirecount, self._releasecount)
            
            if self._ctxown is not None:
                try:
                    self._ctxown.destroy()
                except Exception:
                    log.exception()
                self._ctxown = None
            self._ctx = None

        def SetDestroy(self):
            # make sure no new socket can be created
            self._isok = False

            # make sure no one can acquire a socket now
            self._availablesockets = []

        def _OpenSocket(self):
            if not self._isok:
                return None

            socket = self._ctx.socket(zmq.REQ)
            socket.connect(self._url)
            assert(socket not in self._sockets)
            self._sockets[socket] = True
            self._opencount += 1

            log.debug('opened a socket, url = %s opened = %d, closed = %d', self._url, self._opencount, self._closecount)
            return socket

        def _CloseSocket(self, socket):
            assert(socket in self._sockets)
            self._closecount += 1
            del self._sockets[socket]
            try:
                socket.close()
            except:
                log.exception()

        def _StartPollingSocket(self, socket):
            assert(socket not in self._pollingsockets)
            self._pollingsockets[socket] = time.time()
            self._poller.register(socket, zmq.POLLIN|zmq.POLLOUT)

        def _StopPollingSocket(self, socket):
            assert(socket in self._pollingsockets)
            self._poller.unregister(socket)
            del self._pollingsockets[socket]            

        def Poll(self):
            """spin once and does internal polling of sockets
            """
            now = time.time()

            # poll for receives, non blocking
            for socket, event in self._poller.poll(0):
                if (event & zmq.POLLIN) == zmq.POLLIN:
                    log.verbose('a socket is ready for receive, url = %s, polling = %d, availble = %d', self._url, len(self._pollingsockets), len(self._availablesockets))

                    # at least one message can be received without blocking
                    try:
                        socket.recv(zmq.NOBLOCK)
                    except:
                        # when error occur, throw the socket away
                        log.exception()
                        self._StopPollingSocket(socket)
                        self._CloseSocket(socket)
                        continue

                    # reset the timestamp since we just called recv
                    self._pollingsockets[socket] = now

            # poll again for send, non blocking, some previously in recv state socket may now be available for sending
            for socket, event in self._poller.poll(0):
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

        def CreateUseScope(self):
            """return a UseScope object that can be used by the with statement to automatically acquire/release a socket from the pool.

            :return: a UseScope object
            """
            return self.UseScope(self)

        def AcquireSocket(self):
            """acquire a socket from the list of availble sockets for sending
            """
            self.Poll()
            self._acquirecount += 1
            if len(self._availablesockets) > 0:
                return self._availablesockets.pop()

            # no socket availble, create one
            return self._OpenSocket()

        def ReleaseSocket(self, socket, reuse=True):
            """release a socket after use, if caller did not call recv, the pool will take care of that
            """
            self._releasecount += 1
            if socket is not None:
                if self._isok and reuse:
                    self._StartPollingSocket(socket)
                else:
                    self._CloseSocket(socket)
            self.Poll()


    _hostname = None
    _port = None
    _url = None
    _pool = None
    _isok = False
    
    def __init__(self, hostname, port, ctx=None):
        self._hostname = hostname
        self._port = int(port)
        self._url = 'tcp://%s:%d' % (self._hostname, self._port)

        self._pool = self.ZmqSocketPool(self._url, ctx=ctx)
        self._isok = True
        
    def __del__(self):
        self.Destroy()
        
    def Destroy(self):
        self.SetDestroy()

        if self._pool is not None:
            self._pool.Destroy()
            self._pool = None

    def SetDestroy(self):
        self._isok = False
        if self._pool is not None:
            self._pool.SetDestroy()

    @property
    def hostname(self):
        return self._hostname
    
    @property
    def port(self):
        return self._port
        
    def SendCommand(self, command, timeout=10.0, fireandforget=False, sendjson=True, recvjson=True):
        """sends command via established zmq socket

        :param command: command in json format
        :param timeout: if None, block. If >= 0, use as timeout
        :param fireandforget: if True, will send command and immediately return without trying to receive
        :param sendjson: if True (default), will send data as json
        :param recvjson: if True (default), will parse received data as json
        
        :return: returns the response from the zmq server in json format if blockwait is True
        """
        log.verbose(u'Sending command via ZMQ: %s', command)

        if not self._isok:
            return None

        # attempt to send the message twice
        with self._pool.CreateUseScope() as socket:

            # we may be exiting, the pool refused to give us a socket
            if socket is None:
                return None

            # send phase
            starttime = time.time()
            while self._isok:
                # timeout checking
                elapsedtime = time.time() - starttime
                if timeout is not None and elapsedtime > timeout:
                    raise TimeoutError(u'Timed out trying to send to %s after %f seconds' % (self._url, elapsedtime))
                
                # poll to see if we can send, if not, loop
                if socket.poll(50, zmq.POLLOUT) == 0:
                    continue

                if sendjson:
                    socket.send_json(command, zmq.NOBLOCK)
                else:
                    socket.send(command, zmq.NOBLOCK)
                # break when successfully sent
                break

            # for fire and forget, no need to receive
            if fireandforget:
                return None

            # receive phase
            starttime = time.time()
            while self._isok:
                # timeout checking
                elapsedtime = time.time() - starttime
                if timeout is not None and elapsedtime > timeout:
                    raise TimeoutError(u'Timed out to get response from %s after %f seconds' % (self._url, elapsedtime))
                
                # poll to see if something has been received, if received nothing, loop
                if socket.poll(50, zmq.POLLIN) == 0:
                    continue
                
                if recvjson:
                    return socket.recv_json(zmq.NOBLOCK)
                else:
                    return socket.recv(zmq.NOBLOCK)

        return None
