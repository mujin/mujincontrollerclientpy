# -*- coding: utf-8 -*-
# Copyright (C) 2014-2015 MUJIN Inc.

try:
    import mujincommon.i18n
    ugettext, ungettext = mujincommon.i18n.GetDomain('mujincontrollerclientpy').GetTranslationFunctions()
except ImportError:
    import gettext
    _null_translations = gettext.NullTranslations()
    ugettext = _null_translations.ugettext
    ungettext = _null_translations.ugettext

_ = ugettext

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

#     def __eq__(self, r):
#         return self.msg == r.msg
#     
#     def __ne__(self, r):
#         return self.msg != r.msg

class ClientExceptionBase(Exception):
    """client base exception
    """
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

class APIServerError(Exception):
    responseerror_message = None # the error. should be unicode
    responseerrorcode = None # the error code coming from the server
    responsestacktrace = None # the traceback from the error. should be unicode
    inputcommand = None # the command sent to the server
    def __init__(self, responseerror_message, responsestacktrace=None, responseerrorcode=None, inputcommand=None, detailerrorcode=None):
        if isinstance(responseerror_message, unicode):
            self.responseerror_message = responseerror_message
        elif responseerror_message is not None:
            self.responseerror_message = unicode(responseerror_message, 'utf-8')
        if isinstance(responsestacktrace, unicode):
            self.responsestacktrace = responsestacktrace
        elif responsestacktrace is not None:
            self.responsestacktrace = unicode(responsestacktrace, 'utf-8')

        self.responseerrorcode = responseerrorcode
        self.inputcommand = inputcommand
        self.detailerrorcode = detailerrorcode
    def __unicode__(self):
        if self.responseerror_message is not None:
            return self.responseerror_message
        
        return _('Unknown error')
    
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __repr__(self):
        if self.detailerrorcode is None:
            return '<%s(%r, %r, %r, %r)>' % (self.__class__.__name__, self.responseerror_message, self.responsestacktrace, self.responseerrorcode, self.inputcommand)
        else:
            return '<%s(%r, %r, %r, %r, %r)>' % (self.__class__.__name__, self.responseerror_message, self.responsestacktrace, self.responseerrorcode, self.inputcommand, self.detailerrorcode)

def GetAPIServerErrorFromWeb(request_type, url, status_code, responsecontent):
    inputcommand = {'request_type':request_type, 'url':url, 'status_code':status_code}
    responseerror_message = _('Unknown error')
    responseerrorcode = None
    responsestacktrace = None
    try:
        content = json.loads(responsecontent)
        responsestacktrace = content.get('stacktrace',None)
        if responsestacktrace is not None:
            responsestacktrace = responsestacktrace.encode('utf-8')
        responseerror_message = content.get('errormessage', None)
        if responseerror_message is not None:
            responseerror_message = responseerror_message.encode('utf-8')
        responseerrorcode = content.get('errorcode',None)
        detailerrorcode = content.get('detailerrorcode', None)
    except ValueError:
        raise
        if isinstance(responsecontent, unicode):
            responseerror_message = responsecontent.encode('utf-8')
        else:
            responseerror_message = responsecontent
    return APIServerError(responseerror_message, responsestacktrace, responseerrorcode, inputcommand, detailerrorcode=detailerrorcode)

def GetAPIServerErrorFromZMQ(response):
    """If response is in error, return the APIServerError instantiated from the response's error field. Otherwise return None
    """
    if response is None:
        return None
    
    if 'error' in response:
        if isinstance(response['error'], dict):
            return APIServerError(response['error']['description'], response['error']['stacktrace'], response['error']['errorcode'], detailerrorcode=response['error'].get('detailerrorcode', None))
        
        else:
            return APIServerError(response['error'])
    
    elif 'exception' in response:
        return APIServerError(response['exception'])
    
    elif 'status' in response and response['status'] != 'succeeded':
        # something happened so raise exception
        return APIServerError(u'Resulting status is %s' % response['status'])
    
    return None

class FluidPlanningError(Exception):
    pass

class TimeoutError(Exception):
    pass

class AuthenticationError(Exception):
    pass

class ControllerClientError(ClientExceptionBase):
    def __unicode__(self):
        return _('Controller Client Error:\n%s')%self.msg

class BinPickingError(ClientExceptionBase):
    def __unicode__(self):
        return _('Bin Picking Client Error:\n%s')%self.msg

class HandEyeCalibrationError(ClientExceptionBase):
    def __unicode__(self):
        return _('Hand-eye Calibration Client Error:\n%s')%self.msg

from traceback import format_exc


def GetExceptionStack():
    """returns the unicode of format_exc
    """
    s = format_exc()
    if isinstance(s, unicode):
        return s
    return unicode(s, 'utf-8')
