# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 MUJIN Inc.
import json

from logging import addLevelName, NOTSET, getLoggerClass

VERBOSE = 5

class MujinLogger(getLoggerClass()):
    def __init__(self, name, level=NOTSET):
        super(MujinLogger, self).__init__(name, level)

        addLevelName(VERBOSE, "VERBOSE")
        
    def verbose(self, msg, *args, **kwargs):
        if self.isEnabledFor(VERBOSE):
            self._log(VERBOSE, msg, args, **kwargs)

class APIServerError(Exception):
    """error from API server
    """
    responseerror_message = None # the error
    responsetraceback = None # the traceback from the error
    def __init__(self, request_type, url, status_code, responsecontent):
        self.request_type = request_type
        self.url = unicode(url)
        self.status_code = status_code
        try:
            content = json.loads(responsecontent)
            self.responsetraceback = content.get('traceback',None)
            if self.responsetraceback is not None:
                self.responsetraceback = self.responsetraceback.encode('utf-8')
            self.responseerror_message = content.get('error_message', None)
            if self.responseerror_message is not None:
                self.responseerror_message = self.responseerror_message.encode('utf-8')
        except ValueError:
            self.responseerror_message = responsecontent.encode('utf-8')
        
    def __unicode__(self):
        error_base = u'Error with %s to %s\n\nThe API call failed (status: %s)' % (self.request_type, self.url, self.status_code)
        if self.responsetraceback is not None:
            error_base += u', here is the stack trace that came back in the request:\n%s' % (self.responsetraceback)
        return error_base
    
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __repr__(self):
        return '<%s(%r, %r, %r, %r)>' % (self.__class__.__name__, self.request_type, self.url, self.status_code, {'traceback':self.responsetraceback, 'error_message':self.responseerror_message})
    
#     def __eq__(self, r):
#         return self.msg == r.msg
#     
#     def __ne__(self, r):
#         return self.msg != r.msg

class ControllerClientError(Exception):
    responseerror_message = None # the error
    responsetraceback = None # the traceback from the error
    def __init__(self, responseerror_message, responsetraceback=None):
        self.responseerror_message = responseerror_message
        self.responsetraceback = responsetraceback

    def __unicode__(self):
        if self.responseerror_message is not None:
            return self.responseerror_message

        return u'Unknown error'

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return '<%s(%r, %r)>' % (self.__class__.__name__, self.responseerror_message, self.responsetraceback)
    
class FluidPlanningError(Exception):
    pass

class TimeoutError(Exception):
    pass

class AuthenticationError(Exception):
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
    return unicode(s, 'utf-8')
