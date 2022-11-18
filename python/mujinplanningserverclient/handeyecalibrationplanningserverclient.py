# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
# Mujin controller client for bin picking task

# System imports

# Mujin imports
from . import planningserverclient

# Logging
import logging
log = logging.getLogger(__name__)


class HandEyeCalibrationPlanningServerClient(planningserverclient.PlanningServerClient):
    """Mujin planning server client for the hand-eye calibration task
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
        super(HandEyeCalibrationPlanningServerClient, self).__init__(tasktype=self.tasktype, **kwargs)
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
