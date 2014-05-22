# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 MUJIN Inc
# Mujin controller client base

# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# system imports

# mujin imports
from . import ControllerClientError
from . import controllerclientraw as webapiclient
from . import zmqclient
import simplejson

class ControllerClientBase(object):
    """mujin controller client base
    """
    def __init__(self, controllerurl, controllerusername, controllerpassword, taskzmqport, taskheartbeatport, taskheartbeattimeout, tasktype, scenepk, initializezmq=False):
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

        # logs in via web api
        self.controllerurl = controllerurl
        self.controllerIp = controllerurl[len('http://'):].split(":")[0]
        if len(controllerurl[len('http://'):].split(":"))>1:
            self.controllerPort = controllerurl[len('http://'):].split(":")[1]
        else:
            self.controllerPort = 80
        self.controllerusername = controllerusername
        self.controllerpassword = controllerpassword
        self.LogIn(controllerurl, controllerusername, controllerpassword)

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
            
            self._zmqclient = zmqclient.ZmqClient(self.controllerIp, taskzmqport)

    def LogIn(self, controllerurl, controllerusername, controllerpassword):
        """logs into the mujin controller via web api
        """
        log.info('logging into controller at %s'%(controllerurl))
        webapiclient.config.BASE_CONTROLLER_URL = controllerurl
        webapiclient.config.USERNAME = controllerusername
        webapiclient.config.PASSWORD = controllerpassword
        webapiclient.Login()
        log.info('successfully logged into mujin controller as %s'%(controllerusername))
        
    def ExecuteCommandViaWebapi(self,taskparameters, webapitimeout=3000):
        """executes command via web api
        """
        if not webapiclient.IsVerified():
            raise ControllerClientError('cannot execute command, need to log into the mujin controller first')

        if self.tasktype == 'binpicking':
            results = webapiclient.ExecuteBinPickingTask(self.scenepk, taskparameters, timeout=webapitimeout)
        elif self.tasktype == 'handeyecalibration':
            results = webapiclient.ExecuteHandEyeCalibrationTask(self.scenepk, taskparameters, timeout=webapitimeout)
        else:
            raise ControllerClientError(u'unknown task type: %s'%self.tasktype)
        return results

    def ExecuteCommand(self, taskparameters, usewebapi=False, webapitimeout=3000):
        """executes command with taskparameters
        :param taskparameters: task parameters in json format
        :param webapitimeout: timeout in seconds for web api call
        :return: return the server response in json format
        """
        log.debug(u'Executing task with parameters: %s',taskparameters)
        if usewebapi:
            response = self.ExecuteCommandViaWebapi(taskparameters, webapitimeout)
        else:
            response = self._zmqclient.SendCommand(taskparameters)
        if type(response) == str:
            raise ControllerClientError(u'response is string, not json! response: %s'%response)
        return response    

    def InitializeControllerZmqServer(self, taskzmqport=7110, taskheartbeatport=7111):
        """starts the zmq server on mujin controller
        no need to call this for visionserver initialization, visionserver calls this during initialization
        """
        taskparameters = {'command': 'InitializeZMQ',
                          'port': taskzmqport,
                          'heartbeatPort': taskheartbeatport,
                          }
        return self.ExecuteCommand(taskparameters, usewebapi=True)
