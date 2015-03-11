# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc
"""
Mujin controller client base
"""
from urlparse import urlparse
from urllib import quote, unquote
import os

# logging
import logging
log = logging.getLogger(__name__)

# system imports

# mujin imports
from . import ControllerClientError
from . import controllerclientraw as webapiclient
from . import zmqclient

# the outside world uses this specifier to signify a '#' specifier. This is needed
# because '#' in URL parsing is a special role
id_separator = u'@'


def GetFilenameFromURI(uri, mujinpath):
    """returns the filesystem path that the URI points to.
    :param uri: points to mujin:/ resource

    example:

      GetFilenameFromURI(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae',u'/var/www/media/u/testuser')
      returns: (ParseResult(scheme=u'mujin', netloc='', path=u'/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae', params='', query='', fragment=''), u'/var/www/media/u/testuser/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae')
    """
    index = uri.find(id_separator)
    if index >= 0:
        res = urlparse(uri[:index])
    else:
        res = urlparse(uri)
    if res.scheme != 'mujin':
        raise ControllerClientError(_('Only mujin: sceheme supported of %s') % uri)

    if len(res.path) == 0 or res.path[0] != '/':
        raise ControllerClientError(_('path is not absolute on URI %s') % uri)

    return res, os.path.join(mujinpath, res.path[1:])


def GetURIFromPrimaryKey(pk):
    """Given the encoded primary key (has to be str object), returns the unicode URL.
    If pk is a unicode object, will use inside url as is, otherwise will decode

    example:

      GetURIFromPrimaryKey('%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122')
      returns: u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae'
    """
    pkunicode = GetUnicodeFromPrimaryKey(pk)
    # check if separator is present
    index = pkunicode.find(id_separator)
    if index >= 0:
        basefilename = pkunicode[0:index]
        if len(os.path.splitext(basefilename)[1]) == 0:
            # no extension present in basefilename, so default to mujin.dae
            basefilename += u'.mujin.dae'
        return u'mujin:/' + basefilename + pkunicode[index:]

    if len(os.path.splitext(pkunicode)[1]) == 0:
        # no extension present in basefilename, so default to mujin.dae
        pkunicode += u'.mujin.dae'
    return u'mujin:/' + pkunicode


def GetUnicodeFromPrimaryKey(pk):
    """Given the encoded primary key (has to be str object), returns the unicode string.
    If pk is a unicode object, will return the string as is.

    example:

      GetUnicodeFromPrimaryKey('%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122')
      returns: u'\u691c\u8a3c\u52d5\u4f5c1_121122'
    """
    if not isinstance(pk, unicode):
        return unicode(unquote(str(pk)), 'utf-8')

    else:
        return pk


def GetPrimaryKeyFromURI(uri):
    """
    example:

      GetPrimaryKeyFromURI(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae')
      returns u'%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122'
    """
    res = urlparse(unicode(uri))
    path = res.path[1:]
    return quote(path.encode('utf-8'), '')


class ControllerClientBase(object):
    """mujin controller client base
    """
    _usewebapi = True  # if True use the HTTP webapi, otherwise the zeromq webapi (internal use only)
    sceneparams = {}

    def __init__(self, controllerurl, controllerusername, controllerpassword, taskzmqport, taskheartbeatport, taskheartbeattimeout, tasktype, scenepk, initializezmq=False, usewebapi=True, ctx=None):
        """logs into the mujin controller and initializes the task's zmq connection
        :param controllerurl: url of the mujin controller, e.g. http://controller14
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        :param taskzmqport: port of the task's zmq server, e.g. 7110
        :param taskheartbeatport: port of the task's zmq server's heartbeat publisher, e.g. 7111
        :param taskheartbeattimeout: seconds until reinitializing task's zmq server if no hearbeat is received, e.g. 7
        :param tasktype: type of the task
        :param scenepk: pk of the bin picking task scene, e.g. irex2013.mujin.dae
        :param initializezmq: whether to initialize controller zmq server
        """
        # task
        self.tasktype = tasktype
        self.scenepk = scenepk
        self._usewebapi = usewebapi
        # logs in via web api
        self.controllerurl = controllerurl
        self.controllerIp = controllerurl[len('http://'):].split(":")[0]
        if len(controllerurl[len('http://'):].split(":")) > 1:
            self.controllerPort = controllerurl[len('http://'):].split(":")[1]
        else:
            self.controllerPort = 80
        self.controllerusername = controllerusername
        self.controllerpassword = controllerpassword
        self.LogIn(controllerurl, controllerusername, controllerpassword)
        self.sceneparams = {'scenetype': 'mujincollada', 'scenefilename': self.scenepk, 'scale': [1.0, 1.0, 1.0]}  # TODO: set scenetype according to the scene

        # connects to task's zmq server
        self._zmqclient = None
        if taskzmqport is not None:
            self.taskzmqport = taskzmqport
            self.taskheartbeatport = taskheartbeatport
            self.taskheartbeattimeout = taskheartbeattimeout
            if initializezmq:
                log.info('initializing controller zmq server...')
                self.InitializeControllerZmqServer(taskzmqport, taskheartbeatport)
                # TODO add heartbeat logic

            self._zmqclient = zmqclient.ZmqClient(self.controllerIp, taskzmqport, ctx)

    def LogIn(self, controllerurl, controllerusername, controllerpassword):
        """logs into the mujin controller via web api
        """
        log.info('logging into controller at %s' % (controllerurl))
        webapiclient.config.BASE_CONTROLLER_URL = controllerurl
        webapiclient.config.USERNAME = controllerusername
        webapiclient.config.PASSWORD = controllerpassword
        webapiclient.Login()
        log.info('successfully logged into mujin controller as %s' % (controllerusername))

    def ExecuteCommandViaWebapi(self, taskparameters, webapitimeout=3000):
        """executes command via web api
        """
        if not webapiclient.IsVerified():
            raise ControllerClientError('cannot execute command, need to log into the mujin controller first')

        if self.tasktype == 'binpicking':
            results = webapiclient.ExecuteBinPickingTaskSync(self.scenepk, taskparameters)  # , timeout=webapitimeout)
        elif self.tasktype == 'handeyecalibration':
            # results = webapiclient.ExecuteHandEyeCalibrationTaskAsync(self.scenepk, taskparameters, timeout=webapitimeout)
            results = webapiclient.ExecuteHandEyeCalibrationTaskSync(self.scenepk, taskparameters)
        else:
            raise ControllerClientError(u'unknown task type: %s' % self.tasktype)
        return results

    def ExecuteCommand(self, taskparameters, usewebapi=None, webapitimeout=3000, timeout=None):
        """executes command with taskparameters
        :param taskparameters: task parameters in json format
        :param webapitimeout: timeout in seconds for web api call
        :return: return the server response in json format
        """
        log.debug(u'Executing task with parameters: %s', taskparameters)
        if usewebapi is None:
            usewebapi = self._usewebapi
        if usewebapi:
            response = self.ExecuteCommandViaWebapi(taskparameters, webapitimeout)
        else:
            response = self._zmqclient.SendCommand(taskparameters, timeout)
        if 'error' in response:
            raise ControllerClientError(u'Got exception: %s' % response['error'])
        elif 'exception' in response:
            raise ControllerClientError(u'Got exception: %s' % response['exception'])
        return response

    def InitializeControllerZmqServer(self, taskzmqport=7110, taskheartbeatport=7111):
        """starts the zmq server on mujin controller
        no need to call this for visionserver initialization, visionserver calls this during initialization
        """
        taskparameters = {'command': 'InitializeZMQ',
                          'port': taskzmqport,
                          'heartbeatPort': taskheartbeatport,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteCommand(taskparameters, usewebapi=True)  # for webapi
