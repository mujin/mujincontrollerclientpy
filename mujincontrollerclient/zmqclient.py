# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

# logging
import time
import logging
log = logging.getLogger(__name__)

# system imports
from traceback import format_exc
import zmq


class ZmqClient(object):
    def __init__(self, hostname, port, ctx=None):
        self.hostname = hostname
        self.port = int(port)
        self._url = 'tcp://%s:%d' % (self.hostname, self.port)
        if ctx is None:
            self._ctx = zmq.Context()
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

    def ConnectToServer(self, url):
        """connects to the zmq server
        :param url: url of the zmq server, default is self._url
        """
        if url is None:
            url = self._url
        log.info("Connecting to %s...", url)
        try:
            self._socket = self._ctx.socket(zmq.REQ)
            self._socket.connect(url)
            self._initialized = True
        except Exception, e:  # TODO better exception handling
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
        try:
            self._socket.send_json(command)
        except zmq.ZMQError, e:
            log.error(u'Failed to send command to controller. %s' % e.message)
            # raise e
            if e.errno == zmq.EFSM:
                log.warn(u'Receive message and try to send again.')
                self.ReceiveCommand(timeout)
                try:
                    self._socket.send_json(command)
                except zmq.ZMQError, e:
                    return {'status': 'error', 'exception': u'Failed to send command to controller. %d:%s %s' % (e.errno, zmq.strerror(e.errno), e.message)}
            else:
                return {'status': 'error', 'exception': u'Failed to send command to controller. %d:%s %s' % (e.errno, zmq.strerror(e.errno), e.message)}
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
                        # raise
                        return {'status': 'error', 'error': u'Failed to receive command to controller. %d:%s %s' % (e.errno, zmq.strerror(e.errno), e.message)}
                time.sleep(0.1)
            if triedagain:
                if len(result) > 0:
                    log.info('retry succeeded, result: %s' % result)
                else:
                    log.error('Timed out to get response from %s:%d after %f seconds' % (self.hostname, self.port, timeout))
                    # raise Exception('Timed out to get response from controller.')
                    return {'status': 'error', 'error': u'Timed out to get response from %s:%d after %f seconds' % (self.hostname, self.port, timeout)}
            return result
