# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

# logging
import time
import zmq

from . import GetExceptionStack, TimeoutError, ControllerClientError

import logging
log = logging.getLogger(__name__)

class ZmqClient(object):
    hostname = None
    port = None
    _url = None
    _socket = None
    _initialized = False
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
        self._initialized = False
        self.ConnectToServer(self._url)
        
    def __del__(self):
        self.Destroy()
        
    def Destroy(self):
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
        
    def ConnectToServer(self, url):
        """connects to the zmq server
        :param url: url of the zmq server, default is self._url
        """
        if url is None:
            url = self._url
        else:
            self._url = url
        log.debug(u"Connecting to %s...", url)
        try:
            self._socket = self._ctx.socket(zmq.REQ)
            self._socket.connect(url)
            self._initialized = True
        except Exception, e:  # TODO better exception handling
            log.error(u'failed to connect to %s: %s', url, GetExceptionStack())
            self._initialized = False
            raise
        
    def SendCommand(self, command, timeout=None):
        """sends command via established zmq socket
        :param command: command in json format
        :param timeout: if None, block. If >= 0, use as timeout
        :return: if zmq is not initialized, returns immediately, else returns the response from the zmq server in json format
        """
        if not self._initialized:
            raise ControllerClientError(u'zmq server is not initialized')
        
        log.debug(u'Sending command via ZMQ: ', command)
        try:
            self._socket.send_json(command)
        except zmq.ZMQError, e:
            log.error(u'Failed to send command %r to controller. zmq error: %s', command, e)
            # raise e
            if e.errno == zmq.EAGAIN:
                raise
            
            if e.errno == zmq.EFSM:
                log.warn(u'Zmq is in bad state')
            log.warn(u're-creating zmq socket and trying again')
            self._socket = self._ctx.socket(zmq.REQ)
            self._socket.connect(self._url)
            log.warn(u'Try to send again.')
            self._socket.send_json(command)
        return self.ReceiveCommand(timeout)
    
    def ReceiveCommand(self, timeout=None):
        if timeout is None:
            return self._socket.recv_json()
        else:
            starttime = time.time()
            result = ""
            triedagain = False
            while len(result) == 0 and time.time() - starttime < timeout:
                try:
                    result = self._socket.recv_json(zmq.NOBLOCK)
                except zmq.ZMQError, e:
                    if e.errno == zmq.EAGAIN:
                        triedagain = True
                    else:
                        if e.errno == zmq.EFSM:
                            log.warn(u'Zmq is in bad state, re-creating socket...')
                        self._socket = self._ctx.socket(zmq.REQ)
                        self._socket.connect(self._url)
                        # just raise the error, anyone we cannot recover the original response anymore...
                        raise
                    
#                         try:
#                             triedagain = True
#                             log.warn(u'Try to receive again.')
#                             result = self._socket.recv_json(zmq.NOBLOCK)
#                         except zmq.ZMQError, e:
#                             if e.errno != zmq.EAGAIN:
#                                 return {'status': 'error', 'error': u'Failed to receive command from controller. %d:%s %s' % (e.errno, zmq.strerror(e.errno), e.message)}
#                     else:
#                         # raise
#                         return {'status': 'error', 'error': u'Failed to receive command from controller. %d:%s %s' % (e.errno, zmq.strerror(e.errno), e.message)}
                time.sleep(0.1)
            if triedagain:
                if len(result) > 0:
                    log.verbose(u'retry succeeded, result: %s', result)
                else:
                    raise TimeoutError(u'Timed out to get response from %s:%d after %f seconds'%(self.hostname, self.port, timeout))
                
            return result
