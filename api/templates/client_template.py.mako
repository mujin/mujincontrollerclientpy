# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

from . import json
from . import planningclient

import logging
log = logging.getLogger(__name__)

class ${clientClassName}(planningclient.PlanningControllerClient):
    """Mujin controller client for ${clientClassName} task"""
    _robotname = None  # Optional name of the robot selected
    _robotspeed = None  # Speed of the robot, e.g. 0.4
    _robotaccelmult = None  # Current robot accel mult
    _envclearance = None  # Environment clearance in millimeters, e.g. 20
    _robotBridgeConnectionInfo = None  # dict holding the connection info for the robot bridge.
    
    def __init__(self,  ${constructorExtraArgs}robotname=None, robotspeed=None, robotaccelmult=None, envclearance=10.0, robotBridgeConnectionInfo=None, taskzmqport=7110, taskheartbeatport=7111, taskheartbeattimeout=7.0, tasktype='', scenepk='', ctx=None, slaverequestid=None, controllerurl='http://127.0.0.1', controllerusername='', controllerpassword='', author=None):
        """
        Args:
            ${constructorExtraArgsDocstringLines}
            robotname (str): Name of the robot selected. Optional (can be empty)
            robotspeed (str, optional): Speed of the robot, e.g. 0.4.
            robotaccelmult (str, optional): Current robot acceleration multiplication.
            envclearance (str): Environment clearance in millimeter, e.g. 20
            robotBridgeConnectionInfo (str, optional): dict holding the connection info for the robot bridge.
            taskzmqport (int): Port of the task's ZMQ server, e.g. 7110
            taskheartbeatport (int): Port of the task's ZMQ server's heartbeat publisher, e.g. 7111
            taskheartbeattimeout (float): Seconds until reinitializing task's ZMQ server if no heartbeat is received, e.g. 7
            tasktype (str): Type of the task, e.g. 'binpicking', 'handeyecalibration', 'itlrealtimeplanning3'
            scenepk (str): Primary key (pk) of the scene, e.g. irex_demo.mujin.dae
            controllerurl (str): URL of the mujin controller, e.g. http://controller14
            controllerusername (str): Username for the Mujin controller, e.g. testuser
            controllerpassword (str): Password for the Mujin controller
        """
        ${constructorExtraContent}
        self._robotname = robotname
        self._robotspeed = robotspeed
        self._robotaccelmult = robotaccelmult
        self._envclearance = envclearance
        self._robotBridgeConnectionInfo = robotBridgeConnectionInfo
        super(${clientClassName}, self).__init__(taskzmqport=taskzmqport, taskheartbeatport=taskheartbeatport, taskheartbeattimeout=taskheartbeattimeout, tasktype=tasktype, scenepk=scenepk, ctx=ctx, slaverequestid=slaverequestid, controllerurl=controllerurl, controllerusername=controllerusername, controllerpassword=controllerpassword, author=author)

    def GetRobotConnectionInfo(self):
        """ """
        return self._robotBridgeConnectionInfo
    
    def SetRobotConnectionInfo(self, robotBridgeConnectionInfo):
        """

        Args:
            robotBridgeConnectionInfo:
        """
        self._robotBridgeConnectionInfo = robotBridgeConnectionInfo
    
    def GetRobotName(self):
        """ """
        return self._robotname

    def SetRobotName(self, robotname):
        """

        Args:
            robotname (str):
        """
        self._robotname = robotname

    def SetRobotSpeed(self, robotspeed):
        """

        Args:
            robotspeed:
        """
        self._robotspeed = robotspeed

    def SetRobotAccelMult(self, robotaccelmult):
        """

        Args:
            robotaccelmult:
        """
        self._robotaccelmult = robotaccelmult

    def ExecuteCommand(self, taskparameters, robotname=None, toolname=None, robotspeed=None, robotaccelmult=None, envclearance=None, usewebapi=None, timeout=10, fireandforget=False, respawnopts=None):
        """Wrapper to ExecuteCommand with robot info specified in taskparameters.

        Executes a command in the task.

        Args:
            taskparameters (dict): Specifies the arguments of the task/command being called.
            robotname (str, optional): Name of the robot
            robotaccelmult (float, optional):
            envclearance (float, optional):
            respawnopts (optional):
            toolname (str, optional): Name of the manipulator. Default: self.toolname
            timeout (float, optional):  (Default: 10)
            fireandforget (bool, optional):  (Default: False)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            robotspeed (float, optional):

        Returns:
            dict: Contains:
                - robottype (str): robot type
                - currentjointvalues (list[float]): current joint values, vector length = DOF
                - elapsedtime (float): elapsed time in seconds
                - numpoints (int): the number of points
                - error (dict): optional error info
                - desc (str): error message
                - type (str): error type
                    - errorcode (str): error code
        """
        if robotname is None:
            robotname = self._robotname
        
        # caller wants to use a different tool
        if toolname is not None:
            # set at the first level
            taskparameters['toolname'] = toolname
        
        if robotname is not None:
            taskparameters['robotname'] = robotname
        
        if 'robotspeed' not in taskparameters:
            if robotspeed is None:
                robotspeed = self._robotspeed
            if robotspeed is not None:
                taskparameters['robotspeed'] = robotspeed

        if 'robotaccelmult' not in taskparameters:
            if robotaccelmult is None:
                robotaccelmult = self._robotaccelmult
            if robotaccelmult is not None:
                taskparameters['robotaccelmult'] = robotaccelmult
        
        if self._robotBridgeConnectionInfo is not None:
            taskparameters['robotBridgeConnectionInfo'] = self._robotBridgeConnectionInfo
        
        if 'envclearance' not in taskparameters or taskparameters['envclearance'] is None:
            if envclearance is None:
                envclearance = self._envclearance
            if envclearance is not None:
                taskparameters['envclearance'] = envclearance

        return super(${clientClassName}, self).ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget, respawnopts=respawnopts)

    # 
    # Generated commands
    # 

${clientContent}