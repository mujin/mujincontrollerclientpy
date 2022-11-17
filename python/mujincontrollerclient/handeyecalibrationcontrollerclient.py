# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
# Mujin controller client for bin picking task

# System imports

# Mujin imports
from . import planningclient

# Logging
import logging
log = logging.getLogger(__name__)


class HandEyeCalibrationControllerClient(planningclient.PlanningControllerClient):
    """Mujin controller client for the hand-eye calibration task
    """
    tasktype = 'handeyecalibration'

    def __init__(self, robot, **kwargs):
        """Logs into the mujin controller, initializes hand eye calibration task, and sets up parameters
        :param controllerurl: URL of the mujin controller, e.g. http://controller14
        :param controllerusername: Username of the mujin controller, e.g. testuser
        :param controllerpassword: Password of the mujin controller
        :param scenepk: Primary key (pk) of the bin picking task scene, e.g. irex2013.mujin.dae
        """
        super(HandEyeCalibrationControllerClient, self).__init__(tasktype=self.tasktype, **kwargs)
        self.robot = robot

    def ComputeCalibrationPoses(self, cameracontainername, primarysensorname, secondarysensornames, numsamples, calibboardvisibility, calibboardLinkName=None, calibboardGeomName=None, timeout=3000, **kwargs):
        taskparameters = {
            'command': 'ComputeCalibrationPoses',
            'cameracontainername': cameracontainername,
            'primarysensorname': primarysensorname,
            'secondarysensornames': secondarysensornames,
            'numsamples': numsamples,
            'calibboardvisibility': calibboardvisibility,
            'calibboardLinkName': calibboardLinkName,
            'calibboardGeomName': calibboardGeomName,
        }
        taskparameters.update(kwargs)
        if self.robot is not None:
            taskparameters['robot'] = self.robot
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def SampleCalibrationConfiguration(self, cameracontainername, primarysensorname, secondarysensornames, gridindex, calibboardvisibility, calibboardLinkName=None, calibboardGeomName=None, timeout=3000, **kwargs):
        taskparameters = {
            'command': 'SampleCalibrationConfiguration',
            'cameracontainername': cameracontainername,
            'primarysensorname': primarysensorname,
            'secondarysensornames': secondarysensornames,
            'gridindex': gridindex,
            'calibboardvisibility': calibboardvisibility,
            'calibboardLinkName': calibboardLinkName,
            'calibboardGeomName': calibboardGeomName,
        }
        taskparameters.update(kwargs)
        if self.robot is not None:
            taskparameters['robot'] = self.robot
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ReloadModule(self, **kwargs):
        return self.ExecuteCommand({
            'command': 'ReloadModule',
        }, **kwargs)
