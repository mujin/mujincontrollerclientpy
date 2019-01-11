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

import logging
log = logging.getLogger(__name__)

try:
    import mujincommon.i18n
    ugettext, ungettext = mujincommon.i18n.GetDomain('mujincontrollerclientpy').GetTranslationFunctions()
except ImportError:
    import gettext
    _null_translations = gettext.NullTranslations()
    ugettext = _null_translations.ugettext if hasattr(_null_translations, 'ugettext') else _null_translations.gettext
    ungettext = _null_translations.ungettext if hasattr(_null_translations, 'ungettext') else _null_translations.ngettext

_ = ugettext


@six.python_2_unicode_compatible
class ClientExceptionBase(Exception):
    """client base exception
    """
    def __init__(self, msg=''):
        if not isinstance(msg, six.text_type):
            msg = msg.decode('utf-8')
        self.msg = msg

    def __str__(self):
        return u'%s: %s' % (self.__class__.__name__, self.msg)

    def __repr__(self):
        return '<%s(%r)>' % (self.__class__.__name__, self.msg)


@six.python_2_unicode_compatible
class APIServerError(ClientExceptionBase):
    responseerror_message = None  # the error. should be unicode
    responseerrorcode = None  # the error code coming from the server
    responsestacktrace = None  # the traceback from the error. should be unicode
    inputcommand = None  # the command sent to the server

    def __init__(self, responseerror_message, responsestacktrace=None, responseerrorcode=None, inputcommand=None):
        if isinstance(responseerror_message, six.text_type):
            self.responseerror_message = responseerror_message
        elif responseerror_message is not None:
            self.responseerror_message = responseerror_message.decode('utf-8')
        if isinstance(responsestacktrace, six.text_type):
            self.responsestacktrace = responsestacktrace
        elif responsestacktrace is not None:
            self.responsestacktrace = responsestacktrace.decode('utf-8')

        self.responseerrorcode = responseerrorcode
        self.inputcommand = inputcommand

    def __str__(self):
        if self.responseerror_message is not None:
            return self.responseerror_message
        return _('Unknown error')

    def __repr__(self):
        return '<%s(%r, %r, %r, %r)>' % (self.__class__.__name__, self.responseerror_message, self.responsestacktrace, self.responseerrorcode, self.inputcommand)


def GetAPIServerErrorFromWeb(request_type, url, status_code, responsecontent):
    inputcommand = {
        'request_type': request_type,
        'url': url,
        'status_code': status_code,
    }
    responseerror_message = _('Unknown error')
    responseerrorcode = None
    responsestacktrace = None
    try:
        content = json.loads(responsecontent)
        responsestacktrace = content.get('stacktrace', None)
        responseerror_message = content.get('error_message', None)
        responseerrorcode = content.get('error_code', None)
    except ValueError:
        responseerror_message = responsecontent
    return APIServerError(responseerror_message, responsestacktrace, responseerrorcode, inputcommand)


def GetAPIServerErrorFromZMQ(response):
    """If response is in error, return the APIServerError instantiated from the response's error field. Otherwise return None
    """
    if response is None:
        return None

    if 'error' in response:
        if isinstance(response['error'], dict):
            return APIServerError(response['error']['description'], response['error']['stacktrace'], response['error']['errorcode'])

        else:
            return APIServerError(response['error'])

    elif 'exception' in response:
        return APIServerError(response['exception'])

    elif 'status' in response and response['status'] != 'succeeded':
        # something happened so raise exception
        return APIServerError(u'Resulting status is %s' % response['status'])

<<<<<<< HEAD

class TimeoutError(ClientExceptionBase):
    pass

class AuthenticationError(ClientExceptionBase):
    pass

class ControllerClientError(ClientExceptionBase):
    def __unicode__(self):
        return _('Controller Client Error:\n%s')%self.msg
=======
    return None


class TimeoutError(ClientExceptionBase):
    pass


class AuthenticationError(ClientExceptionBase):
    pass


class ControllerClientError(ClientExceptionBase):
    pass
>>>>>>> origin/cleanup
