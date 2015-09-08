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
        
    def __del__(self):
        self.Destroy()
        
    def Destroy(self):
        self.SetDestroy()
        self._CloseSocket()
        
        if self._ctxown is not None:
            try:
                self._ctxown.destroy()
            except Exception:
                log.error(u'caught ctx: %s', GetExceptionStack())
            
            self._ctxown = None
        self._ctx = None

    def SetDestroy(self):
        self._isok = False
        
    def _CloseSocket(self):
        if self._socket is not None:
            self._socket.close()
            self._socket = None
        
    def ConnectToServer(self, url=None):
        """connects to the zmq server
        :param url: url of the zmq server, default is self._url
        """
        if url is None:
            url = self._url
        else:
            self._url = url
        
        self._CloseSocket()
        
        log.debug(u"Connecting to %s...", url)
        try:
            self._socket = self._ctx.socket(zmq.REQ)
            self._socket.connect(url)
            log.debug(u"connected to %s...", url)
        except Exception, e:  # TODO better exception handling
            log.error(u'failed to connect to %s: %s', url, GetExceptionStack())
            raise
        
    def SendCommand(self, command, timeout=10.0, blockwait=True):
        """sends command via established zmq socket
        :param command: command in json format
        :param timeout: if None, block. If >= 0, use as timeout
        :param blockwait: if True, will block and wait until function is done. Otherwise user will have to call ReceiveCommand on their own
        
        :return: if zmq is not initialized, returns immediately, else returns the response from the zmq server in json format
        """
        log.verbose(u'Sending command via ZMQ: %s', command)
        if self._socket is None:
            self.ConnectToServer()
        
        # attempt to send the message twice
        try:
            starttime = time.time()
            while self._isok:
                # timeout checking
                elapsedtime = time.time() - starttime
                if timeout is not None and elapsedtime > timeout:
                    raise TimeoutError(u'Timed out trying to send to %s after %f seconds' % (self._url, elapsedtime))
                
                # poll to see if we can send, if not, loop
                if self._socket.poll(50, zmq.POLLOUT) == 0:
                    continue

                self._socket.send_json(command, zmq.NOBLOCK)
                # break when successfully sent
                break
            
        except:
            # close the socket on any exception, since we may have skipped a
            # receive due to a previous exception causing the socket to get
            # stuck in a bad state.
            self._CloseSocket()
            raise
        
        if blockwait:
            return self.ReceiveCommand(timeout=timeout)
        
    def ReceiveCommand(self, timeout=10.0):
        assert(self._socket is not None) # always need a valid socket when receiving
        
        try:
            starttime = time.time()
            while self._isok:
                # timeout checking
                elapsedtime = time.time() - starttime
                if timeout is not None and elapsedtime > timeout:
                    raise TimeoutError(u'Timed out to get response from %s after %f seconds' % (self._url, elapsedtime))
                
                # poll to see if something has been received, if received nothing, loop
                if self._socket.poll(50, zmq.POLLIN) == 0:
                    continue
                
                return self._socket.recv_json(zmq.NOBLOCK)
            
        except:
            # here we will always close the socket when there is an exception,
            # because a skipped receive will cause the next send to always
            # fail.
            self._CloseSocket()
            raise
        
        return None
