# -*- coding: utf-8 -*-
# Copyright (C) 2012-2023 MUJIN Inc

import threading
import time

from . import _
from . import zmq
from . import GetMonotonicTime
from . import TimeoutError, UserInterrupt

import logging
log = logging.getLogger(__name__)


class ZmqSubscriber(object):
    """Subscriber that can handle ongoing subscriptions and automatic socket recreation.
    """

    _ctx = None # zmq context
    _ctxown = None # created zmq context

    _endpoint = None # zmq subscription endpoint
    _getEndpointFn = None # function that returns the endpoint string to subscribe to, must be thread-safe
    _callbackFn = None # function to call back when new message is received on the subscription socket

    _socket = None # zmq socket
    _socketEndpoint = None # connected socket endpoint
    _lastReceivedTimestamp = 0 # when message was last received on this subscription
    _timeout = 4.0 # beyond this number of seconds, the socket is considered dead and should be recreated
    _checkpreemptfn = None # function for checking for preemptions
    _conflate = True # whether to conflate received messages to avoid parsing stale message

    def __init__(self, endpoint=None, getEndpointFn=None, callbackFn=None, timeout=4.0, ctx=None, checkpreemptfn=None, conflate=True):
        """Subscribe to zmq endpoint.

        Args:
            endpoint: the zmq endpoint string to subscribe to
            getEndpointFn: a thread-safe function that returns the zmq endpoint, when this result changes, subscription socket will be recreated
            callbackFn: the function to call when subscription receives latest message, it is up to the caller to decode the raw zmq message received, the keyword arguments for the callback are: 1. message: the received raw message, 2. endpoint: the current subscription endpoint, 3: elapsedTime: the time in seconds taken since last message received or socket creation. When the subscription timed out, message will be None during callback
            timeout: number of seconds, after this duration, the subscription socket is considered dead and will be recreated automatically to handle network changes (Default: 4.0)
            checkpreemptfn: The function for checking for preemptions
            conflate: whether to conflate received messages to avoid parsing stale message
        """
        self._timeout = timeout
        self._endpoint = endpoint
        self._getEndpointFn = getEndpointFn
        self._callbackFn = callbackFn

        self._ctx = ctx
        if self._ctx is None:
            self._ctxown = zmq.Context()
            self._ctx = self._ctxown

        self._checkpreemptfn = checkpreemptfn
        self._conflate = conflate

    def __del__(self):
        self.Destroy()

    def __repr__(self):
        return '<%s(endpoint=%r)>' % (self.__class__.__name__, self.endpoint)

    @property
    def endpoint(self):
        """Endpoint string for the subscription
        """
        return self._endpoint

    def SetEndpoint(self, endpoint):
        """Update endpoint for subscription
        """
        self._endpoint = endpoint

    def Destroy(self):
        self._CloseSocket()
        if self._ctxown is not None:
            try:
                self._ctxown.destroy()
            except Exception as e:
                log.exception('caught exception when destroying zmq context: %s', e)
            self._ctxown = None
        self._ctx = None

    def _HandleReceivedMessage(self, message, endpoint, elapsedTime):
        """Call the user callback when message is received.
        """
        if self._callbackFn:
            self._callbackFn(message=message, endpoint=endpoint, elapsedTime=elapsedTime)

    def _HandleTimeout(self, endpoint, elapsedTime):
        """Call the user callback when subscription timed out.
        """
        if self._callbackFn:
            self._callbackFn(message=None, endpoint=endpoint, elapsedTime=elapsedTime)

    def _HandleNotConfigured(self):
        """Call the user callback when getEndpointFn() returns None, disabling the subscription temporarily.
        """
        if self._callbackFn:
            self._callbackFn(message=None, endpoint=None, elapsedTime=0)

    def _OpenSocket(self, endpoint):
        # close previous socket just in case
        self._CloseSocket()

        # create new subscription socket with new endpoint
        socket = self._ctx.socket(zmq.SUB)
        if self._conflate:
            socket.setsockopt(zmq.CONFLATE, 1) # store only newest message. have to call this before connect
        socket.setsockopt(zmq.TCP_KEEPALIVE, 1) # turn on tcp keepalive, do these configuration before connect
        socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 2) # the interval between the last data packet sent (simple ACKs are not considered data) and the first keepalive probe; after the connection is marked to need keepalive, this counter is not used any further
        socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 2) # the interval between subsequential keepalive probes, regardless of what the connection has exchanged in the meantime
        socket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 2) # the number of unacknowledged probes to send before considering the connection dead and notifying the application layer
        socket.connect(endpoint)
        socket.setsockopt(zmq.SUBSCRIBE, b'') # have to use b'' to make python3 compatible
        self._socket = socket
        self._socketEndpoint = endpoint
        return socket

    def _CloseSocket(self):
        if self._socket:
            try:
                self._socket.close()
            except Exception as e:
                log.exception('failed to close subscription socket for endpoint "%s": %s', self._socketEndpoint, e)
        self._socket = None
        self._socketEndpoint = None

    def _UpdateEndpoint(self):
        # check and see if endpoint has changed
        if self._getEndpointFn is not None:
            self._endpoint = self._getEndpointFn()

        endpoint = self._endpoint
        if self._socket is not None and self._socketEndpoint != endpoint:
            log.debug('subscription endpoint changed "%s" -> "%s", so closing previous subscription socket', self._socketEndpoint, endpoint)
            self._CloseSocket()

    def SpinOnce(self, timeout=None, checkpreemptfn=None):
        """Spin subscription once, ensure that each subscription is received at least once. Block up to supplied timeout duration. If timeout is None, then receive what we can receive without blocking or raising any timeout error.

        Args:
            timeout: If not None, will raise TimeoutError if not all subscriptions can be handled in time. If None, then receive what we can receive without blocking or raising TimeoutError.
            checkpreemptfn: The function for checking for preemptions

        Return:
            Raw message received
        """
        checkpreemptfn = checkpreemptfn or self._checkpreemptfn
        starttime = GetMonotonicTime()

        self._UpdateEndpoint()

        while True:
            now = GetMonotonicTime()

            # ensure socket
            endpoint = self._endpoint
            if endpoint is not None and self._socket is None:
                self._OpenSocket(endpoint)
                self._lastReceivedTimestamp = starttime

            # loop to get all received message and only process the last one
            if self._socket is not None:
                message = None
                while True:
                    try:
                        message = self._socket.recv(zmq.NOBLOCK)
                    except zmq.ZMQError as e:
                        if e.errno != zmq.EAGAIN:
                            log.exception('caught exception while trying to receive from subscription socket for endpoint "%s": %s', self._socketEndpoint, e)
                            self._CloseSocket()
                            raise
                        break # got EAGAIN, so break
                if message is not None:
                    self._HandleReceivedMessage(message=message, endpoint=self._socketEndpoint, elapsedTime=now - self._lastReceivedTimestamp)
                    self._lastReceivedTimestamp = now
                    return message

                if now - self._lastReceivedTimestamp > self._timeout:
                    log.debug('have not received message on subscription socket for endpoint "%s" in %.03f seconds, closing socket and re-creating', self._socketEndpoint, now - self._lastReceivedTimestamp)
                    self._CloseSocket()
                    endpoint = self._endpoint
                    if endpoint is not None:
                        self._OpenSocket(endpoint)
                        self._lastReceivedTimestamp = now

            if timeout is None:
                if self._socket is None:
                    self._HandleNotConfigured() # finished spinning without opening socket, report not configured before returning
                return None

            # check for timeout
            elapsedTime = now - starttime
            if elapsedTime > timeout:
                if self._socket is None:
                    self._HandleNotConfigured() # timed out due to no socket, then report not configured without raising
                    return None
                # report timeout and raise
                self._HandleTimeout(endpoint=self._socketEndpoint, elapsedTime=elapsedTime)
                raise TimeoutError(_('Timed out waiting to receive message from subscription to "%s" after %0.3f seconds') % (self._socketEndpoint, elapsedTime))

            # check preempt
            if checkpreemptfn:
                checkpreemptfn()

            # poll
            if self._socket is not None:
                self._socket.poll(20) # poll a little and try again
            else:
                time.sleep(0.2)
                self._UpdateEndpoint() # sleep a little and see if we have an endpoint to connect to now


class ZmqThreadedSubscriber(ZmqSubscriber):
    """A threaded version of ZmqSubscriber.
    """

    _threadInterval = None # thread spin interval in number of seconds, used to limit the rate of subscription if set
    _threadName = None # thread name for the background thread
    _thread = None # a background thread for handling subscription
    _stopThread = False # flag to preempt the background thread

    def __init__(self, threadName='zmqSubscriber', threadInterval=None, **kwargs):
        self._threadName = threadName
        self._threadInterval = threadInterval
        super(ZmqThreadedSubscriber, self).__init__(**kwargs)

        self._StartSubscriberThread()

    def Destroy(self):
        self._StopSubscriberThread()

        super(ZmqThreadedSubscriber, self).Destroy()

    def _StartSubscriberThread(self):
        self._StopSubscriberThread()

        self._stopThread = False
        self._thread = threading.Thread(name=self._threadName, target=self._RunSubscriberThread)
        self._thread.start()

    def _StopSubscriberThread(self):
        self._stopThread = True
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def _CheckPreempt(self):
        if self._stopThread:
            raise UserInterrupt(_('Stop has been requested'))
        if self._checkpreemptfn is not None:
            self._checkpreemptfn()

    def _RunSubscriberThread(self):
        log.debug('subscriber thread "%s" started', self._threadName)
        loggedTimeoutError = False # whether time out error has been logged once already
        try:
            while not self._stopThread:
                starttime = GetMonotonicTime()
                try:
                    self.SpinOnce(timeout=self._timeout, checkpreemptfn=self._CheckPreempt)
                    loggedTimeoutError = False
                except UserInterrupt as e:
                    log.exception('subscriber thread "%s" preempted: %s', self._threadName, e)
                    break # preempted
                except TimeoutError as e:
                    if not loggedTimeoutError:
                        log.exception('timed out in subscriber thread "%s": %s', self._threadName, e)
                        loggedTimeoutError = True
                except Exception as e:
                    log.exception('exception caught in subscriber thread "%s": %s', self._threadName, e)
                # rate limit the loop if desired
                if self._threadInterval is None:
                    continue
                elapsedTime = GetMonotonicTime() - starttime
                if elapsedTime > self._threadInterval:
                    continue
                time.sleep(self._threadInterval - elapsedTime)
        except Exception as e:
            log.exception('exception caught in subscriber thread "%s": %s', self._threadName, e)
        finally:
            log.debug('subscriber thread "%s" stopping', self._threadName)
            self._CloseSocket()
