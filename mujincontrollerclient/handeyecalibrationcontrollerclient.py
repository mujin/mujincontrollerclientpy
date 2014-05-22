# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 MUJIN Inc.
# Mujin controller client for bin picking task

# logging
import logging
log = logging.getLogger(__name__)

# system imports

# mujin imports
from . import controllerclientbase

class HandEyeCalibrationControllerClient(controllerclientbase.ControllerClientBase):
    """mujin controller client for hand-eye calibration task
    """
    tasktype = 'handeyecalibration'
    def __init__(self, scenepk, controllerurl, controllerusername, controllerpassword, usewebapi=True):
        """logs into the mujin controller, initializes hand eye calibration task, and sets up parameters
        :param controllerurl: url of the mujin controller, e.g. http://controller14
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        :param scenepk: pk of the bin picking task scene, e.g. irex2013.mujin.dae
        :param usewebapi: whether to use webapi for controller commands
        """
        super(HandEyeCalibrationControllerClient, self).__init__(controllerurl, controllerusername, controllerpassword, None, self.tasktype, scenepk)

        self.usewebapi = usewebapi
        
    def ComputeCalibrationPoses(self,cameraname,numsamples, halconpatternparameters, calibboardvisibility, toolname, targetarea = ""):
        taskparameters = {'command': 'ComputeCalibrationPoses',
                          'cameraname': cameraname,
                          'halconpatternparameters': halconpatternparameters,
                          'patternvisibility': calibboardvisibility,
                          'numsamples': numsamples,
                          'toolname' : toolname,
                          'targetarea': targetarea,
                          'samplingmethod': "boardexposure" #"boardexposure"
                          }
        result = self.ExecuteCommandViaWebapi(taskparameters, webapitimeout=3000)
        return result

    def ComputeStereoCalibrationPoses(self,cameranames,numsamples, halconpatternparameters, calibboardvisibility, toolname, targetarea = "",samplingmethod=""):
        if samplingmethod == "":
            samplingmethod = "boardexposure" #"boardexposure"
        taskparameters = {'command': 'ComputeStereoCalibrationPoses',
                          'cameranames': cameranames,
                          'halconpatternparameters': halconpatternparameters,
                          'patternvisibility': calibboardvisibility,
                          'numsamples': numsamples,
                          'toolname' : toolname,
                          'targetarea': targetarea,
                          'samplingmethod': samplingmethod
                          }
        result = self.ExecuteCommandViaWebapi(taskparameters, webapitimeout=3000)
        return result

