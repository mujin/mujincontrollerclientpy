# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

from . import controllerclientbase, viewermixin, jogmixin

class RealtimeRobotControllerClient(controllerclientbase.ControllerClientBase, viewermixin.ViewerMixin, jogmixin.JogMixin):

    _robotControllerUri = None  # URI of the robot controller, e.g. tcp://192.168.13.201:7000?densowavearmgroup=5
    _robotDeviceIOUri = None  # the device io uri (usually PLC used in the robot bridge)
    _robotname = None # name of the robot

    def __init__(self, robotControllerUri, robotDeviceIOUri, robotname, **kwargs):
        super(RealtimeRobotControllerClient, self).__init__(**kwargs)
        # robot controller
        self._robotControllerUri = robotControllerUri
        self._robotDeviceIOUri = robotDeviceIOUri
        self._robotname = robotname

    def GetRobotControllerUri(self):
        return self._robotControllerUri
        
    def GetRobotDeviceIOUri(self):
        return self._robotDeviceIOUri

    def ExecuteCommand(self, taskparameters, usewebapi=None, timeout=10, fireandforget=False):
        """wrapper to ExecuteCommand with robot info set up in taskparameters

        executes a command on the task.

        :return: a dictionary that contains:
        - robottype: robot type,string
        - currentjointvalues: current joint values, DOF floats
        - elapsedtime: elapsed time in seconds, float
        - numpoints: the number of points, int
        - error: optional error info, dictionary
          - desc: error message, string
          - type: error type, string
          - errorcode: error code, string
        """
        robotname = self._robotname
        taskparameters['robot'] = robotname
        taskparameters['robotControllerUri'] = self._robotControllerUri
        taskparameters['robotDeviceIOUri'] = self._robotDeviceIOUri
        return super(RealtimeRobotControllerClient, self).ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def SaveScene(self, timeout=10, **kwargs):
        """saves the current scene to file
        :param filename: e.g. /tmp/testscene.mujin.dae, if not specified, it will be saved with an auto-generated filename
        :param preserveexternalrefs: If True, any bodies currently that are being externally referenced from the environment will be saved as external references.
        :param externalref: If '*', then will save each of the objects as externally referencing their original filename. Otherwise will force saving specific bodies as external references
        :param saveclone: If 1, will save the scenes for all the cloned environments
        :return: the actual filename the scene is saved to in a json dictionary, e.g. {'filename': '2013-11-01-17-10-00-UTC.dae'}
        """
        taskparameters = {'command': 'SaveScene'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def MoveJoints(self, jointvalues, jointindices=None, robotspeed=None, robotaccelmult=None, toolname=None, execute=1, startvalues=None, envclearance=15, timeout=10, usewebapi=True, **kwargs):
        """moves the robot to desired joint angles specified in jointvalues
        :param jointvalues: list of joint values
        :param jointindices: list of corresponding joint indices, default is range(len(jointvalues))
        :param robotspeed: value in [0,1] of the percentage of robot speed to move at
        :param envclearance: environment clearance in milimeter
        """
        if jointindices is None:
            jointindices = range(len(jointvalues))
            log.warn(u'no jointindices specified, moving joints with default jointindices: %s', jointindices)
        taskparameters = {
            'command': 'MoveJoints',
            'goaljoints': list(jointvalues),
            'jointindices': list(jointindices),
            'envclearance': envclearance,
            'execute': execute,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        if toolname is not None:
            taskparameters['toolname'] = toolname
        if startvalues is not None:
            taskparameters['startvalues'] = list(startvalues)
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)
