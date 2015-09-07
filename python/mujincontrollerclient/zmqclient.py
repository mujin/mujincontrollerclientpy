# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

# logging
import time
import zmq

from . import GetExceptionStack, TimeoutError, ControllerClientError
from . import ugettext as _

import logging
log = logging.getLogger(__name__)

class ZmqClient(object):
    hostname = None
    port = None
    _url = None
    _socket = None
    _isok = False
    _ctx = None # the context to use
    _ctxown = None # the context owned exclusively by this streamer client
    
    def __init__(self, hostname, port, ctx=None):
        self.hostname = hostname
        self.port = int(port)
        self._url = 'tcp://%s:%d' % (self.hostname, self.port)
        if ctx is None:
            self._ctxown = self._ctx = zmq.Context()
        else:
            self._ctx = ctx
        self._socket = None
        self._isok = True

        self.ConnectToServer(self._url)
        
    def __del__(self):
        self.Destroy()
        
    def Destroy(self):
        self._isok = False

        if self._socket is not None:
            self._socket.close()
            self._socket = None
        
        if self._ctxown is not None:
            try:
                self._ctxown.destroy()
            except Exception:
                log.error(u'caught ctx: %s', GetExceptionStack())
            
            self._ctxown = None
        self._ctx = None

    def SetDestroy(self):
        self._isok = False
        
    def ConnectToServer(self, url=None):
        """connects to the zmq server
        :param url: url of the zmq server, default is self._url
        """
        if url is None:
            url = self._url
        else:
            self._url = url

        if self._socket is not None:
            self._socket.close()
            self._socket = None

        log.debug(u"Connecting to %s...", url)
        try:
            self._socket = self._ctx.socket(zmq.REQ)
            self._socket.connect(url)
            self._initialized = True
        except:  # TODO better exception handling
            log.exception(u'Failed to connect to %s', url)
            raise
        
    def SendCommand(self, command, timeout=None):
        """sends command via established zmq socket
        :param command: command in json format
        :param timeout: if None, block. If >= 0, use as timeout
        :return: if zmq is not initialized, returns immediately, else returns the response from the zmq server in json format
        """
        log.verbose(u'Sending command via ZMQ: %s', command)

        # attempt to send the message twice
        attempts = 0
        maxattempts = 2
        while self._isok:
            attempts += 1

            try:
                # no timeout, call directly
                if timeout is None:
                    self._socket.send_json(command)
                    break

                starttime = time.time()
                while self._isok:

                    # timeout checking
                    elapsedtime = time.time() - starttime
                    if elapsedtime > timeout:
                        raise TimeoutError(u'Timed out trying to send to %s after %f seconds' % (self._url, elapsedtime))

                    # poll to see if we can send, if not, loop
                    if self._socket.poll(50, zmq.POLLOUT) == 0:
                        continue

                    try:
                        self._socket.send_json(command, zmq.NOBLOCK)
                        # break when successfully sent
                        break
                    except zmq.ZMQError, e:
                        # error should not be eagain because we polled and made sure that we can send
                        assert(e.errno != zmq.EAGAIN)
                        raise

                # break when successfully sent
                break

            except zmq.ZMQError, e:
                if attempts >= maxattempts:
                    raise

                log.exception('Exception caught when sending command via ZMQ, will try again.')
                self.ConnectToServer()
                continue

        return self.ReceiveCommand(timeout)
    
    def ReceiveCommand(self, timeout=None):
        try:
            # no timeout, call directly
            if timeout is None:
                return self._socket.recv_json()

            starttime = time.time()
            while self._isok:

                # timeout checking
                elapsedtime = time.time() - starttime
                if elapsedtime > timeout:
                    raise TimeoutError(u'Timed out to get response from %s after %f seconds' % (self._url, elapsedtime))

                # poll to see if something has been received, if received nothing, loop
                if self._socket.poll(50, zmq.POLLIN) == 0:
                    continue

                try:
                    return self._socket.recv_json(zmq.NOBLOCK)
                except zmq.ZMQError, e:
                    # error should not be eagain because we polled and made sure that there is something to receive
                    assert(e.errno != zmq.EAGAIN)
                    raise
                    
        except zmq.ZMQError, e:
            self.ConnectToServer()
            # just raise the error, we cannot recover the original response anyway ...
            raise

        return None
