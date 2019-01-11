# -*- coding: utf-8 -*-
# Copyright (C) 2017 MUJIN Inc.
# Mujin controller client for bin picking task

# mujin imports
from . import realtimerobotclient
from . import ugettext as _

# logging
import logging
log = logging.getLogger(__name__)


class RealtimeITLPlanning3ControllerClient(realtimerobotclient.RealtimeRobotControllerClient):
    """mujin controller client for realtimeitlplanning3 task
    """

    def __init__(self, **kwargs):

        """logs into the mujin controller, initializes realtimeitlplanning3 task, and sets up parameters
        :param controllerurl: url of the mujin controller, e.g. http://controller13
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        :param taskzmqport: port of the realtimeitlplanning3 task's zmq server, e.g. 7110
        :param taskheartbeatport: port of the realtimeitlplanning3 task's zmq server's heartbeat publisher, e.g. 7111
        :param taskheartbeattimeout: seconds until reinitializing realtimeitlplanning3 task's zmq server if no hearbeat is received, e.g. 7
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
        super(RealtimeITLPlanning3ControllerClient, self).__init__(tasktype='realtimeitlplanning3', **kwargs)

    def SetJointValues(self, jointvalues, robotname=None, timeout=10, usewebapi=True, **kwargs):
        taskparameters = {
            'command': 'SetJointValues',
            'jointvalues': jointvalues,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def GetITLState(self, robotname=None, robots=None, timeout=10, usewebapi=True, fireandforget=False, **kwargs):
        taskparameters = {'command': 'GetITLState'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, robots=robots, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def MoveToCommand(self, program, commandindex=0, envclearance=15, robots=None, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
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
        return self.ExecuteCommand(taskparameters, robots=robots, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def ExecuteTrajectory(self, identifier, trajectories, statevalues=None, stepping=False, istep=None, cycles=1, restorevalues=None, envclearance=15, robots=None, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
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
        return self.ExecuteCommand(taskparameters, robots=robots, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def ExecuteTrajectoryStep(self, reverse=False, envclearance=15, robots=None, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
        taskparameters = {
            'command': 'ExecuteTrajectoryStep',
            'reverse': reverse,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, robots=robots, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def CancelExecuteTrajectoryStep(self, envclearance=15, robots=None, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
        taskparameters = {'command': 'CancelExecuteTrajectoryStep'}
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, robots=robots, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def SetPauseExecuteTrajectory(self, envclearance=15, robots=None, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
        taskparameters = {'command': 'SetPauseExecuteTrajectory'}
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, robots=robots, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def ResumeExecuteTrajectory(self, envclearance=15, robots=None, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False):
        taskparameters = {'command': 'ResumeExecuteTrajectory'}
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, robots=robots, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def ComputeRobotConfigsForCommandVisualization(self, program, commandindex=0, usewebapi=True, timeout=2, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'ComputeRobotConfigsForCommandVisualization',
            'program': program,
            'commandindex': commandindex,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def ComputeRobotJointValuesForCommandVisualization(self, program, commandindex=0, usewebapi=True, timeout=2, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'ComputeRobotJointValuesForCommandVisualization',
            'program': program,
            'commandindex': commandindex,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def PlotProgramWaypoints(self, usewebapi=False, timeout=1, fireandforget=True, **kwargs):
        taskparameters = {
            'command': 'PlotProgramWaypoints',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def StartITLProgram(self, program, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'StartITLProgram',
            'program': program,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def StopITLProgram(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """stops the itl program
        """
        taskparameters = {'command': 'StopITLProgram',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
