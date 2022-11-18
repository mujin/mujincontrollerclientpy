# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 MUJIN Inc.

from .version import __version__ # noqa: F401

import six

try:
    import ujson as json  # noqa: F401
except ImportError:
    import json  # noqa: F401

from mujinwebstackclient import ClientExceptionBase

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
    ugettext, ungettext = mujincommon.i18n.GetDomain('mujinplanningserverclientpy').GetTranslationFunctions()
except ImportError:
    def ugettext(message):
        return message

    def ungettext(singular, plural, n):
        return singular if n == 1 else plural

_ = ugettext


class TimeoutError(ClientExceptionBase):
    pass

class UserInterrupt(ClientExceptionBase):
    pass
