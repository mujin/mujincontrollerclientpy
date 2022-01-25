# -*- coding: utf-8 -*-
# Copyright (C) 2022 MUJIN Inc.
# Mujin controller client for visualization task

from . import realtimerobotclient

# logging
import logging
log = logging.getLogger(__name__)

class VisualizationClient(realtimerobotclient.RealtimeRobotControllerClient):
    """Mujin controller client for visualization tasks
    """
    tasktype = 'visualization'

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
        :param usewebapi: Whether to use webapi for controller commands
        :param robotaccelmult: Optional multiplier for forcing the acceleration
        """
        super(VisualizationClient, self).__init__(tasktype=self.tasktype, **kwargs)

    def SetVisualizationState(self, visualizationState, timeout=10, fireandforget=False, **kwargs):
        # type: (dict, int, bool, dict) -> dict | None
        taskparameters = {
            'command': 'SetVisualizationState',
            'visualizationState': visualizationState,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=False, timeout=timeout, fireandforget=fireandforget)

    def ComputeRobotConfigsForGraspVisualization(self, targetname, graspname, robotname=None, toolname=None, unit='mm', usewebapi=False, timeout=10, **kwargs):
        """Returns robot configs for grasp visualization

        Args:
            targetname (str):
            graspname (str):
            robotname (str, optional): Name of the robot
            toolname (str, optional): Name of the manipulator. Default: self.toolname
            unit (str, optional):  (Default: 'mm')
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {
            'command': 'ComputeRobotConfigsForGraspVisualization',
            'targetname': targetname,
            'graspname': graspname
        }
        if unit is not None:
            taskparameters['unit'] = unit
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, toolname=toolname, usewebapi=usewebapi, timeout=timeout)

    def GetTranslationForShadowTarget(self, ikparammeta=None, uri=None, localTargetDir=None, timeout=10, **kwargs):
        taskparameters = {
            'command': 'GetTranslationForShadowTarget',
            'uri': uri,
            'ikparammeta': ikparammeta,
        }
        if localTargetDir:
            taskparameters['localTargetDir'] = localTargetDir
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=False, timeout=timeout)

    #SetCameraTransforms, SetViewerParameters inherited from PlanningControllerClient

    #
    # From binpickingui yet
    #

    def ClearPackingStateVisualization(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """
        Clear packing visualization
        """
        taskparameters = {
            'command': 'ClearPackingStateVisualization',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def VisualizePackFormationResult(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """stops the packing computation thread thread started with StartPackFormationComputationThread
        :param initializeCameraPosition: bool. reset camera position
        """
        taskparameters = {
            'command': 'VisualizePackFormationResult',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
