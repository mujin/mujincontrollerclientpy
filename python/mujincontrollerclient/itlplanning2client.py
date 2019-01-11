# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
# Mujin controller client for bin picking task

# mujin imports
from . import realtimerobotclient

# logging
import logging
log = logging.getLogger(__name__)


class ITLPlanning2ControllerClient(realtimerobotclient.RealtimeRobotControllerClient):
    """mujin controller client for itlplanning2 task
    """

    def __init__(self, **kwargs):

        """logs into the mujin controller, initializes itlplanning2 task, and sets up parameters
        :param controllerurl: url of the mujin controller, e.g. http://controller13
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        :param taskzmqport: port of the itlplanning2 task's zmq server, e.g. 7110
        :param taskheartbeatport: port of the itlplanning2 task's zmq server's heartbeat publisher, e.g. 7111
        :param taskheartbeattimeout: seconds until reinitializing itlplanning2 task's zmq server if no hearbeat is received, e.g. 7
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
        super(ITLPlanning2ControllerClient, self).__init__(tasktype='itlplanning2', **kwargs)

    def ReloadModule(self, timeout=10, **kwargs):
        return self.ExecuteCommand({'command': 'ReloadModule'}, timeout=timeout, **kwargs)

    def GetJointValuesFromToolValues(self, toolvalues, initjointvalues=None, timeout=1, usewebapi=True, **kwargs):
        taskparameters = {
            'command': 'GetJointValuesFromToolValues',
            'toolvalues': toolvalues,
        }
        if initjointvalues is not None:
            taskparameters['initjointvalues'] = initjointvalues
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def ComputeCommandPosition(self, movecommand, jointvalues=None, usewebapi=True, timeout=5, **kwargs):
        """
        computes the position from the command
        """
        taskparameters = {
            'command': 'ComputeCommandPosition',
            'movecommand': movecommand,
        }
        if jointvalues is not None:
            taskparameters['jointvalues'] = jointvalues
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def JogCommandPosition(self, movecommand, direction=None, rotation=None, movealongsurface=True, fireandforget=False, timeout=5, usewebapi=False, **kwargs):
        taskparameters = {
            'command': 'JogCommandPosition',
            'movecommand': movecommand,
            'movealongsurface': movealongsurface,
        }
        if direction is not None:
            taskparameters['direction'] = direction
        if rotation is not None:
            taskparameters['rotation'] = rotation
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, fireandforget=fireandforget, timeout=timeout, usewebapi=usewebapi)

    def MoveToSurface(self, distancetosurface, robotspeed=None, robotaccelmult=None, toolname=None, timeout=10, usewebapi=True, **kwargs):
        taskparameters = {
            'command': 'MoveToSurface',
            'distancetosurface': distancetosurface,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout, usewebapi=usewebapi)

    def MoveToCommand(self, movecommand, toinitial=False, robotspeed=None, robotaccelmult=None, toolname=None, timeout=10, usewebapi=True, **kwargs):
        taskparameters = {
            'command': 'MoveToCommand',
            'movecommand': movecommand,
            'toinitial': toinitial,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout, usewebapi=usewebapi)

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

    def PlotGraph(self, programname, updatestamp, ikparams=None, highlight=-1, maniptrajectories=None, deltatime=None, usewebapi=False, timeout=10, fireandforget=True):
        taskparameters = {
            'command': 'PlotGraph',
            'programname': programname,
            'updatestamp': int(updatestamp),
        }
        if ikparams is not None:
            taskparameters['ikparams'] = ikparams
            taskparameters['highlight'] = highlight
        if maniptrajectories is not None:
            taskparameters['maniptrajectories'] = maniptrajectories
        if deltatime is not None:
            taskparameters['deltatime'] = float(deltatime)

        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def ExecuteTrajectory(self, trajectories, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, cycles=1, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'ExecuteTrajectory',
            'trajectories': trajectories,
            'cycles': cycles,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
