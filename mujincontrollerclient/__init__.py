# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 MUJIN Inc.

from logging import addLevelName, NOTSET, getLoggerClass

VERBOSE = 5


class MujinLogger(getLoggerClass()):
    def __init__(self, name, level=NOTSET):
        super(MujinLogger, self).__init__(name, level)

        addLevelName(VERBOSE, "VERBOSE")

    def verbose(self, msg, *args, **kwargs):
        if self.isEnabledFor(VERBOSE):
            self._log(VERBOSE, msg, args, **kwargs)


class ControllerClientError(Exception):
    pass


class APIServerError(Exception):
    pass


class FluidPlanningError(Exception):
    pass


class TimeoutError(Exception):
    pass


class BinPickingError(Exception):
    def __init__(self, msg=u''):
        self.msg = unicode(msg)

    def __unicode__(self):
        return u'%s: %s' % (self.__class__.__name__, self.msg)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return '<%s(%r)>' % (self.__class__.__name__, self.msg)

    def __eq__(self, r):
        return self.msg == r.msg

    def __ne__(self, r):
        return self.msg != r.msg


class HandEyeCalibrationError(Exception):
    def __init__(self, msg=u''):
        self.msg = unicode(msg)

    def __unicode__(self):
        return u'%s: %s' % (self.__class__.__name__, self.msg)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return '<%s(%r)>' % (self.__class__.__name__, self.msg)

    def __eq__(self, r):
        return self.msg == r.msg

    def __ne__(self, r):
        return self.msg != r.msg

from traceback import format_exc
def GetExceptionStack():
    """returns the unicode of format_exc
    """
    s = format_exc()
    if isinstance(s, unicode):
        return s
    
    return unicode(s,'utf-8')
