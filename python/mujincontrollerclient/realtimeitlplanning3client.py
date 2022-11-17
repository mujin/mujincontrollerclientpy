# -*- coding: utf-8 -*-
# Copyright (C) 2017 MUJIN Inc.
# Mujin controller client for bin picking task

# mujin imports
from . import realtimerobotclient

# logging
import logging
log = logging.getLogger(__name__)


class RealtimeITLPlanning3ControllerClient(realtimerobotclient.RealtimeRobotControllerClient):
    """Mujin controller client for realtimeitlplanning3 task
    """

    def __init__(self, **kwargs):
        """Logs into the mujin controller, initializes realtimeitlplanning3 task, and sets up parameters
        :param controllerurl: URL of the mujin controller, e.g. http://controller13
        :param controllerusername: Username of the mujin controller, e.g. testuser
        :param controllerpassword: Password of the mujin controller
        :param taskzmqport: Port of the realtimeitlplanning3 task's zmq server, e.g. 7110
        :param taskheartbeatport: Port of the realtimeitlplanning3 task's zmq server's heartbeat publisher, e.g. 7111
        :param taskheartbeattimeout: Seconds until reinitializing realtimeitlplanning3 task's zmq server if no heartbeat is received, e.g. 7
        :param scenepk: Primary key (pk) of the bin picking task scene, e.g. komatsu_ntc.mujin.dae
        :param robotname: Name of the robot, e.g. VP-5243I
        :param robotspeed: Speed of the robot, e.g. 0.4
        :param regionname: Name of the bin, e.g. container1
        :param targetname: Name of the target, e.g. plasticnut-center
        :param toolname: Name of the manipulator, e.g. 2BaseZ
        :param envclearance: Environment clearance in millimeters, e.g. 20
        :param robotaccelmult: Optional multiplier for forcing the acceleration
        """
        super(RealtimeITLPlanning3ControllerClient, self).__init__(tasktype='realtimeitlplanning3', **kwargs)

    def SetJointValues(self, jointvalues, robotname=None, timeout=10, **kwargs):
        taskparameters = {
            'command': 'SetJointValues',
            'jointvalues': jointvalues,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout)

    def GetITLState(self, robotname=None, timeout=10, fireandforget=False, **kwargs):
        taskparameters = {'command': 'GetITLState'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, fireandforget=fireandforget)

    def ExecuteTrajectory(self, identifier, trajectories, statevalues=None, stepping=False, istep=None, cycles=1, restorevalues=None, envclearance=15, robotspeed=None, robotaccelmult=None, timeout=10, fireandforget=False):
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
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def ExecuteTrajectoryStep(self, reverse=False, envclearance=15, robotspeed=None, robotaccelmult=None, timeout=10, fireandforget=False):
        taskparameters = {
            'command': 'ExecuteTrajectoryStep',
            'reverse': reverse,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def PauseExecuteTrajectory(self, timeout=10, fireandforget=False):
        taskparameters = {'command': 'PauseExecuteTrajectory'}
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def ResumeExecuteTrajectory(self, timeout=10, fireandforget=False):
        taskparameters = {'command': 'ResumeExecuteTrajectory'}
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def ComputeRobotConfigsForCommandVisualization(self, executiongraph, commandindex=0, timeout=2, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'ComputeRobotConfigsForCommandVisualization',
            'executiongraph': executiongraph,
            'commandindex': commandindex,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def ComputeRobotJointValuesForCommandVisualization(self, program, commandindex=0, timeout=2, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'ComputeRobotJointValuesForCommandVisualization',
            'program': program,
            'commandindex': commandindex,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def PlotProgramWaypoints(self, timeout=1, fireandforget=True, **kwargs):
        taskparameters = {
            'command': 'PlotProgramWaypoints',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def StartITLProgram(self, programName, robotspeed=None, robotaccelmult=None, timeout=10, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'StartITLProgram',
            'programName': programName,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def StopITLProgram(self, timeout=10, fireandforget=False, **kwargs):
        """stops the itl program
        """
        taskparameters = {
            'command': 'StopITLProgram',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def GenerateExecutionGraph(self, programName, commandTimeout=0.2, totalTimeout=1.0, timeout=10, fireandforget=False, **kwargs):
        """generate list of commands for the itl program
        """
        taskparameters = {
            'command': 'GenerateExecutionGraph',
            'programName': programName,
            'commandTimeout': commandTimeout,
            'totalTimeout': totalTimeout,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def PlotContacts(self, report={}, timeout=1, fireandforget=True, **kwargs):
        taskparameters = {
            'command': 'PlotContacts',
            'report': report
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def PopulateTargetInContainer(self, locationName, populateTargetUri, populateFnName, containerMetaData=None, timeout=20, **kwargs):
        """Populate targets in container using populateFn
        """
        taskparameters = {
            'command': 'PopulateTargetInContainer',
            'locationName': locationName,
            'populateTargetUri': populateTargetUri,
            'populateFnName': populateFnName,
            'containerMetaData': containerMetaData,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
