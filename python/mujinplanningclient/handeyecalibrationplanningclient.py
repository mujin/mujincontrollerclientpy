# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
# Mujin controller client for bin picking task

# System imports

# Mujin imports
from . import planningclient

# Logging
import logging
log = logging.getLogger(__name__)


class HandEyeCalibrationPlanningClient(planningclient.PlanningClient):
    """Mujin planning client for the hand-eye calibration task
    """
    tasktype = 'handeyecalibration'

    def __init__(self, robot, **kwargs):
        """Logs into the mujin controller, initializes hand eye calibration task, and sets up parameters

        Args:
            controllerurl (str): URL of the mujin controller, e.g. http://controller14
            controllerusername (str): Username for the Mujin controller, e.g. testuser
            controllerpassword (str): Password for the Mujin controller
            scenepk (str, optional): Primary key (pk) of the scene, e.g. irex_demo.mujin.dae
        """
        super(HandEyeCalibrationPlanningClient, self).__init__(tasktype=self.tasktype, **kwargs)
        self.robot = robot

    def ComputeCalibrationPoses(self, primarySensorSelectionInfo, secondarySensorSelectionInfos, numsamples, calibboardvisibility, calibboardLinkName=None, calibboardGeomName=None, timeout=3000, gridindex=None, **kwargs):
        """Compute a set of calibration poses that satisfy the angle constraints using latin hypercube sampling (or stratified sampling upon failure)

        Args:
            primarySensorSelectionInfo (dict): Selects the primary camera that everything will be calibrated against.
            secondarySensorSelectionInfos (list[dict]): Selects the secondary camera(s) (assumed to be nearby the primary sensor).
            numsamples (int): Number of samples to take. A reasonable number is often between 5 and 25.
            calibboardvisibility (bool):
            calibboardLinkName (str, optional):
            calibboardGeomName (str, optional):
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 3000)
            gridindex:
        """
        taskparameters = {
            'command': 'ComputeCalibrationPoses',
            'primarySensorSelectionInfo': primarySensorSelectionInfo,
            'secondarySensorSelectionInfos': secondarySensorSelectionInfos,
            'numsamples': numsamples,
            'calibboardvisibility': calibboardvisibility,
        }
        if calibboardLinkName is not None:
            taskparameters['calibboardLinkName'] = calibboardLinkName
        if calibboardGeomName is not None:
            taskparameters['calibboardGeomName'] = calibboardGeomName
        if gridindex is not None:
            taskparameters['gridindex'] = gridindex
        if self.robot is not None:
            taskparameters['robot'] = self.robot
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def SampleCalibrationConfiguration(self, primarySensorSelectionInfo, secondarySensorSelectionInfos, gridindex, calibboardvisibility, calibboardLinkName=None, calibboardGeomName=None, timeout=3000, minPatternTiltAngle=None, maxPatternTiltAngle=None, **kwargs):
        """Sample a valid calibration pose inside the given voxel and find a corresponding IK solution.

        Args:
            primarySensorSelectionInfo (dict): Selects the primary camera that everything will be calibrated against.
            secondarySensorSelectionInfos (list[dict]): Selects the secondary camera(s) (assumed to be nearby the primary sensor).
            gridindex (int): The index of the voxel
            calibboardvisibility (bool):
            calibboardLinkName (str, optional):
            calibboardGeomName (str, optional):
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 3000)
            minPatternTiltAngle (float, optional): The minimum tilt of the pattern in degrees. Default: 10 degrees
            maxPatternTiltAngle (float, optional): The maximum tilt of the pattern in degrees. Default: 30 degrees
        """
        taskparameters = {
            'command': 'SampleCalibrationConfiguration',
            'primarySensorSelectionInfo': primarySensorSelectionInfo,
            'secondarySensorSelectionInfos': secondarySensorSelectionInfos,
            'gridindex': gridindex,
            'calibboardvisibility': calibboardvisibility,
        }
        if calibboardLinkName is not None:
            taskparameters['calibboardLinkName'] = calibboardLinkName
        if calibboardGeomName is not None:
            taskparameters['calibboardGeomName'] = calibboardGeomName
        if minPatternTiltAngle is not None:
            taskparameters['minPatternTiltAngle'] = minPatternTiltAngle
        if maxPatternTiltAngle is not None:
            taskparameters['maxPatternTiltAngle'] = maxPatternTiltAngle
        if self.robot is not None:
            taskparameters['robot'] = self.robot
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ReloadModule(self, **kwargs):
        return self.ExecuteCommand({
            'command': 'ReloadModule',
        }, **kwargs)
