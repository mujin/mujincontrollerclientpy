# -*- coding: utf-8 -*-
# Copyright (C) 2013-2014 MUJIN Inc.
# Mujin controller client for bin picking task

# logging
import logging
log = logging.getLogger(__name__)

# system imports

# mujin imports
from . import controllerclientbase

class BinpickingControllerClient(controllerclientbase.ControllerClientBase):
    """mujin controller client for bin picking task
    """
    tasktype = 'binpicking'
    def __init__(self, controllerurl, controllerusername, controllerpassword, robotcontrollerhostname, robotcontrollerport, binpickingzmqport, scenepk, robotname, robotspeed, containername, targetname, toolname, envclearance, usewebapi=False):
        """logs into the mujin controller, initializes binpicking task, and sets up parameters
        :param controllerurl: url of the mujin controller, e.g. http://controller14
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        :param robotcontrollerhostname: hostname of the robot controller, e.g. 192.168.13.201
        :param robotcontrollerport: port of the robot controller, e.g. 5007
        :param binpickingzmqport: port of the binpicking task's zmq server, e.g. 7100
        :param scenepk: pk of the bin picking task scene, e.g. irex2013.mujin.dae
        :param robotname: name of the robot, e.g. VP-5243I
        :param robotspeed: speed of the robot, e.g. 0.4
        :param containername: name of the bin, e.g. container1
        :param targetname: name of the target, e.g. plasticnut-center
        :param toolname: name of the manipulator, e.g. 2BaseZ
        :param envclearance: environment clearance in milimeter, e.g. 20
        :param usewebapi: whether to use webapi for controller commands
        """
        super(BinpickingControllerClient, self).__init__(controllerurl, controllerusername, controllerpassword, binpickingzmqport, self.tasktype, scenepk)

        # robot controller
        self.robotcontrollerhostname = robotcontrollerhostname
        self.robotcontrollerport = robotcontrollerport

        # bin picking task
        self.scenepk = scenepk
        self.robotname = robotname
        self.robotspeed = robotspeed
        self.containername = containername
        self.targetname = targetname
        self.toolname = toolname
        self.envclearance = envclearance

        # whether to use webapi for bin picking task commands
        self.usewebapi = usewebapi
        
    #########################
    # robot commands        
    #########################

    def ExecuteRobotCommand(self, taskparameters, robotspeed=None):
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
        robotcontrollerhostname = self.robotcontrollerhostname
        robotcontrollerport = self.robotcontrollerport
        taskparameters['robot'] = robotname
        taskparameters['robotcontrollerip'] = robotcontrollerhostname
        taskparameters['robotcontrollerport'] = robotcontrollerport
        
        if taskparameters.get('speed',None) is None:
            # taskparameters does not have robotspeed, so set the global speed
            if robotspeed is None:
                taskparameters['robotspeed'] = self.robotspeed
            else:
                taskparameters['robotspeed'] = robotspeed
                
        return self.ExecuteCommand(taskparameters)

    def ExecuteTrajectory(self, trajectoryxml, robotspeed=None, **kwargs):
        """Executes a trajectory on the robot from a serialized Mujin Trajectory XML file.
        """
        taskparameters = {'command': 'ExecuteTrajectory',
                          'trajectory': trajectoryxml }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed)
        
    def MoveJoints(self, jointvalues, jointindices=None, robotspeed=None, execute=1, startvalues=None, **kwargs):
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
                          'execute' : execute,
                          }
        if startjointvalues is not None:
            taskparameters['startvalues'] = list(startjointvalues)
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed)
    
    def UnchuckGripper(self, toolname=None, targetname=None, robotspeed=None):
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
                          }
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed)
    
    def ChuckGripper(self,toolname=None, robotspeed=None):
        """chucks the manipulator
        :param toolname: name of the manipulator, default is self.toolname
        """
        if toolname is None:
            toolname=self.toolname
        taskparameters = {'command': 'ChuckGripper',
                          'toolname': toolname,
                          }
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed)
    
    def GetJointValues(self):
        """gets the current robot joint values
        :return: current joint values in a json dictionary with
        - currentjointvalues: [0,0,0,0,0,0]
        """
        taskparameters = {'command': 'GetJointValues',
                          }
        return self.ExecuteRobotCommand(taskparameters)
    
    def GetManipulatorTransformInRobotFrame(self):
        """gets the transform of the manipulator in robot frame
        :return: current transform of the manipulator in robot frame in a json dictionary, e.g. {'translation': [100,200,300], 'rotationmat': [[1,0,0],[0,1,0],[0,0,1]], 'quaternion': [1,0,0,0]}
        """
        taskparameters = {'command': 'GetManipTransformToRobot',
                          }
        return self.ExecuteRobotCommand(taskparameters)
    
    def PickAndPlace(self, goaltype, goals, targetnamepattern=None, approachoffset=30, departoffsetdir=[0,0,50], leaveoffsetdir=[0,0,30], deletetarget=0, debuglevel=4, movetodestination=1, freeinc=[0.08], worksteplength=None, armgroup=5, containername=None, envclearance=15, toolname=None, robotspeed=0.5, **kwargs):
        """picks up an object with the targetnamepattern and places it down at one of the goals. First computes the entire plan from robot moving to a grasp and then moving to its destination, then runs it on the real robot. Task finishes once the real robot is at the destination.
        
        :param desttargetname: The destination target name where the destination goal ikparams come from
        :param destikparamnames: A list of lists of ikparam names for the destinations of the target. Only destikparamnames[0] is looked at and tells the system to place the part in any of the ikparams in destikparamnames[0]
        
        :param targetnamepattern: regular expression describing the name of the object, default is '%s_\d+'%(self.targetname). See https://docs.python.org/2/library/re.html
        :param approachoffset: distance in milimeter to move straight to the grasp point, e.g. 30 mm
        :param departoffsetdir: the direction and distance in mm to move the part in global frame (usually along negative gravity) after it is grasped, e.g. [0,0,50]
        :param leaveoffsetdir: the direction and distance in mm to move away from the object after it is placed, e.g. [0,0,30]
        :param deletetarget: whether to delete target after pick and place is done
        :param toolname: name of the manipulator
        :param containername: name of the container of the objects
        :param cameranames: the names of the cameras to avoid occlusions with the robot, list of strings
        :param envclearance: environment clearance in milimeter
        
        Low level planning parameters:
        :param debuglevel: sets debug level of the task
        :param movetodestination: planning parameter
        :param iksolverfreeinc: discretization parameter of the ik solver free joints
        :param worksteplength: planning parameter
        :param armgroup: planning parameter
        :param graspsetname: the name of the grasp set belong to the target objects to use for the target. Grasp sets are a list of ikparams

        Manual Destination Specification (deprecated)
        :param goaltype: type of the goal, e.g. translationdirection5d or transform6d
        :param goals: flat list of goals, e.g. two 5d ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]
        
        """
        if worksteplength is None:
            worksteplength = min(0.25, 0.1/robotspeed)
        if toolname is None:
            toolname=self.toolname
        if targetnamepattern is None:
            targetnamepattern='%s_\d+'%(self.targetname)
        if containername is None:
            containername = self.containername
        taskparameters = {'command': 'PickAndPlace',
                          'toolname': toolname,
                          'goaltype': goaltype,
                          'envclearance': envclearance,
                          'movetodestination': movetodestination,
                          'armgroup': armgroup,
                          'goals': goals,
                          'approachoffset': approachoffset,
                          'departoffsetdir': departoffsetdir,
                          'leaveoffsetdir': leaveoffsetdir,
                          'freeinc': freeinc,
                          'worksteplength': worksteplength,
                          'targetnamepattern':targetnamepattern,
                          'containername':containername,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed)
    
    def StartPickAndPlaceThread(self, goaltype, goals, targetnamepattern=None, approachoffset=30, departoffsetdir=[0,0,50], leaveoffsetdir=[0,0,30], deletetarget=0, debuglevel=4, movetodestination=1, freeinc=[0.08], worksteplength=None, armgroup=5, containername=None, envclearance=15, toolname=None, **kwargs):
        """Start a background loop to continuously pick up objects with the targetnamepattern and place them down at the goals. The loop will check new objects arriving in and move the robot as soon as it finds a feasible grasp. The thread can be quit with StopPickPlaceThread.
        
        :param desttargetname: The destination target name where the destination goal ikparams come from
        :param destikparamnames: A list of lists of ikparam names for the ordered destinations of the target. destikparamnames[0] is where the first picked up part goes, desttargetname[1] is where the second picked up target goes.
        :param targetnamepattern: regular expression describing the name of the object, default is '%s_\d+'%(self.targetname). See https://docs.python.org/2/library/re.html
        :param approachoffset: distance in milimeter to move straight to the grasp point, e.g. 30 mm
        :param departoffsetdir: the direction and distance in mm to move the part in global frame (usually along negative gravity) after it is grasped, e.g. [0,0,50]
        :param leaveoffsetdir: the direction and distance in mm to move away from the object after it is placed, e.g. [0,0,30]
        :param deletetarget: whether to delete target after pick and place is done
        :param toolname: name of the manipulator
        :param containername: name of the container of the objects
        :param cameranames: the names of the cameras to avoid occlusions with the robot, list of strings
        :param envclearance: environment clearance in milimeter
        Low level planning parameters:
        :param debuglevel: sets debug level of the task
        :param movetodestination: planning parameter
        :param iksolverfreeinc: discretization parameter of the ik solver free joints
        :param worksteplength: planning parameter
        :param armgroup: planning parameter
        :param graspsetname: the name of the grasp set belong to the target objects to use for the target. Grasp sets are a list of ikparams
        
        :param goaltype: type of the goal, e.g. translationdirection5d
        :param goals: flat list of goals, e.g. two 5d ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]

        """        
        if worksteplength is None:
            worksteplength = 0.01
        if toolname is None:
            toolname=self.toolname
        if goals is None:
            goals = GetOrderedGoals(self.targetname,envclearance,numparts)
        if targetnamepattern is None:
            targetnamepattern='%s_\d+'%(self.targetname)
        if containername is None:
            containername = self.containername
        taskparameters = {'command': 'StartPickAndPlaceThread',
                          'toolname': toolname,
                          'goaltype': goaltype,
                          'envclearance': envclearance,
                          'movetodestination': movetodestination,
                          'armgroup': armgroup,
                          'orderedgoals': goals,
                          'approachoffset': approachoffset,
                          'departoffsetdir': departoffsetdir,
                          'leaveoffsetdir': leaveoffsetdir,
                          'freeinc': freeinc,
                          'worksteplength': worksteplength,
                          'targetnamepattern':targetnamepattern,
                          'containername':containername
                          }
        taskparameters.update(kwargs);
        return self.ExecuteRobotCommand(taskparameters, robotspeed=taskparameters.get('robotspeed',None))
    
    def StopPickPlaceThread(self, **kwargs):
        """stops the pick and place thread started with StartPickAndPlaceThread
        """
        taskparameters = {'command': 'StopPickPlaceThread'}
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters)
    
    def GetPickPlaceStatus(self, **kwargs):
        """gets the status of the pick and place thread
        :return: status (0: not running, 1: no error, 2: error) of the pick and place thread in a json dictionary, e.g. {'status': 2, 'error': 'an error happened'}
        """
        taskparameters = {'command': 'GetPickPlaceStatus'}
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters)
    
    def MoveToHandPosition(self,goaltype,goals,toolname=None,envclearance=None,closegripper=0, robotspeed=None):
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
                          'goaltype':goaltype,
                          'goals':goals,
                          'toolname': toolname,
                          'envclearance':envclearance,
                          'closegripper':closegripper,
                          }
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed)
    
    def ComputeIK(self, **kwargs):
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
        taskparameters = {'command': 'ComputeIK'}
        taskparameters.update(kwargs)
        if not 'toolname' in taskparameters:
            taskparameters['toolname'] = self.toolname
        if not 'envclearance' in taskparameters:
            taskparameters['envclearance'] = self.envclearance
        return self.ExecuteRobotCommand(taskparameters)
    
    def ComputeIKFromParameters(self, **kwargs):
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
        taskparameters = {'command': 'ComputeIKFromParameters'}
        taskparameters.update(kwargs)
        if not 'toolname' in taskparameters:
            taskparameters['toolname'] = self.toolname
        if not 'envclearance' in taskparameters:
            taskparameters['envclearance'] = self.envclearance
        return self.ExecuteRobotCommand(taskparameters)
    
    def InitializePartsWithPhysics(self, **kwargs):
        """Start a physics simulation where the parts drop down into the bin. The method returns as soon as the physics is initialized, user has to wait for the "duration" or call StopPhysicsThread command.
        :param targeturi: the target uri to initialize the scene with
        :param numtargets: the number of targets to create
        :param containername: the container name to drop the targets into
        :param duration: the duration in seconds to continue the physics until it is stopped.
        :param basename: The basename to give to all the new target names. Numbers are suffixed at the end, like basename+'0134'. If not specified, will use a basename derived from the targeturi.
        :param deleteprevious: if True, will delete all the previous targets in the scene. By default this is True.
        """
        taskparameters = {'command': 'InitializePartsWithPhysics'}
        taskparameters.update(kwargs)
        if not 'containername' in taskparameters:
            taskparameters['containername'] = self.containername
        return self.ExecuteRobotCommand(taskparameters)
        
    def StopPhysicsThread(self, **kwargs):
        """stops the physics simulation started with InitializePartsWithPhysics
        """
        taskparameters = {'command': 'StopPhysicsThread'}
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters)
        

    def JitterPartUntilValidGrasp(self, **kwargs):
        """Select a part that wasn't able to be grasped and jitter its location such that a grasp set is found for it that will take it to the destination.

        On the backend, we should call this function "JitterPartUntilValidGrasp?", parameters should be
        :param toolname: name of the manipulator
        :param targetname: The target to try to grasp.
        :param graspsetname: the name of the grasp set belong to the target objects to use for the target. Grasp sets are a list of ikparams.
        :param approachoffset: The approach distance for simulating full grasp.
        :param departoffsetdir: The depart distance for simulating full grasp.
        :param desttargetname: The destination target name where the destination goal ikparams come from
        :param destikparamnames: A list of lists of ikparam names for the ordered destinations of the target. destikparamnames[0] is where the first picked up part goes, desttargetname[1] is where the second picked up target goes.
        :param jitterdist: Amount to jitter the target object translation by
        :param jitterangle: Amount to jitter the target object's orientation angle

        :return: A dictionary with the following keys:
          - translation: the new translation of the target part
          - quaternion: the new quaternion of the target part
          - jointvalues: robot joint values that are grasping the part (fingers are at their preshape)
        """
        taskparameters = {'command': 'JitterPartUntilValidGrasp'}
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters)

    ####################
    # scene commands
    ####################
    
    def IsRobotOccludingBody(self,bodyname,cameraname):
        """returns if the robot is occluding body in the view of the specified camera
        :param bodyname: name of the object
        :param cameraname: name of the camera
        :param robotname: name of the robot
        :return: the occlusion state in a json dictionary, e.g. {'occluded': 0}
        """
        taskparameters = {'command' : 'IsRobotOccludingBody',
                          'robotname': self.robotname,
                          'bodyname': bodyname,
                          'cameraname': cameraname,
                          }
        return self.ExecuteCommand(taskparameters)
    
    def GetPickedPositions(self):
        """returns the poses and the timestamps of the picked objects
        :param robotname: name of the robot
        :return: the positions and the timestamps of the picked objects in a json dictionary, info of each object has the format of quaternion (w,x,y,z) followed by x,y,z translation in milimeter followed by timestamp in milisecond e.g. {'positions': [[1,0,0,0,100,200,300,1389774818.8366449],[1,0,0,0,200,200,300,1389774828.8366449]]}
        """
        taskparameters = {'command': 'GetPickedPositions',
                          'robotname': self.robotname}
        return self.ExecuteCommand(taskparameters)

    def UpdateObjects(self, envstate, targetname=None):
        """updates objects in the scene with the envstate
        :param envstate: a list of dictionaries for each instance object. translation is in milimeter. quaternion is specified in w,x,y,z order. e.g. [{'name': 'target_0', 'translation_': [100,200,300], 'quat_': [1,0,0,0]}, {'name': 'target_1', 'translation_': [200,200,300], 'quat_': [1,0,0,0]}]
        """
        if targetname is None:
            targetname = self.targetname
        taskparameters = { 'command': 'UpdateObjects',
                           'objectname': targetname,
                           'object_uri': u'mujin:/%s.mujin.dae'%(targetname),
                           'robot': self.robotname,
                           'envstate': envstate,
                           }
        return self.ExecuteCommand(taskparameters)


    def Grab(self, targetname, toolname=None):
        """grabs an object with tool
        :param targetname: name of the object
        :param robotname: name of the robot
        :param toolname: name of the manipulator, default is self.toolname
        """
        if toolname is None:
            toolname = self.toolname
        taskparameters = {'command' : 'Grab',
                          'targetname': targetname,
                          'robotname': self.robotname,
                          'toolname': toolname,
                          }
        return self.ExecuteCommand(taskparameters)

    def GetGrabbed(self):
        """gets the names of the grabbed objects
        :return: names of the grabbed object in a json dictionary, e.g. {'names': ['target_0']}
        """
        taskparameters = {'command': 'GetGrabbed',
                          'robotname': self.robotname,
                          }
        return self.ExecuteCommand(taskparameters)

    def GetTransform(self,targetname):
        """gets the transform of an object
        :param targetname: name of the object
        :return: transform of the object in a json dictionary, e.g. {'translation': [100,200,300], 'rotationmat': [[1,0,0],[0,1,0],[0,0,1]], 'quaternion': [1,0,0,0]}
        """
        taskparameters = {'command': 'GetTransform',
                          'targetname': targetname,
                          }
        return self.ExecuteCommand(taskparameters)

    def SetTransform(self,targetname,translation,rotationmat=None,quaternion=None):
        """sets the transform of an object
        :param targetname: name of the object
        :param translation: list of x,y,z value of the object in milimeter
        :param rotationmat: list specifying the rotation matrix in row major format, e.g. [1,0,0,0,1,0,0,0,1]
        :param quaternion: list specifying the quaternion in w,x,y,z format, e.g. [1,0,0,0]
        """
        taskparameters = {'command': 'SetTransform',
                          'targetname': targetname,
                          'translation': translation,
                          }
        if rotationmat is not None:
            taskparameters['rotationmat'] = rotationmat
        if quaternion is not None:
            taskparameters['quaternion'] = quaternion
        if rotationmat is None and quaternion is None:
            taskparameters['quaternion'] = [1,0,0,0]
            log.warn('no rotation is specified, using identity quaternion ', taskparameters['quaternion'])
        return self.ExecuteCommand(taskparameters)

    def RemoveObjectsWithPrefix(self,prefix):
        """removes objects with prefix
        """
        taskparameters = {'command': 'RemoveObjectsWithPrefix',
                          'prefix': prefix,
                          }
        return self.ExecuteCommand(taskparameters)

    def SaveScene(self,**kwargs):
        """saves the current scene to file
        :param filename: e.g. /tmp/testscene.mujin.dae, if not specified, it will be saved with an auto-generated filename
        :param externalref: If '*', then will save each of the objects as externally referencing their original filename.
        :param saveclone: If 1, will save the scenes for all the cloned environments
        :return: the actual filename the scene is saved to in a json dictionary, e.g. {'filename': '2013-11-01-17-10-00-UTC.dae'}
        """
        taskparameters = {'command': 'SaveScene'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters)

    def GetTrajectoryLog(self,**kwargs):
        """Gets the recent trajectories executed on the binpicking server. The internal server keeps trajectories around for 10 minutes before clearing them.
        
        :param startindex: int, start of the trajectory to get
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
        return self.ExecuteCommand(taskparameters)

    #######################
    # unsupported commands
    #######################

    def UnchuckManipulator(self, *args, **kwargs):
        log.warn('deprecated')
        return self.UnchuckGripper(*args, **kwargs)
    
    def ChuckManipulator(self, *args, **kwargs):
        log.warn('deprecated')
        return self.ChuckGripper(*args, **kwargs)
    
    def __StartBackgroundTask(self, taskname, robotspeed=None):
        """starts a background task (need testing)
        :param taskname: name of the background task
        """
        taskparameters = {'command':'ExecuteBackgroundTask',
                          'taskname':taskname}
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed)

    def __StopBackgroundTask(self):
        """stops the background task (need testing)
        assumes that only one background task is running
        """
        taskparameters = {'command':'StopBackgroundTask'}
        return self.ExecuteRobotCommand(taskparameters)

    def __PickAndMove(self,goaltype,armjointvaluesgoals,destinationgoals=None,targetnames=None,movetodestination=0,deletetarget=1, startvalues=None,toolname=None,envclearance=20,boxname=None, robotspeed=None):
        """deprecated
        """
        if toolname is None:
            toolname=self.toolname
        taskparameters = {'command': 'PickAndMove',
                          'toolname': toolname,
                          'goaltype':goaltype,
                          'envclearance':envclearance,
                          'movetodestination': movetodestination,
                          'deletetarget': deletetarget,
                          'armjointvaluesgoals':list(armjointvaluesgoals),
                          }
        if boxname is not None:
            taskparameters['boxname']=boxname
        if destinationgoals is not None:
            taskparameters['goals']=destinationgoals
        if targetnames is not None:
            taskparameters['targetnames']=targetnames
        if startvalues is not None:
            taskparameters['startvalues'] = list(startvalues)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed)

