# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

from . import controllerclientbase, viewermixin, jogmixin

import logging
log = logging.getLogger(__name__)

class RealtimeRobotControllerClient(controllerclientbase.ControllerClientBase, viewermixin.ViewerMixin, jogmixin.JogMixin):

    _robotname = None # name of the robot selected
    _robots = None # a dict of robot params

    def __init__(self, robotname, robots, **kwargs):
        super(RealtimeRobotControllerClient, self).__init__(**kwargs)
        self._robotname = robotname
        self._robots = robots

    def GetRobotName(self):
        return self._robotname

    def GetRobots(self):
        return self._robots

    def IsRobotControllerConfigured(self):
        robots = self._robots or {}
        return bool(robots.get('robotControllerUri', None))

    def ExecuteCommand(self, taskparameters, robotname=None, toolname=None, useallrobots=False, robots=None, usewebapi=None, timeout=10, fireandforget=False):
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
        if robotname is None:
            robotname = self._robotname
        allrobots = robots or self._robots
        robots = {}
        if useallrobots:
            robots = allrobots
        else:
            robots[robotname] = allrobots[robotname]
            if toolname is not None and len(toolname) > 0:
                robots[robotname]['toolname'] = toolname

        taskparameters['robots'] = robots
        taskparameters['robotname'] = robotname
        log.debug('robotname = %s, robots = %r', robotname, robots)
        return super(RealtimeRobotControllerClient, self).ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def ChuckGripper(self, robotname=None, timeout=10, usewebapi=None, **kwargs):
        taskparameters = {'command': 'ChuckGripper'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def UnchuckGripper(self, robotname=None, timeout=10, usewebapi=None, **kwargs):
        taskparameters = {'command': 'UnchuckGripper'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def CalibrateGripper(self, robotname=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        taskparameters = {'command': 'CalibrateGripper'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def StopGripper(self, robotname=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        taskparameters = {'command': 'StopGripper'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def MoveGripper(self, grippervalues, robotname=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'MoveGripper',
            'grippervalues': grippervalues,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

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

    def MoveJoints(self, jointvalues, jointindices=None, robotname=None, robots=None, robotspeed=None, robotaccelmult=None, execute=1, startvalues=None, envclearance=15, timeout=10, usewebapi=True, **kwargs):
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
        if startvalues is not None:
            taskparameters['startvalues'] = list(startvalues)

        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, robots=robots, timeout=timeout, usewebapi=usewebapi)

    def SetRobotBridgeIOVariables(self, iovalues, robotname=None, timeout=10, usewebapi=None, **kwargs):
        taskparameters = {
            'command': 'SetRobotBridgeIOVariables',
            'iovalues': list(iovalues)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def ComputeIkParamPosition(self, name, robotname=None, timeout=10, usewebapi=None, **kwargs):
        taskparameters = {
            'command': 'ComputeIkParamPosition',
            'name': name,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def StartIPython(self, timeout=1, usewebapi=False, fireandforget=True, **kwargs):
        taskparameters = {'command': 'StartIPython'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
