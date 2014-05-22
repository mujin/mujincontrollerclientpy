# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 MUJIN Inc

# logging
import time
import logging
log = logging.getLogger(__name__)

# system imports
from traceback import format_exc
import zmq

class ZmqClient(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = int(port)
        self._url = 'tcp://%s:%d'%(self.hostname,self.port)
        self._ctx = None
        self._socket = None
        self._initialized = False

        self.ConnectToServer(self._url)

    def ConnectToServer(self,url):
        """connects to the zmq server
        :param url: url of the zmq server, default is self._url
        """
        if url is None:
            url = self._url
        log.info("Connecting to %s...",url)
        try:
            self._ctx = zmq.Context()
            self._socket = self._ctx.socket(zmq.REQ)
            self._socket.connect(url)
            self._initialized = True
        except Exception,e: #TODO better exception handling
            log.error(format_exc())            
            self._initialized = False
            raise e

    def SendCommand(self, command, timeout=None):
        """sends command via established zmq socket
        :param command: command in json format
        :param timeout: if None, block. If >= 0, use as timeout
        :return: if zmq is not initialized, returns immediately, else returns the response from the zmq server in json format
        """
        if not self._initialized:
            log.error('zmq server is not initialized')
            return

        log.debug(u'Sending command via ZMQ: ', command)
        self._socket.send_json(command)
        return self.ReceiveCommand(timeout)

    def ReceiveCommand(self, timeout=None):
        if timeout is None:
            return self._socket.recv_json()
        else:
            starttime = time.time()
            result = ""
            while len(result)==0 and time.time()-starttime<timeout:
                result= self._socket.recv_json(zmq.NOBLOCK)
                time.sleep(0.1)
            return result
