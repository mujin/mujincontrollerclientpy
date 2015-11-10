# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
# Mujin controller client for bin picking task

# logging
import logging
log = logging.getLogger(__name__)

# mujin imports
from . import ControllerClientError, APIServerError
from . import realtimerobotclient
from . import ugettext as _

class RealtimeITLPlanningControllerClient(realtimerobotclient.RealtimeRobotControllerClient):
    """mujin controller client for realtimeitlplanning task
    """
    
    def __init__(self, **kwargs):
        
        """logs into the mujin controller, initializes realtimeitlplanning task, and sets up parameters
        :param controllerurl: url of the mujin controller, e.g. http://controller13
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        :param taskzmqport: port of the realtimeitlplanning task's zmq server, e.g. 7110
        :param taskheartbeatport: port of the realtimeitlplanning task's zmq server's heartbeat publisher, e.g. 7111
        :param taskheartbeattimeout: seconds until reinitializing realtimeitlplanning task's zmq server if no hearbeat is received, e.g. 7
        :param scenepk: pk of the bin picking task scene, e.g. komatsu_ntc.mujin.dae
        :param robotname: name of the robot, e.g. VP-5243I
        :param robotspeed: speed of the robot, e.g. 0.4
        :param regionname: name of the bin, e.g. container1
        :param targetname: name of the target, e.g. plasticnut-center
        :param toolname: name of the manipulator, e.g. 2BaseZ
        :param envclearance: environment clearance in milimeter, e.g. 20
        :param usewebapi: whether to use webapi for controller commands
        :param robotaccelmult: optional multiplier for forcing the acceleration
        """
        super(RealtimeITLPlanningControllerClient, self).__init__(tasktype='realtimeitlplanning', **kwargs)
    
    def SetJointValues(self, jointvalues, timeout=10, usewebapi=True, **kwargs):
        taskparameters = {
            'command': 'SetJointValues',
            'jointvalues': jointvalues,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)
    
    def GetITLState(self, timeout=10, usewebapi=True, **kwargs):
        taskparameters = {'command': 'GetITLState'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)

    def ExecuteTrajectory(self, trajectories, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
        taskparameters = {
            'command': 'ExecuteTrajectory',
            'trajectories': trajectories,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
