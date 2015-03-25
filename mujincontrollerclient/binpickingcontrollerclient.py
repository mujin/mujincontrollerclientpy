# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
# Mujin controller client for bin picking task
import os

# logging
import logging
log = logging.getLogger(__name__)

# mujin imports
from . import controllerclientbase


class BinpickingControllerClient(controllerclientbase.ControllerClientBase):
    """mujin controller client for bin picking task
    """
    tasktype = 'binpicking'
    sceneparams = {}

    def __init__(self, controllerurl, controllerusername, controllerpassword, robotControllerUri, scenepk, robotname, robotspeed, regionname, targetname, toolname, envclearance, binpickingzmqport=None, binpickingheartbeatport=None, binpickingheartbeattimeout=None, usewebapi=True, initializezmq=False, ctx=None, timeout=None):
        """logs into the mujin controller, initializes binpicking task, and sets up parameters
        :param controllerurl: url of the mujin controller, e.g. http://controller14
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        :param robotControllerUri: URI of the robot controller, e.g. tcp://192.168.13.201:7000?densowavearmgroup=5
        :param binpickingzmqport: port of the binpicking task's zmq server, e.g. 7110
        :param binpickingheartbeatport: port of the binpicking task's zmq server's heartbeat publisher, e.g. 7111
        :param binpickingheartbeattimeout: seconds until reinitializing binpicking task's zmq server if no hearbeat is received, e.g. 7
        :param scenepk: pk of the bin picking task scene, e.g. irex2013.mujin.dae
        :param robotname: name of the robot, e.g. VP-5243I
        :param robotspeed: speed of the robot, e.g. 0.4
        :param regionname: name of the bin, e.g. container1
        :param targetname: name of the target, e.g. plasticnut-center
        :param toolname: name of the manipulator, e.g. 2BaseZ
        :param envclearance: environment clearance in milimeter, e.g. 20
        :param usewebapi: whether to use webapi for controller commands
        """
        super(BinpickingControllerClient, self).__init__(controllerurl, controllerusername, controllerpassword, binpickingzmqport, binpickingheartbeatport, binpickingheartbeattimeout, self.tasktype, scenepk, initializezmq, usewebapi, ctx, timeout)

        # robot controller
        self.robotControllerUri = robotControllerUri

        # bin picking task
        self.robotname = robotname
        self.robotspeed = robotspeed
        self.regionname = regionname
        self.targetname = targetname
        self.toolname = toolname
        self.envclearance = envclearance
        self.SetScenePrimaryKey(scenepk)
        self.controllerusername = controllerusername
        
    def SetScenePrimaryKey(self, scenepk):
        self.scenepk = scenepk
        sceneuri = controllerclientbase.GetURIFromPrimaryKey(scenepk)
        # for now (HACK) need to set the correct scenefilename. newer version of mujin controller need only scenepk, so remove scenefilename eventually
        mujinpath = os.path.join(os.environ.get('MUJIN_MEDIA_ROOT_DIR', '/var/www/media/u'), self.controllerusername)
        scenefilename = controllerclientbase.GetFilenameFromURI(sceneuri, mujinpath)[1]
        self.sceneparams = {'scenetype': 'mujincollada', 'sceneuri':sceneuri, 'scenefilename': scenefilename, 'scale': [1.0, 1.0, 1.0]}  # TODO: set scenetype according to the scene
        
    def ReloadModule(self, timeout=10, **kwargs):
        return self.ExecuteCommand({'command': 'ReloadModule', 'sceneparams': self.sceneparams, 'tasktype': self.tasktype}, timeout=timeout, **kwargs)

    #########################
    # robot commands
    #########################

    def ExecuteRobotCommand(self, taskparameters, robotspeed=None, usewebapi=None, timeout=10):
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
        robotname = self.robotname
        robotControllerUri = self.robotControllerUri
        taskparameters['robot'] = robotname
        taskparameters['robotControllerUri'] = robotControllerUri

        if taskparameters.get('speed', None) is None:
            # taskparameters does not have robotspeed, so set the global speed
            if robotspeed is None:
                taskparameters['robotspeed'] = self.robotspeed
            else:
                taskparameters['robotspeed'] = robotspeed

        return self.ExecuteCommand(taskparameters, usewebapi, timeout=timeout)
    
    def ExecuteTrajectory(self, trajectoryxml, robotspeed=None, timeout=10, **kwargs):
        """Executes a trajectory on the robot from a serialized Mujin Trajectory XML file.
        """
        taskparameters = {'command': 'ExecuteTrajectory',
                          'trajectory': trajectoryxml,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)
    
    def MoveJoints(self, jointvalues, jointindices=None, robotspeed=None, execute=1, startvalues=None, timeout=10, **kwargs):
        """moves the robot to desired joint angles specified in jointvalues
        :param jointvalues: list of joint values
        :param jointindices: list of corresponding joint indices, default is range(len(jointvalues))
        :param robotspeed: value in [0,1] of the percentage of robot speed to move at
        :param envclearance: environment clearance in milimeter
        """
        if jointindices is None:
            jointindices = range(len(jointvalues))
            log.warn('no jointindices specified, moving joints with default jointindices: ', jointindices)
        taskparameters = {'command': 'MoveJoints',
                          'goaljoints': list(jointvalues),
                          'jointindices': list(jointindices),
                          'envclearance': self.envclearance,
                          'execute': execute,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        if startvalues is not None:
            taskparameters['startvalues'] = list(startvalues)
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)

    def UnchuckGripper(self, toolname=None, targetname=None, robotspeed=None, timeout=10):
        """unchucks the manipulator and releases the target
        :param toolname: name of the manipulator, default is self.toolname
        :param targetname: name of the target, default is self.targetname
        """
        if toolname is None:
            toolname = self.toolname
        if targetname is None:
            targetname = self.targetname
        taskparameters = {'command': 'UnchuckGripper',
                          'toolname': toolname,
                          'targetname': targetname,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)

    def ChuckGripper(self, toolname=None, robotspeed=None, timeout=10):
        """chucks the manipulator
        :param toolname: name of the manipulator, default is self.toolname
        """
        if toolname is None:
            toolname = self.toolname
        taskparameters = {'command': 'ChuckGripper',
                          'toolname': toolname,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)

    def GetJointValues(self, timeout=10, **kwargs):
        """gets the current robot joint values
        :return: current joint values in a json dictionary with
        - currentjointvalues: [0,0,0,0,0,0]
        """
        taskparameters = {'command': 'GetJointValues',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def GetManipulatorTransformInRobotFrame(self, timeout=10):
        """gets the transform of the manipulator in robot frame
        :return: current transform of the manipulator in robot frame in a json dictionary, e.g. {'translation': [100,200,300], 'rotationmat': [[1,0,0],[0,1,0],[0,0,1]], 'quaternion': [1,0,0,0]}
        """
        taskparameters = {'command': 'GetManipTransformToRobot',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def PickAndPlace(self, goaltype, goals, targetnamepattern=None, approachoffset=30, departoffsetdir=[0, 0, 50], destdepartoffsetdir=[0, 0, 30], deletetarget=0, debuglevel=4, movetodestination=1, freeinc=[0.08], worksteplength=None, densowavearmgroup=5, regionname=None, cameranames=None, envclearance=15, toolname=None, robotspeed=0.5, timeout=1000, **kwargs):
        """picks up an object with the targetnamepattern and places it down at one of the goals. First computes the entire plan from robot moving to a grasp and then moving to its destination, then runs it on the real robot. Task finishes once the real robot is at the destination.

        :param desttargetname: The destination target name where the destination goal ikparams come from
        :param destikparamnames: A list of lists of ikparam names for the destinations of the target. Only destikparamnames[0] is looked at and tells the system to place the part in any of the ikparams in destikparamnames[0]

        :param targetnamepattern: regular expression describing the name of the object, default is '%s_\d+'%(self.targetname). See https://docs.python.org/2/library/re.html
        :param approachoffset: distance in milimeter to move straight to the grasp point, e.g. 30 mm
        :param departoffsetdir: the direction and distance in mm to move the part in global frame (usually along negative gravity) after it is grasped, e.g. [0,0,50]
        :param destdepartoffsetdir: the direction and distance in mm to move away from the object after it is placed, e.g. [0,0,30]. Depending on leaveoffsetintool parameter, this can in the global coordinate system or tool coordinate system.
        :param leaveoffsetintool: If 1, destdepartoffsetdir is in the tool coordinate system. If 0, destdepartoffsetdir is in the global coordinate system. By default this is 0.
        :param deletetarget: whether to delete target after pick and place is done
        :param toolname: name of the manipulator
        :param regionname: name of the region of the objects
        :param cameranames: the names of the cameras to avoid occlusions with the robot, list of strings
        :param envclearance: environment clearance in milimeter

        Low level planning parameters:
        :param debuglevel: sets debug level of the task
        :param movetodestination: planning parameter
        :param freeinc: planning parameter
        :param worksteplength: planning parameter
        :param densowavearmgroup: planning parameter
        :param graspsetname: the name of the grasp set belong to the target objects to use for the target. Grasp sets are a list of ikparams

        Manual Destination Specification (deprecated)
        :param goaltype: type of the goal, e.g. translationdirection5d or transform6d
        :param goals: flat list of goals, e.g. two 5d ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]
        """
        if worksteplength is None:
            worksteplength = 0.01
        if toolname is None:
            toolname = self.toolname
        if targetnamepattern is None:
            targetnamepattern = '%s_\d+' % (self.targetname)
        if regionname is None:
            regionname = self.regionname
        if robotspeed is None:
            robotspeed = self.robotspeed
        taskparameters = {'command': 'PickAndPlace',
                          'toolname': toolname,
                          'goaltype': goaltype,
                          'envclearance': envclearance,
                          'movetodestination': movetodestination,
                          'goals': goals,
                          'approachoffset': approachoffset,
                          'departoffsetdir': departoffsetdir,
                          'destdepartoffsetdir': destdepartoffsetdir,
                          'freeinc': freeinc,
                          'worksteplength': worksteplength,
                          'targetnamepattern': targetnamepattern,
                          'containername': regionname,
                          'deletetarget': deletetarget,
                          'robotspeed': robotspeed,
                          'debuglevel': debuglevel,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)

    def StartPickAndPlaceThread(self, goaltype=None, goals=None, targetnamepattern=None, approachoffset=30, departoffsetdir=[0, 0, 50], destdepartoffsetdir=[0, 0, 30], deletetarget=0, debuglevel=4, movetodestination=1, worksteplength=None, regionname=None, envclearance=15, toolname=None, robotspeed=None, timeout=10, **kwargs):
        """Start a background loop to continuously pick up objects with the targetnamepattern and place them down at the goals. The loop will check new objects arriving in and move the robot as soon as it finds a feasible grasp. The thread can be quit with StopPickPlaceThread.

        :param desttargetname: The destination target name where the destination goal ikparams come from
        :param destikparamnames: A list of lists of ikparam names for the ordered destinations of the target. destikparamnames[0] is where the first picked up part goes, desttargetname[1] is where the second picked up target goes.
        :param cycledests: When finished cycling through all destikparamnames, will delete all the targets and start from the first index again doing this for cycledests times. By default it is 1.

        :param targetnamepattern: regular expression describing the name of the object, default is '%s_\d+'%(self.targetname). See https://docs.python.org/2/library/re.html
        :param approachoffset: distance in milimeter to move straight to the grasp point, e.g. 30 mm
        :param departoffsetdir: the direction and distance in mm to move the part in global frame (usually along negative gravity) after it is grasped, e.g. [0,0,50]
        :param destdepartoffsetdir: the direction and distance in mm to move away from the object after it is placed, e.g. [0,0,30]. Depending on leaveoffsetintool parameter, this can in the global coordinate system or tool coordinate system.
        :param leaveoffsetintool: If 1, destdepartoffsetdir is in the tool coordinate system. If 0, destdepartoffsetdir is in the global coordinate system. By default this is 0.
        :param deletetarget: whether to delete target after pick and place is done
        :param toolname: name of the manipulator
        :param regionname: name of the region of the objects
        :param cameranames: the names of the cameras to avoid occlusions with the robot, list of strings
        :param envclearance: environment clearance in milimeter
        Low level planning parameters:
        :param debuglevel: sets debug level of the task
        :param movetodestination: planning parameter
        :param worksteplength: planning parameter
        :param densowavearmgroup: robot parameters
        :param graspsetname: the name of the grasp set belong to the target objects to use for the target. Grasp sets are a list of ikparams

        :param goaltype: type of the goal, e.g. translationdirection5d
        :param goals: flat list of goals, e.g. two 5d ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]

        :param useworkspaceplanner: If 1 is set, will try the workspace planner for moving the hand straight. If 2 is set, will try the RRT for moving straight. Can set 3 for trying both.
        """
        if worksteplength is None:
            worksteplength = 0.01
        if toolname is None:
            toolname = self.toolname
        if targetnamepattern is None:
            targetnamepattern = '%s_\d+' % (self.targetname)
        if regionname is None:
            regionname = self.regionname
        if robotspeed is None:
            robotspeed = self.robotspeed
        taskparameters = {'command': 'StartPickAndPlaceThread',
                          'toolname': toolname,
                          'envclearance': envclearance,
                          'movetodestination': movetodestination,
                          'approachoffset': approachoffset,
                          'departoffsetdir': departoffsetdir,
                          'destdepartoffsetdir': destdepartoffsetdir,
                          'worksteplength': worksteplength,
                          'targetnamepattern': targetnamepattern,
                          'containername': regionname,
                          'deletetarget': deletetarget,
                          'robotspeed': robotspeed,
                          'debuglevel': debuglevel,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        if goals is not None:
            taskparameters['orderedgoals'] = goals
            taskparameters['goaltype'] = goaltype
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)

    def StopPickPlaceThread(self, timeout=10, **kwargs):
        """stops the pick and place thread started with StartPickAndPlaceThread
        """
        taskparameters = {'command': 'StopPickPlaceThread',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype}
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def GetPickPlaceStatus(self, timeout=10, **kwargs):
        """gets the status of the pick and place thread
        :return: status (0: not running, 1: no error, 2: error) of the pick and place thread in a json dictionary, e.g. {'status': 2, 'error': 'an error happened'}
        """
        taskparameters = {'command': 'GetPickPlaceStatus',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def MoveToHandPosition(self, goaltype, goals, toolname=None, envclearance=None, closegripper=0, robotspeed=None, timeout=10):
        """Computes the inverse kinematics and moves the manipulator to any one of the goals specified.
        :param goaltype: type of the goal, e.g. translationdirection5d
        :param goals: flat list of goals, e.g. two 5d ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]
        :param toolname: name of the manipulator, default is self.toolname
        :param envclearance: clearance in milimeter, default is self.envclearance
        :param closegripper: whether to close gripper once the goal is reached, default is 0
        """
        if toolname is None:
            toolname = self.toolname
        if envclearance is None:
            envclearance = self.envclearance
        taskparameters = {'command': 'MoveToHandPosition',
                          'goaltype': goaltype,
                          'goals': goals,
                          'toolname': toolname,
                          'envclearance': envclearance,
                          'closegripper': closegripper,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)

    def ComputeIK(self, timeout=10, **kwargs):
        """
        :param toolname: tool name, string
        :param limit: number of solutions to return, int
        :param iktype: grasp (but basically the just the ikparam), string
        :param quaternion: grasp (but basically the just the ikparam) quaternion in world cooordinates, float array
        :param translation: grasp (but basically the just the ikparam) translation in world cooordinates in mm, float array
        :param direction: grasp (but basically the just the ikparam) direction in world cooordinates, float array
        :param angle: grasp (but basically the just the ikparam) angle in world cooordinates, float
        :param freeincvalue: float, the discretization of the free joints of the robot when computing ik.
        :param filteroptions: OpenRAVE IkFilterOptions bitmask. By default this is 1, which means all collisions are checked, int
        :param preshape: If the tool has fingers after the end effector, specify their values. The gripper DOFs come from **gripper_dof_pks** field from the tool., float array

        :return: A dictionary of:
        - solutions: array of IK solutions (each of which is an array of DOF values), sorted by minimum travel distance and truncated to match the limit
        """
        taskparameters = {'command': 'ComputeIK',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        if 'toolname' not in taskparameters:
            taskparameters['toolname'] = self.toolname
        if 'envclearance' not in taskparameters:
            taskparameters['envclearance'] = self.envclearance
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def ComputeIKFromParameters(self, timeout=10, **kwargs):
        """
        :param toolname: tool name, string
        :param limit: number of solutions to return, int
        :param ikparamnames: the ikparameter names, also contains information about the grasp like the preshape
        :param targetname: the target object name that the ikparamnames belong to
        :param freeincvalue: float, the discretization of the free joints of the robot when computing ik.
        :param filteroptions: OpenRAVE IkFilterOptions bitmask. By default this is 1, which means all collisions are checked, int

        :return: A dictionary of:
        - solutions: array of IK solutions (each of which is an array of DOF values), sorted by minimum travel distance and truncated to match the limit
        """
        taskparameters = {'command': 'ComputeIKFromParameters',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        if 'toolname' not in taskparameters:
            taskparameters['toolname'] = self.toolname
        if 'envclearance' not in taskparameters:
            taskparameters['envclearance'] = self.envclearance
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def InitializePartsWithPhysics(self, timeout=10, **kwargs):
        """Start a physics simulation where the parts drop down into the bin. The method returns as soon as the physics is initialized, user has to wait for the "duration" or call StopPhysicsThread command.
        :param targeturi: the target uri to initialize the scene with
        :param numtargets: the number of targets to create
        :param regionname: the container name to drop the targets into
        :param duration: the duration in seconds to continue the physics until it is stopped.
        :param basename: The basename to give to all the new target names. Numbers are suffixed at the end, like basename+'0134'. If not specified, will use a basename derived from the targeturi.
        :param deleteprevious: if True, will delete all the previous targets in the scene. By default this is True.
        """
        taskparameters = {'command': 'InitializePartsWithPhysics',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        if 'containername' not in taskparameters:
            taskparameters['containername'] = self.regionname
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def StopPhysicsThread(self, timeout=10, **kwargs):
        """stops the physics simulation started with InitializePartsWithPhysics
        """
        taskparameters = {'command': 'StopPhysicsThread',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def JitterPartUntilValidGrasp(self, timeout=10, **kwargs):
        """Select a part that wasn't able to be grasped and jitter its location such that a grasp set is found for it that will take it to the destination.

        :param toolname: name of the manipulator
        :param targetname: The target to try to grasp.
        :param graspsetname: the name of the grasp set belong to the target objects to use for the target. Grasp sets are a list of ikparams.
        :param approachoffset: The approach distance for simulating full grasp.
        :param departoffsetdir: The depart distance for simulating full grasp.
        :param destdepartoffsetdir: the direction and distance in mm to move away from the object after it is placed, e.g. [0,0,30]. Depending on leaveoffsetintool parameter, this can in the global coordinate system or tool coordinate system.
        :param leaveoffsetintool: If 1, destdepartoffsetdir is in the tool coordinate system. If 0, destdepartoffsetdir is in the global coordinate system. By default this is 0.
        :param desttargetname: The destination target name where the destination goal ikparams come from. If no name is specified, then robot won't consider putting the target into the destination when it searches for grasps.
        :param destikparamnames: A list of lists of ikparam names for the ordered destinations of the target. destikparamnames[0] is where the first picked up part goes, desttargetname[1] is where the second picked up target goes.
        :param jitterdist: Amount to jitter the target object translation by
        :param jitterangle: Amount to jitter the target object's orientation angle
        :param jitteriters: Number of times to try jittering before giving up.

        :return: If failed, an empty dictionary. If succeeded, a dictionary with the following keys:
          - translation: the new translation of the target part
          - quaternion: the new quaternion of the target part
          - jointvalues: robot joint values that are grasping the part (fingers are at their preshape).
          - graspname: the grasp name used for jointvalues. If empty, then no grasp was found.
          - destikname: the name of the destination ikparam that was chosen with the grasp
          - destjointvalues: robot joint values at one of the specified destinations (fingers are at their final positions).
          - desttranslation: the new translation of the target part
          - destquaternion: the new quaternion of the target part
        """
        taskparameters = {'command': 'JitterPartUntilValidGrasp',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype}
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    ####################
    # scene commands
    ####################

    def IsRobotOccludingBody(self, bodyname, cameraname, timeout=10):
        """returns if the robot is occluding body in the view of the specified camera
        :param bodyname: name of the object
        :param cameraname: name of the camera
        :return: the occlusion state in a json dictionary, e.g. {'occluded': 0}
        """
        taskparameters = {'command': 'IsRobotOccludingBody',
                          'robotname': self.robotname,
                          'bodyname': bodyname,
                          'cameraname': cameraname,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetPickedPositions(self, unit='m', timeout=10):
        """returns the poses and the timestamps of the picked objects
        :param robotname: name of the robot
        :param unit: unit of the translation
        :return: the positions and the timestamps of the picked objects in a json dictionary, info of each object has the format of quaternion (w,x,y,z) followed by x,y,z translation (in mm) followed by timestamp in milisecond e.g. {'positions': [[1,0,0,0,100,200,300,1389774818.8366449],[1,0,0,0,200,200,300,1389774828.8366449]]}
        """
        taskparameters = {'command': 'GetPickedPositions',
                          'robotname': self.robotname,
                          'unit': unit,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def UpdateObjects(self, envstate, targetname=None, unit="m", timeout=10):
        """updates objects in the scene with the envstate
        :param envstate: a list of dictionaries for each instance object in world frame. quaternion is specified in w,x,y,z order. e.g. [{'name': 'target_0', 'translation_': [1,2,3], 'quat_': [1,0,0,0]}, {'name': 'target_1', 'translation_': [2,2,3], 'quat_': [1,0,0,0]}]
        :param unit: unit of envstate
        """
        if targetname is None:
            targetname = self.targetname
        taskparameters = {'command': 'UpdateObjects',
                          'objectname': targetname,
                          'object_uri': u'mujin:/%s.mujin.dae' % (targetname),
                          'robot': self.robotname,
                          'envstate': envstate,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          'unit': unit,
                          }
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def Grab(self, targetname, toolname=None, timeout=10):
        """grabs an object with tool
        :param targetname: name of the object
        :param robotname: name of the robot
        :param toolname: name of the manipulator, default is self.toolname
        """
        if toolname is None:
            toolname = self.toolname
        taskparameters = {'command': 'Grab',
                          'targetname': targetname,
                          'robotname': self.robotname,
                          'toolname': toolname,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetGrabbed(self, timeout=10):
        """gets the names of the grabbed objects
        :return: names of the grabbed object in a json dictionary, e.g. {'names': ['target_0']}
        """
        taskparameters = {'command': 'GetGrabbed',
                          'robotname': self.robotname,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetTransform(self, targetname, unit='mm', timeout=10):
        """gets the transform of an object
        :param targetname: name of the object
        :param unit: unit of the result translation
        :return: transform of the object in a json dictionary, e.g. {'translation': [100,200,300], 'rotationmat': [[1,0,0],[0,1,0],[0,0,1]], 'quaternion': [1,0,0,0]}
        """
        taskparameters = {'command': 'GetTransform',
                          'targetname': targetname,
                          'unit': unit,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def SetTransform(self, targetname, translation, unit='mm', rotationmat=None, quaternion=None, timeout=10):
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
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        if rotationmat is not None:
            taskparameters['rotationmat'] = rotationmat
        if quaternion is not None:
            taskparameters['quaternion'] = quaternion
        if rotationmat is None and quaternion is None:
            taskparameters['quaternion'] = [1, 0, 0, 0]
            log.warn('no rotation is specified, using identity quaternion ', taskparameters['quaternion'])
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetAABB(self, targetname, unit='mm', timeout=10):
        """Gets the axis aligned bounding box of object
        :param targetname: name of the object
        :param unit: unit of the AABB
        :return: AABB of the object, e.g. {'pos': [1000,400,100], 'extents': [100,200,50]}
        """
        taskparameters = {'command': 'GetAABB',
                          'targetname': targetname,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          'unit': unit,
                          }
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def RemoveObjectsWithPrefix(self, prefix, timeout=10):
        """removes objects with prefix
        """
        taskparameters = {'command': 'RemoveObjectsWithPrefix',
                          'prefix': prefix,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def SaveScene(self, timeout=10, **kwargs):
        """saves the current scene to file
        :param filename: e.g. /tmp/testscene.mujin.dae, if not specified, it will be saved with an auto-generated filename
        :param preserveexternalrefs: If True, any bodies currently that are being externally referenced from the environment will be saved as external references.
        :param externalref: If '*', then will save each of the objects as externally referencing their original filename. Otherwise will force saving specific bodies as external references
        :param saveclone: If 1, will save the scenes for all the cloned environments
        :return: the actual filename the scene is saved to in a json dictionary, e.g. {'filename': '2013-11-01-17-10-00-UTC.dae'}
        """
        taskparameters = {'command': 'SaveScene',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

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
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetPickAndPlaceLog(self, timeout=10, **kwargs):
        """Gets the recent pick-and-place log executed on the binpicking server. The internal server keeps the log around until the next Pick-and-place command is executed.

        :param startindex: int, start of the trajectory to get. If negative, will start counting from the end. For example, -1 is the last element, -2 is the second to last element.
        :param num: int, number of trajectories from startindex to return. If 0 will return all the trajectories starting from startindex

        :return:

        total: 10
        messages: [
        {
          "message":"message1",
          "type":"",
          "level":0,
          "data": {
             "jointvalues":[0,0,0,0,0,0]
           }
        },
        ]

        """
        taskparameters = {'command': 'GetPickAndPlaceLog',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def MoveRobotOutOfCameraOcclusion(self, regionname=None, robotspeed=None, toolname=None, timeout=10, **kwargs):
        """moves the robot out of camera occlusion and deletes targets if it was in occlusion.
        
        :param toolname: name of the tool to move when avoiding
        :param cameranames: the names of the cameras to avoid occlusions with the robot, list of strings
        """
        if regionname is None:
            regionname = self.regionname
        if toolname is None:
            toolname = self.toolname
        taskparameters = {'command': 'MoveRobotOutOfCameraOcclusion',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          'containername': regionname,
                          'toolname': toolname
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)
    
    def GetRobotBridgePLCStatus(self, timeout=10, **kwargs):
        taskparameters = {'command': 'GetRobotBridgePLCStatus',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def PausePickPlace(self, timeout=10, **kwargs):
        taskparameters = {'command': 'PausePickPlace',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def ResumePickPlace(self, timeout=10, **kwargs):
        taskparameters = {'command': 'ResumePickPlace',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)
    
    def GetRobotBridgeState(self, timeout=10, **kwargs):
        taskparameters = {'command': 'GetRobotBridgeState',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def GetBinpickingState(self, timeout=10, **kwargs):
        taskparameters = {'command': 'GetBinpickingState',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)
    
    #######################
    # unsupported commands
    #######################

    def UnchuckManipulator(self, *args, **kwargs):
        log.warn('deprecated')
        return self.UnchuckGripper(*args, **kwargs)

    def ChuckManipulator(self, *args, **kwargs):
        log.warn('deprecated')
        return self.ChuckGripper(*args, **kwargs)

    def __StartBackgroundTask(self, taskname, robotspeed=None, timeout=10):
        """starts a background task (need testing)
        :param taskname: name of the background task
        """
        taskparameters = {'command': 'ExecuteBackgroundTask',
                          'taskname': taskname,
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)

    def __StopBackgroundTask(self, timeout=10):
        """stops the background task (need testing)
        assumes that only one background task is running
        """
        taskparameters = {'command': 'StopBackgroundTask',
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def __PickAndMove(self, goaltype, armjointvaluesgoals, destinationgoals=None, targetnames=None, movetodestination=0, deletetarget=1, startvalues=None, toolname=None, envclearance=20, regionname=None, robotspeed=None, timeout=10):
        """deprecated
        """
        if toolname is None:
            toolname = self.toolname
        taskparameters = {'command': 'PickAndMove',
                          'toolname': toolname,
                          'goaltype': goaltype,
                          'envclearance': envclearance,
                          'movetodestination': movetodestination,
                          'deletetarget': deletetarget,
                          'armjointvaluesgoals': list(armjointvaluesgoals),
                          'sceneparams': self.sceneparams,
                          'tasktype': self.tasktype,
                          }
        if regionname is not None:
            taskparameters['boxname'] = regionname  # TODO: update backend
        if destinationgoals is not None:
            taskparameters['goals'] = destinationgoals
        if targetnames is not None:
            taskparameters['targetnames'] = targetnames
        if startvalues is not None:
            taskparameters['startvalues'] = list(startvalues)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)
