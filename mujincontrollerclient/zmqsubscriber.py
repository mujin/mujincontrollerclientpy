# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

# logging
import time
import logging
import threading
log = logging.getLogger(__name__)

import zmq


class ZmqSubscriber(object):
    def __init__(self, host, port, ctx=None):
        self._host = host
        self._port = port
        self._thread = None
        self._msg = ""
        self._shutdown = False
        if ctx is None:
            self._ctx = zmq.Context()
        else:
            self._ctx = ctx

    def __del__(self):
        self.StopSubscription()

    def Connect(self, host, port):
        self._socket.connect("tcp://%s:%s" % (host, port))
        self._socket.setsockopt(zmq.SUBSCRIBE, "")
        self._poller.register(self._socket, zmq.POLLIN)

    def __enter__(self):
        self.StartSubscription()
        return self

    def __exit__(self, type, value, traceback):
        self.StopSubscription()

    def StartSubscription(self):
        self._thread = threading.Thread(target=self._StartSubscription)
        self._thread.start()

    def StopSubscription(self):
        if not self._shutdown:
            self._shutdown = True
            self._thread.join()

    def _StartSubscription(self):
        self._shutdown = False
        self._socket = self._ctx.socket(zmq.SUB)
        self._poller = zmq.Poller()
        self.Connect(self._host, self._port)

        while not self._shutdown:
            socks = dict(self._poller.poll(1000))
            if self._socket in socks and socks.get(self._socket) == zmq.POLLIN:
                try:
                    self._msg = self._socket.recv(zmq.NOBLOCK)
                except zmq.ZMQError, e:
                    print e
                    pass
            time.sleep(0.01)  # sec

    def GetMessage(self):
        return self._msg
