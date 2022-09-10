# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
# Mujin controller client for bin picking task

# mujin imports
from . import realtimerobotclient

# logging
import logging
log = logging.getLogger(__name__)


class RealtimeITLPlanningControllerClient(realtimerobotclient.RealtimeRobotControllerClient):
    """Mujin controller client for realtimeitlplanning task
    """

    def __init__(self, **kwargs):
        """Logs into the mujin controller, initializes realtimeitlplanning task, and sets up parameters
        :param controllerurl: URL of the mujin controller, e.g. http://controller13
        :param controllerusername: Username of the mujin controller, e.g. testuser
        :param controllerpassword: Password of the mujin controller
        :param taskzmqport: Port of the realtimeitlplanning task's zmq server, e.g. 7110
        :param taskheartbeatport: Port of the realtimeitlplanning task's zmq server's heartbeat publisher, e.g. 7111
        :param taskheartbeattimeout: Seconds until reinitializing realtimeitlplanning task's zmq server if no heartbeat is received, e.g. 7
        :param scenepk: Primary key (pk) of the bin picking task scene, e.g. komatsu_ntc.mujin.dae
        :param robotname: Name of the robot, e.g. VP-5243I
        :param robotspeed: Speed of the robot, e.g. 0.4
        :param regionname: Name of the bin, e.g. container1
        :param targetname: Name of the target, e.g. plasticnut-center
        :param toolname: Name of the manipulator, e.g. 2BaseZ
        :param envclearance: Environment clearance in millimeters, e.g. 20
        :param usewebapi: Whether to use webapi for controller commands
        :param robotaccelmult: Optional multiplier for forcing the acceleration
        """
        super(RealtimeITLPlanningControllerClient, self).__init__(tasktype='realtimeitlplanning', **kwargs)

    def SetJointValues(self, jointvalues, robotname=None, timeout=10, usewebapi=True, **kwargs):
        taskparameters = {
            'command': 'SetJointValues',
            'jointvalues': jointvalues,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def GetITLState(self, robotname=None, timeout=10, usewebapi=True, fireandforget=False, **kwargs):
        taskparameters = {'command': 'GetITLState'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def MoveToCommand(self, program, commandindex=0, envclearance=15, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
        taskparameters = {
            'command': 'MoveToCommand',
            'program': program,
            'commandindex': commandindex,
            'envclearance': envclearance,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def ExecuteTrajectory(self, identifier, trajectories, statevalues=None, stepping=False, istep=None, cycles=1, restorevalues=None, envclearance=15, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
        taskparameters = {
            'command': 'ExecuteTrajectory',
            'identifier': identifier,
            'trajectories': trajectories,
            'statevalues': statevalues,
            'stepping': stepping,
            'envclearance': envclearance,
            'cycles': cycles,
        }
        if istep is not None:
            taskparameters['istep'] = istep
        if restorevalues is not None:
            taskparameters['restorevalues'] = restorevalues
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def ExecuteTrajectoryStep(self, reverse=False, envclearance=15, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
        taskparameters = {
            'command': 'ExecuteTrajectoryStep',
            'reverse': reverse,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def CancelExecuteTrajectoryStep(self, envclearance=15, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
        taskparameters = {'command': 'CancelExecuteTrajectoryStep'}
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def SetPauseExecuteTrajectory(self, envclearance=15, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
        taskparameters = {'command': 'SetPauseExecuteTrajectory'}
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def ResumeExecuteTrajectory(self, envclearance=15, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
        taskparameters = {'command': 'ResumeExecuteTrajectory'}
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
