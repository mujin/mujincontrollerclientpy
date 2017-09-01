# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

import copy

from . import planningclient

import logging
log = logging.getLogger(__name__)

class RealtimeRobotControllerClient(planningclient.PlanningControllerClient):
    """mujin controller client for realtimerobot task
    """
    _robotname = None # optional name of the robot selected
    _robots = None # a dict of robot params
    _robotspeed = None # speed of the robot, e.g. 0.4
    _robotaccelmult = None # current robot accel mult
    _envclearance = None # environment clearance in milimeter, e.g. 20

    def __init__(self, robotname, robots, robotspeed=None, robotaccelmult=None, envclearance=10.0, **kwargs):
        """
        :param robotspeed: speed of the robot, e.g. 0.4
        :param envclearance: environment clearance in milimeter, e.g. 20
        """
        super(RealtimeRobotControllerClient, self).__init__(**kwargs)
        self._robotname = robotname
        self._robots = robots
        self._robotspeed = robotspeed
        self._robotaccelmult = robotaccelmult
        self._envclearance = envclearance
        
    def GetRobotName(self):
        return self._robotname

    def SetRobotName(self, robotname):
        self._robotname = robotname
    
    def GetRobots(self):
        return self._robots
    
    def SetRobots(self, robots):
        self._robots = robots
    
    def GetRobotControllerUri(self):
        robots = self._robots or {}
        return robots.get(self._robotname, {}).get('robotControllerUri', '')

    def GetRobotDeviceIOUri(self):
        robots = self._robots or {}
        return robots.get(self._robotname, {}).get('robotDeviceIOUri', '')
    
    def IsRobotControllerConfigured(self):
        return len(self.GetRobotControllerUri()) > 0
    
    def IsRobotDeviceIOConfigured(self):
        return len(self.GetRobotDeviceIOUri()) > 0
    
    def SetRobotSpeed(self, robotspeed):
        self._robotspeed = robotspeed

    def SetRobotAccelMult(self, robotaccelmult):
        self._robotaccelmult = robotaccelmult
    
    def ExecuteCommand(self, taskparameters, robotname=None, toolname=None, robots=None, robotspeed=None, robotaccelmult=None, envclearance=None, usewebapi=None, timeout=10, fireandforget=False):
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
        if robots is None:
            robots = self._robots

        # caller wants to use a different tool
        if toolname is not None:
            if robots is not None:
                robots = copy.deepcopy(robots)
                if robotname not in robots:
                    robots[robotname] = {}
                robots[robotname]['toolname'] = toolname
            else:
                # set at the first level
                taskparameters['toolname'] = toolname
        
        if robots is not None:
            taskparameters['robots'] = robots
        if robots is None or robotname in robots:
            taskparameters['robotname'] = robotname

        log.verbose('robotname = %r, robots = %r', robotname, robots)
        
        if 'robotspeed' not in taskparameters:
            if robotspeed is None:
                robotspeed = self._robotspeed
            if robotspeed is not None:
                taskparameters['robotspeed'] = robotspeed

        if 'robotaccelmult' not in taskparameters:
            if robotaccelmult is None:
                robotaccelmult = self._robotaccelmult
            if robotaccelmult is not None:
                taskparameters['robotaccelmult'] = robotaccelmult
        
        if 'envclearance' not in taskparameters or taskparameters['envclearance'] is None:
            if envclearance is None:
                envclearance = self._envclearance
            if envclearance is not None:
                taskparameters['envclearance'] = envclearance

        return super(RealtimeRobotControllerClient, self).ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def ExecuteTrajectory(self, trajectoryxml, robotspeed=None, timeout=10, **kwargs):
        """Executes a trajectory on the robot from a serialized Mujin Trajectory XML file.
        """
        taskparameters = {'command': 'ExecuteTrajectory',
                          'trajectory': trajectoryxml,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)
    
    def GetJointValues(self, timeout=10, **kwargs):
        """gets the current robot joint values
        :return: current joint values in a json dictionary with
        - currentjointvalues: [0,0,0,0,0,0]
        """
        taskparameters = {'command': 'GetJointValues'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def MoveToolLinear(self, goaltype, goals, toolname=None, timeout=10, robotspeed=None, **kwargs):
        """moves the tool linear
        :param goaltype: type of the goal, e.g. translationdirection5d
        :param goals: flat list of goals, e.g. two 5d ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]
        :param toolname: name of the manipulator, default is self.toolname
        
        :param maxdeviationangle: how much the tool tip can rotationally deviate from the linear path
        :param plannername:
        
        :param workspeed: [anglespeed, transspeed] in deg/s and mm/s
        :param workaccel: [angleaccel, transaccel] in deg/s^2 and mm/s^2
        :param worksteplength: discretization for planning MoveHandStraight, in seconds.
        :param workminimumcompletetime: set to trajduration - 0.016s. EMU_MUJIN example requires at least this much
        :param workminimumcompleteratio: in case the duration of the trajectory is now known, can specify in terms of [0,1]. 1 is complete everything
        :param numspeedcandidates: if speed/accel are not specified, the number of candiates to consider
        :param workignorefirstcollisionee: time, necessary in case initial is in collision, has to be multiples of step length?
        :param workignorelastcollisionee: time, necessary in case goal is in collision, has to be multiples of step length?
        :param workignorefirstcollision:

        """
        taskparameters = {'command': 'MoveToolLinear',
                          'goaltype': goaltype,
                          'goals': goals,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotspeed=robotspeed, toolname=toolname, timeout=timeout)
    
    def MoveToHandPosition(self, goaltype, goals, toolname=None, envclearance=None, closegripper=0, robotspeed=None, robotaccelmult=None, timeout=10, **kwargs):
        """Computes the inverse kinematics and moves the manipulator to any one of the goals specified.
        :param goaltype: type of the goal, e.g. translationdirection5d
        :param goals: flat list of goals, e.g. two 5d ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]
        :param toolname: name of the manipulator, default is self.toolname
        :param envclearance: clearance in milimeter, default is self.envclearance
        :param closegripper: whether to close gripper once the goal is reached, default is 0
        """
        taskparameters = {'command': 'MoveToHandPosition',
                          'goaltype': goaltype,
                          'goals': goals,
                          'closegripper': closegripper,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotspeed=robotspeed, robotaccelmult=robotaccelmult, envclearance=envclearance, toolname=toolname, timeout=timeout)
    
    def UpdateObjects(self, envstate, targetname=None, state=None, unit="mm", timeout=10, **kwargs):
        """updates objects in the scene with the envstate
        :param envstate: a list of dictionaries for each instance object in world frame. quaternion is specified in w,x,y,z order. e.g. [{'name': 'target_0', 'translation_': [1,2,3], 'quat_': [1,0,0,0], 'object_uri':'mujin:/asdfas.mujin.dae'}, {'name': 'target_1', 'translation_': [2,2,3], 'quat_': [1,0,0,0]}]
        :param unit: unit of envstate
        """
        taskparameters = {'command': 'UpdateObjects',
                          'envstate': envstate,
                          'unit': unit,
                          }
        if targetname is not None:
            taskparameters['objectname'] = targetname
            taskparameters['object_uri'] = u'mujin:/%s.mujin.dae' % (targetname)
        taskparameters.update(kwargs)
        if state is not None:
            taskparameters['state'] = json.dumps(state)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def Grab(self, targetname, toolname=None, timeout=10, **kwargs):
        """grabs an object with tool
        :param targetname: name of the object
        :param toolname: name of the manipulator, default is self.toolname
        """
        taskparameters = {'command': 'Grab',
                          'targetname': targetname,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout)
    
    def Release(self, targetname, timeout=10, **kwargs):
        """releases an object already grabbed
        :param targetname: name of the object
        """
        taskparameters = {'command': 'Release',
                          'targetname': targetname,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def GetGrabbed(self, timeout=10, **kwargs):
        """gets the names of the grabbed objects
        :return: names of the grabbed object in a json dictionary, e.g. {'names': ['target_0']}
        """
        taskparameters = {'command': 'GetGrabbed',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def GetTransform(self, targetname, unit='mm', timeout=10, **kwargs):
        """gets the transform of an object
        :param targetname: name of the object
        :param unit: unit of the result translation
        :return: transform of the object in a json dictionary, e.g. {'translation': [100,200,300], 'rotationmat': [[1,0,0],[0,1,0],[0,0,1]], 'quaternion': [1,0,0,0]}
        """
        taskparameters = {'command': 'GetTransform',
                          'targetname': targetname,
                          'unit': unit,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def SetTransform(self, targetname, translation, unit='mm', rotationmat=None, quaternion=None, timeout=10, **kwargs):
        """sets the transform of an object
        :param targetname: name of the object
        :param translation: list of x,y,z value of the object in milimeter
        :param unit: unit of translation
        :param rotationmat: list specifying the rotation matrix in row major format, e.g. [1,0,0,0,1,0,0,0,1]
        :param quaternion: list specifying the quaternion in w,x,y,z format, e.g. [1,0,0,0]
        """
        taskparameters = {'command': 'SetTransform',
                          'targetname': targetname,
                          'unit': unit,
                          'translation': translation,
                          }
        taskparameters.update(kwargs)
        if rotationmat is not None:
            taskparameters['rotationmat'] = rotationmat
        if quaternion is not None:
            taskparameters['quaternion'] = quaternion
        if rotationmat is None and quaternion is None:
            taskparameters['quaternion'] = [1, 0, 0, 0]
            log.warn('no rotation is specified, using identity quaternion ', taskparameters['quaternion'])
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def GetOBB(self, targetname, unit='mm', timeout=10, **kwargs):
        """ Get the oriented bounding box of object
        :param targetname: name of the object
        :param unit: unit of the OBB
        :return: OBB of the object
        """
        taskparameters = {'command': 'GetOBB',
                          'targetname': targetname,
                          'unit': unit,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetInnerEmptyRegionOBB(self, targetname, linkname=None, unit='mm', timeout=10, **kwargs):
        """ Get the inner empty oriented bounding box of a container
        :param targetname: name of the object
        :param linkname: can target a specific link
        :param unit: unit of the OBB
        :return: OBB of the object
        """
        taskparameters = {'command': 'GetInnerEmptyRegionOBB',
                          'targetname': targetname,
                          'unit': unit,
                          }
        if linkname is not None:
            taskparameters['linkname'] = unicode(linkname)
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetAABB(self, targetname, unit='mm', timeout=10, **kwargs):
        """Gets the axis aligned bounding box of object
        :param targetname: name of the object
        :param unit: unit of the AABB
        :return: AABB of the object, e.g. {'pos': [1000,400,100], 'extents': [100,200,50]}
        """
        taskparameters = {'command': 'GetAABB',
                          'targetname': targetname,
                          'unit': unit,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def RemoveObjectsWithPrefix(self, prefix=None, prefixes=None, objectPrefixesExpectingFromSlaveTrigger=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """removes objects with prefix
        """
        taskparameters = {'command': 'RemoveObjectsWithPrefix',
                          }
        taskparameters.update(kwargs)
        if prefix is not None:
            taskparameters['prefix'] = unicode(prefix)
        if prefixes is not None:
            taskparameters['prefixes'] = [unicode(prefix) for prefix in prefixes]
        if objectPrefixesExpectingFromSlaveTrigger is not None:
            taskparameters['objectPrefixesExpectingFromSlaveTrigger'] = objectPrefixesExpectingFromSlaveTrigger
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def GetTrajectoryLog(self, timeout=10, **kwargs):
        """Gets the recent trajectories executed on the binpicking server. The internal server keeps trajectories around for 10 minutes before clearing them.

        :param startindex: int, start of the trajectory to get. If negative, will start counting from the end. For example, -1 is the last element, -2 is the second to last element.
        :param num: int, number of trajectories from startindex to return. If 0 will return all the trajectories starting from startindex
        :param includejointvalues: bool, If True will include timedjointvalues, if False will just give back the trajectories. Defautl is False

        :return:

        total: 10
        trajectories: [
        {
        "timestarted": 12345215
        "name": "movingtodest",
        "numpoints": 100,
        "duration": 0.8,
        "timedjointvalues": [0, 0, 0, .....]
        },
        { ... }
        ]

        Where timedjointvalues is a list joint values and the trajectory time. For a 3DOF robot sampled at 0.008s, this is
        [J1, J2, J3, 0, J1, J2, J3, 0.008, J1, J2, J3, 0.016, ...]

        """
        taskparameters = {'command': 'GetTrajectoryLog',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def ChuckGripper(self, robotname=None, timeout=10, usewebapi=None, **kwargs):
        """chucks the manipulator
        :param toolname: name of the manipulator, default is taken from self.robots
        """
        taskparameters = {'command': 'ChuckGripper'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def UnchuckGripper(self, robotname=None, timeout=10, usewebapi=None, **kwargs):
        """unchucks the manipulator and releases the target
        :param toolname: name of the manipulator, default is taken from self.robots
        :param targetname: name of the target
        """
        taskparameters = {'command': 'UnchuckGripper'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def CalibrateGripper(self, robotname=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """goes through the gripper calibration procedure
        """
        taskparameters = {'command': 'CalibrateGripper'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def StopGripper(self, robotname=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        taskparameters = {'command': 'StopGripper'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def MoveGripper(self, grippervalues, robotname=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """chucks the manipulator
        :param toolname: name of the manipulator, default is taken from self.robots
        """
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

    def SaveGripper(self, timeout=10, **kwargs):
        """
        Separate gripper from a robot in a scene and save it.
        :param filename: str. File name to save on the file system. e.g. /tmp/robotgripper/mujin.dae
        :param robotname: str. Name of robot waiting for extracting hand from.
        :param manipname: str. Name of manipulator.
        :param timeout:
        :return:
        """

        taskparameters = {'command': 'SaveGripper'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ResetRobotBridges(self, robots=None, timeout=10, usewebapi=True, **kwargs):
        """resets the robot bridge states
        """
        taskparameters = {
            'command': 'ResetRobotBridges'
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robots=robots, timeout=timeout, usewebapi=usewebapi)
    
    def MoveJoints(self, jointvalues, jointindices=None, robotname=None, robots=None, robotspeed=None, robotaccelmult=None, execute=1, startvalues=None, envclearance=None, timeout=10, usewebapi=True, **kwargs):
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
            'execute': execute,
        }
        if envclearance is not None:
            taskparameters['envclearance'] = envclearance
        
        if startvalues is not None:
            taskparameters['startvalues'] = list(startvalues)

        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, robots=robots, robotspeed=robotspeed, robotaccelmult=robotaccelmult, timeout=timeout, usewebapi=usewebapi)

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

    def ComputeIKFromParameters(self, toolname=None, timeout=10, **kwargs):
        """
        :param toolname: tool name, string
        :param limit: number of solutions to return, int
        :param ikparamnames: the ikparameter names, also contains information about the grasp like the preshape
        :param targetname: the target object name that the ikparamnames belong to
        :param freeincvalue: float, the discretization of the free joints of the robot when computing ik.
        :param filteroptionslist: A list of filter option strings can be: CheckEnvCollisions, IgnoreCustomFilters, IgnoreEndEffectorCollisions, IgnoreEndEffectorEnvCollisions, IgnoreEndEffectorSelfCollisions, IgnoreJointLimits, IgnoreSelfCollisions
        :param filteroptions: OpenRAVE IkFilterOptions bitmask. By default this is 1, which means all collisions are checked, int

        :return: A dictionary of:
        - solutions: array of IK solutions (each of which is an array of DOF values), sorted by minimum travel distance and truncated to match the limit
        """
        taskparameters = {'command': 'ComputeIKFromParameters',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout)

    def StartIPython(self, timeout=1, usewebapi=False, fireandforget=True, **kwargs):
        taskparameters = {'command': 'StartIPython'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def ReloadModule(self, timeout=10, **kwargs):
        taskparameters = {'command': 'ReloadModule'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ResetRobotBridges(self, timeout=10, **kwargs):
        taskparameters = {'command': 'ResetRobotBridges'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ShutdownRobotBridge(self, timeout=10, **kwargs):
        taskparameters = {'command': 'ShutdownRobotBridge'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetRobotBridgeState(self, timeout=10, **kwargs):
        taskparameters = {'command': 'GetRobotBridgeState'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def SetRobotBridgeIOVariables(self, iovalues, timeout=10, usewebapi=None, **kwargs):
        taskparameters = {
            'command': 'SetRobotBridgeIOVariables',
            'iovalues': list(iovalues),
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)
    
    def ClearRobotBridgeError(self, timeout=10, usewebapi=None, **kwargs):
        taskparameters = {
            'command': 'ClearRobotBridgeError',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)

    #
    # jogging related
    #
    def SetJogModeVelocities(self, jogtype, movejointsigns, robotname=None, toolname=None, robotspeed=None, robotaccelmult=None, canJogInCheckMode=None, usewebapi=False, timeout=1, fireandforget=False, **kwargs):
        """
        :param jogtype: One of 'joints', 'world', 'robot', 'tool'
        :param canJogInCheckMode: if true, then allow jogging even if in check mode. By default it is false.
        """
        taskparameters = {
            'command': 'SetJogModeVelocities',
            'jogtype': jogtype,
            'movejointsigns': movejointsigns,
        }
        if canJogInCheckMode is not None:
            taskparameters['canJogInCheckMode'] = canJogInCheckMode
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, toolname=toolname, robotspeed=robotspeed, robotaccelmult=robotaccelmult, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def EndJogMode(self,usewebapi=False, timeout=1, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'EndJogMode',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def SetRobotBridgeServoOn(self, servoon, robotname=None, timeout=3, fireandforget=False):
        taskparameters = {
            'command': 'SetRobotBridgeServoOn',
            'isservoon': servoon
        }
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, fireandforget=fireandforget)

    def SetRobotBridgeControlMode(self, controlMode, timeout=3, fireandforget=False):
        taskparameters = {
            'command': 'SetRobotBridgeControlMode',
            'controlMode': controlMode
        }
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)
    
    def GetDynamicObjects(self, usewebapi=False, timeout=1, **kwargs):
        """Get a list of dynamically added objects in the scene, from vision detection and physics simulation.
        """
        taskparameters = {
            'command': 'GetDynamicObjects',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def ComputeRobotConfigsForGraspVisualization(self, targetname, graspname, robotname=None, toolname=None, unit='mm', usewebapi=False, timeout=10, **kwargs):
        '''returns robot configs for grasp visualization
        '''
        taskparameters = {
            'command': 'ComputeRobotConfigsForGraspVisualization',
            'targetname': targetname,
            'graspname': graspname
        }
        if unit is not None:
            taskparameters['unit'] = unit
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, toolname=toolname, usewebapi=usewebapi, timeout=timeout)
    
    def ResetCacheTemplates(self, usewebapi=False, timeout=1, **kwargs):
        """resets any cached templates
        """
        taskparameters = {
            'command': 'ResetCacheTemplates',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def ResetCacheTemplates(self, usewebapi=False, timeout=1, **kwargs):
        """resets any cached templates
        """
        taskparameters = {
            'command': 'ResetCacheTemplates',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def SetRobotBridgeExternalIOPublishing(self, enable, usewebapi=False, timeout=1, **kwargs):
        """enables publishing collision data to the robotbridge
        """
        taskparameters = {
            'command': 'SetRobotBridgeExternalIOPublishing',
            'enable': bool(enable)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
        
    def SetIgnoreObjectsFromUpdateWithPrefix(self, prefixes, usewebapi=False, timeout=1, **kwargs):
        """enables publishing collision data to the robotbridge
        """
        taskparameters = {
            'command': 'SetIgnoreObjectsFromUpdateWithPrefix',
            'prefixes': prefixes
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
