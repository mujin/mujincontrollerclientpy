# -*- coding: utf-8 -*-
# Copyright (C) 2017 MUJIN Inc.
# Mujin planning client for ITL task (v3)

# mujin imports
from . import realtimerobotplanningclient

# logging
import logging
log = logging.getLogger(__name__)


class RealtimeITL3PlanningClient(realtimerobotplanningclient.RealtimeRobotPlanningClient):
    """Mujin planning client for realtimeitlplanning3 task
    """

    def __init__(self, **kwargs):
        """Logs into the mujin controller, initializes realtimeitlplanning3 task, and sets up parameters

        Args:
            controllerip (str, optional): Ip or hostname of the mujin controller, e.g. controller14 or 172.17.0.2
            controllerurl (str, optional): (Deprecated; use controllerip instead) URL of the mujin controller, e.g. http://controller14.
            controllerusername (str): Username of the mujin controller, e.g. testuser
            controllerpassword (str): Password of the mujin controller
            robotname (str, optional): Name of the robot, e.g. VP-5243I
            scenepk (str, optional): Primary key (pk) of the bin picking task scene, e.g. komatsu_ntc.mujin.dae
            robotspeed (float, optional): Speed of the robot, e.g. 0.4
            regionname (str, optional): Name of the bin, e.g. container1
            targetname (str, optional): Name of the target, e.g. plasticnut-center
            toolname (str, optional): Name of the manipulator, e.g. 2BaseZ
            envclearance (float, optional): Environment clearance in millimeters, e.g. 20
            robotaccelmult (float, optional): Optional multiplier for the robot acceleration.
            taskzmqport (int, optional): Port of the task's zmq server, e.g. 7110
            taskheartbeatport (int, optional): Port of the task's zmq server's heartbeat publisher, e.g. 7111
            taskheartbeattimeout (float, optional): Seconds until reinitializing the task's zmq server if no heartbeat is received, e.g. 7
        """
        super(RealtimeITL3PlanningClient, self).__init__(tasktype='realtimeitlplanning3', **kwargs)

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
            'envclearance': envclearance,
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
