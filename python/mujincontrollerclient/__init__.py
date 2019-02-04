# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 MUJIN Inc.

import six

try:
    import ujson as json  # noqa: F401
except ImportError:
    import json  # noqa: F401

try:
    import urllib.parse as urlparse  # noqa: F401
except ImportError:
    import urlparse  # noqa: F401

import zmq  # noqa: F401 # TODO: stub zmq

# use GetMonotonicTime if possible
try:
    from mujincommon import GetMonotonicTime
except ImportError:
    import time
    if hasattr(time, 'monotonic'):
        def GetMonotonicTime():
            return time.monotonic()
    else:
        def GetMonotonicTime():
            return time.time()

import logging
log = logging.getLogger(__name__)

try:
    import mujincommon.i18n
    ugettext, ungettext = mujincommon.i18n.GetDomain('mujincontrollerclientpy').GetTranslationFunctions()
except ImportError:
    def ugettext(message):
        return message

    def ungettext(singular, plural, n):
        return singular if n == 1 else plural

_ = ugettext


@six.python_2_unicode_compatible
class ClientExceptionBase(Exception):
    """client base exception
    """
    _message = None  # the error message, should be unicode

    def __init__(self, message=''):
        if message is not None and not isinstance(message, six.text_type):
            message = message.decode('utf-8', 'ignore')
        self._message = message

    def __str__(self):
        return u'%s: %s' % (self.__class__.__name__, self._message)

    def __repr__(self):
        return '<%s(message=%r)>' % (self.__class__.__name__, self._message)


@six.python_2_unicode_compatible
class APIServerError(ClientExceptionBase):
    _message = None  # the error. should be unicode
    _errorcode = None  # the error code coming from the server
    _stacktrace = None  # the traceback from the error. should be unicode
    _inputcommand = None  # the command sent to the server

    def __init__(self, message, stacktrace=None, errorcode=None, inputcommand=None):
        if message is not None and not isinstance(message, six.text_type):
            message = message.decode('utf-8', 'ignore')

        if stacktrace is not None and not isinstance(stacktrace, six.text_type):
            stacktrace = stacktrace.decode('utf-8', 'ignore')

        self._message = message
        self._stacktrace = stacktrace
        self._errorcode = errorcode
        self._inputcommand = inputcommand

    def __str__(self):
        if self._message is not None:
            return self._message
        return _('Unknown error')

    def __repr__(self):
        return '<%s(message=%r, stacktrace=%r, errorcode=%r, inputcommand=%r)>' % (self.__class__.__name__, self._message, self._stacktrace, self._errorcode, self._inputcommand)


class TimeoutError(ClientExceptionBase):
    pass


class AuthenticationError(ClientExceptionBase):
    pass


class ControllerClientError(ClientExceptionBase):
    pass


class URIError(ClientExceptionBase):
    pass
