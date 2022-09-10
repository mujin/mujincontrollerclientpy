# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
# Mujin controller client for bin picking task

# mujin imports
from . import realtimerobotclient

# logging
import logging
log = logging.getLogger(__name__)


class BinpickingControllerClient(realtimerobotclient.RealtimeRobotControllerClient):
    """mujin controller client for bin picking task
    """
    tasktype = 'binpicking'

    def __init__(self, regionname=None, **kwargs):
        """logs into the mujin controller, initializes binpicking task, and sets up parameters
        
        Args:
            controllerurl: url of the mujin controller, e.g. http://controller14
            controllerusername: username of the mujin controller, e.g. testuser
            controllerpassword: password of the mujin controller
            taskzmqport: port of the binpicking task's zmq server, e.g. 7110
            taskheartbeatport: port of the binpicking task's zmq server's heartbeat publisher, e.g. 7111
            taskheartbeattimeout: seconds until reinitializing binpicking task's zmq server if no heartbeat is received, e.g. 7
            scenepk: pk of the bin picking task scene, e.g. irex2013.mujin.dae
            robotname: name of the robot, e.g. VP-5243I
            regionname: name of the bin, e.g. container1
            toolname: name of the manipulator, e.g. 2BaseZ
            envclearance: environment clearance in millimeters, e.g. 20
            usewebapi: whether to use webapi for controller commands
            robotaccelmult: optional multiplier for forcing the acceleration
        """
        super(BinpickingControllerClient, self).__init__(tasktype=self.tasktype, **kwargs)

        # bin picking task
        self.regionname = regionname

    #########################
    # robot commands
    #########################

    def PickAndPlace(self, goaltype, goals, targetnamepattern=None, approachoffset=30, departoffsetdir=[0, 0, 50], destdepartoffsetdir=[0, 0, 30], deletetarget=0, debuglevel=4, movetodestination=1, freeinc=[0.08], worksteplength=None, densowavearmgroup=5, regionname=None, cameranames=None, envclearance=None, toolname=None, robotspeed=None, timeout=1000, **kwargs):
        """picks up an object with the targetnamepattern and places it down at one of the goals. First computes the entire plan from robot moving to a grasp and then moving to its destination, then runs it on the real robot. Task finishes once the real robot is at the destination.

        :param desttargetname: The destination target name where the destination goal ikparams come from
        :param destikparamnames: A list of lists of ikparam names for the destinations of the target. Only destikparamnames[0] is looked at and tells the system to place the part in any of the ikparams in destikparamnames[0]

        :param targetnamepattern: regular expression describing the name of the object, no default will be provided, caller must set this. See https://docs.python.org/2/library/re.html
        :param approachoffset: distance in millimeters to move straight to the grasp point, e.g. 30 mm
        :param departoffsetdir: the direction and distance in mm to move the part in global frame (usually along negative gravity) after it is grasped, e.g. [0,0,50]
        :param destdepartoffsetdir: the direction and distance in mm to move away from the object after it is placed, e.g. [0,0,30]. Depending on leaveoffsetintool parameter, this can in the global coordinate system or tool coordinate system.
        :param leaveoffsetintool: If 1, destdepartoffsetdir is in the tool coordinate system. If 0, destdepartoffsetdir is in the global coordinate system. By default this is 0.
        :param deletetarget: whether to delete target after pick and place is done
        :param toolname: name of the manipulator
        :param regionname: name of the region of the objects
        :param cameranames: the names of the cameras to avoid occlusions with the robot, list of strings
        :param envclearance: environment clearance in millimeters

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
        assert (targetnamepattern is not None)
        if regionname is None:
            regionname = self.regionname
        taskparameters = {
            'command': 'PickAndPlace',
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
            'deletetarget': deletetarget,
            'debuglevel': debuglevel,
        }
        if regionname is not None:
            taskparameters['containername'] = regionname
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotspeed=robotspeed, toolname=toolname, timeout=timeout)

    def StartPickAndPlaceThread(self, goaltype=None, goals=None, targetnamepattern=None, approachoffset=30, departoffsetdir=[0, 0, 50], destdepartoffsetdir=[0, 0, 30], deletetarget=0, debuglevel=4, movetodestination=1, worksteplength=None, regionname=None, envclearance=None, toolname=None, robotspeed=None, timeout=10, usewebapi=None, **kwargs):
        """Start a background loop to continuously pick up objects with the targetnamepattern and place them down at the goals. The loop will check new objects arriving in and move the robot as soon as it finds a feasible grasp. The thread can be quit with StopPickPlaceThread.

        :param desttargetname: The destination target name where the destination goal ikparams come from
        :param destikparamnames: A list of lists of ikparam names for the ordered destinations of the target. destikparamnames[0] is where the first picked up part goes, desttargetname[1] is where the second picked up target goes.
        :param cycledests: When finished cycling through all destikparamnames, will delete all the targets and start from the first index again doing this for cycledests times. By default it is 1.

        :param targetnamepattern: regular expression describing the name of the object, no default will be provided, caller must set this. See https://docs.python.org/2/library/re.html
        :param approachoffset: distance in millimeters to move straight to the grasp point, e.g. 30 mm
        :param departoffsetdir: the direction and distance in mm to move the part in global frame (usually along negative gravity) after it is grasped, e.g. [0,0,50]
        :param destdepartoffsetdir: the direction and distance in mm to move away from the object after it is placed, e.g. [0,0,30]. Depending on leaveoffsetintool parameter, this can in the global coordinate system or tool coordinate system.
        :param leaveoffsetintool: If 1, destdepartoffsetdir is in the tool coordinate system. If 0, destdepartoffsetdir is in the global coordinate system. By default this is 0.
        :param deletetarget: whether to delete target after pick and place is done
        :param toolname: name of the manipulator
        :param regionname: name of the region of the objects
        :param cameranames: the names of the cameras to avoid occlusions with the robot, list of strings
        :param envclearance: environment clearance in millimeters
        Low level planning parameters:
        :param debuglevel: sets debug level of the task
        :param movetodestination: planning parameter
        :param worksteplength: planning parameter
        :param densowavearmgroup: robot parameters
        :param graspsetname: the name of the grasp set belong to the target objects to use for the target. Grasp sets are a list of ikparams

        :param goaltype: type of the goal, e.g. translationdirection5d
        :param goals: flat list of goals, e.g. two 5d ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]

        :param useworkspaceplanner: If 1 is set, will try the workspace planner for moving the hand straight. If 2 is set, will try the RRT for moving straight. Can set 3 for trying both.

        :param forceStartRobotValues: planning loop should always start from these values rather than reading from robot
        :param initiallyDisableRobotBridge: if True, stops any communication with the robotbridge until robot bridge is enabled
        """
        if worksteplength is None:
            worksteplength = 0.01
        assert (targetnamepattern is not None)
        if regionname is None:
            regionname = self.regionname
        taskparameters = {
            'command': 'StartPickAndPlaceThread',
            'envclearance': envclearance,
            'movetodestination': movetodestination,
            'approachoffset': approachoffset,
            'departoffsetdir': departoffsetdir,
            'destdepartoffsetdir': destdepartoffsetdir,
            'worksteplength': worksteplength,
            'targetnamepattern': targetnamepattern,
            'containername': regionname,
            'deletetarget': deletetarget,
            'debuglevel': debuglevel,
        }
        if goals is not None:
            taskparameters['orderedgoals'] = goals
            taskparameters['goaltype'] = goaltype
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotspeed=robotspeed, toolname=toolname, timeout=timeout, usewebapi=usewebapi)

    def StopPickPlaceThread(self, resetExecutionState=True, resetStatusPickPlace=False, finishCode=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """stops the pick and place thread started with StartPickAndPlaceThread
        :param resetExecutionState: if True, then reset the order state variables. By default True
        :param resetStatusPickPlace: if True, then reset the statusPickPlace field of hte planning slave. By default False.
        :param finishCode: optional finish code to end the cycle with (if it doesn't end with something else beforehand)
        """
        taskparameters = {
            'command': 'StopPickPlaceThread',
            'resetExecutionState': resetExecutionState,
            'resetStatusPickPlace': resetStatusPickPlace,
            'finishCode': finishCode
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def GetPickPlaceStatus(self, timeout=10, **kwargs):
        """gets the status of the pick and place thread
        :return: status (0: not running, 1: no error, 2: error) of the pick and place thread in a json dictionary, e.g. {'status': 2, 'error': 'an error happened'}
        """
        taskparameters = {'command': 'GetPickPlaceStatus'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ComputeIK(self, toolname=None, timeout=10, **kwargs):
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
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout)

    def InitializePartsWithPhysics(self, timeout=10, **kwargs):
        """Start a physics simulation where the parts drop down into the bin. The method returns as soon as the physics is initialized, user has to wait for the "duration" or call StopPhysicsThread command.
        :param targeturi: the target uri to initialize the scene with
        :param numtargets: the number of targets to create
        :param regionname: the container name to drop the targets into
        :param duration: the duration in seconds to continue the physics until it is stopped.
        :param basename: The basename to give to all the new target names. Numbers are suffixed at the end, like basename+'0134'. If not specified, will use a basename derived from the targeturi.
        :param deleteprevious: if True, will delete all the previous targets in the scene. By default this is True.
        :param forcegravity: if not None, the gravity with which the objects should fall with. If None, then uses the scene's gravity
        """
        taskparameters = {'command': 'InitializePartsWithPhysics'}
        taskparameters.update(kwargs)
        if 'containername' not in taskparameters:
            taskparameters['containername'] = self.regionname
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def StopPhysicsThread(self, timeout=10, **kwargs):
        """stops the physics simulation started with InitializePartsWithPhysics
        """
        taskparameters = {'command': 'StopPhysicsThread'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def JitterPartUntilValidGrasp(self, toolname=None, timeout=10, **kwargs):
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
        taskparameters = {'command': 'JitterPartUntilValidGrasp'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout)

    def MoveToDropOff(self, dropOffInfo, robotname=None, robotspeed=None, robotaccelmult=None, execute=1, startvalues=None, envclearance=None, timeout=10, usewebapi=True, **kwargs):
        """Moves the robot to desired joint angles.

        Args:
            dropOffInfo:
            robotname (str, optional): Name of the robot
            robotspeed (float, optional): Value in (0,1] setting the percentage of robot speed to move at
            robotaccelmult (float, optional): Value in (0,1] setting the percentage of robot acceleration to move at
            execute:  (Default: 1)
            startvalues (list[float], optional):
            envclearance (float, optional): Environment clearance in millimeters
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: True)
        """
        taskparameters = {
            'command': 'MoveToDropOff',
            'dropOffInfo': dropOffInfo,
            'execute': execute,
        }
        if envclearance is not None:
            taskparameters['envclearance'] = envclearance
        if startvalues is not None:
            taskparameters['startvalues'] = list(startvalues)

        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, robotspeed=robotspeed, robotaccelmult=robotaccelmult, timeout=timeout, usewebapi=usewebapi)

    ####################
    # scene commands
    ####################

    def IsRobotOccludingBody(self, bodyname, cameraname, timeout=10, **kwargs):
        """returns if the robot is occluding body in the view of the specified camera
        :param bodyname: name of the object
        :param cameraname: name of the camera
        :return: the occlusion state in a json dictionary, e.g. {'occluded': 0}
        """
        taskparameters = {
            'command': 'IsRobotOccludingBody',
            'bodyname': bodyname,
            'cameraname': cameraname,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetPickedPositions(self, unit='m', timeout=10, **kwargs):
        """returns the poses and the timestamps of the picked objects
        :param unit: unit of the translation
        :return: the positions and the timestamps of the picked objects in a json dictionary, info of each object has the format of quaternion (w,x,y,z) followed by x,y,z translation (in mm) followed by timestamp in milisecond e.g. {'positions': [[1,0,0,0,100,200,300,1389774818.8366449],[1,0,0,0,200,200,300,1389774828.8366449]]}
        """
        taskparameters = {
            'command': 'GetPickedPositions',
            'unit': unit,
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
        taskparameters = {
            'command': 'MoveRobotOutOfCameraOcclusion',
            'containername': regionname,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotspeed=robotspeed, toolname=toolname, timeout=timeout)

    def PausePickPlace(self, timeout=10, **kwargs):
        taskparameters = {
            'command': 'PausePickPlace',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ResumePickPlace(self, timeout=10, **kwargs):
        taskparameters = {
            'command': 'ResumePickPlace',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def SendStateTrigger(self, stateTrigger, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """
        :param stateTrigger: a string that represents a unique trigger
        """
        taskparameters = {
            'command': 'SendStateTrigger',
            'stateTrigger': stateTrigger,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def GetBinpickingState(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        taskparameters = {'command': 'GetBinpickingState'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def SetStopPickPlaceAfterExecutionCycle(self, timeout=10, **kwargs):
        """Sets the cycle for stopping after the current pick cycle finishes.

        If robot has not grabbed a part yet, then will stop the robot immediately.
        On proper finish of the pick cycle, robot should go back to the finish position.
        
        :param finishCode: the finish code to end with. If not specified, will be 'FinishedCycleStopped'
        """
        taskparameters = {
            'command': 'SetStopPickPlaceAfterExecutionCycle',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def PutPartsBack(self, trajectoryxml, numparts, toolname=None, grippervalues=None, usewebapi=False, timeout=100, **kwargs):
        """runs saved planningresult trajs
        """
        taskparameters = {
            'command': 'PutPartsBack',
            'trajectory': trajectoryxml,
            'numparts': numparts,
            'toolname': toolname,
        }
        if grippervalues is not None:
            taskparameters['grippervalues'] = grippervalues
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GenerateGraspModelFromIkParams(self, graspsetname, targeturi, toolname, robotname=None, usewebapi=True,
                                       timeout=10, **kwargs):
        """
        Generate grasp model ik for given setup
        :param graspsetname: str. Name of graspset like 'all5d'
        :param targeturi: str. uri of target scene like '4902201402644.mujin.dae'
        :param toolname: str. Name of manipulator of the robot like 'suction0'
        :param robotname:
        :param usewebapi:
        :param timeout:
        :return:
        """

        taskparameters = {
            'command': 'GenerateGraspModelFromIkParams',
            'graspsetname': graspsetname,
            'targeturi': targeturi,
            'toolname': toolname
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, toolname=toolname, usewebapi=usewebapi,
                                   timeout=timeout)

    def CheckGraspModelIk(self, graspsetname, targeturi, toolname, ikparamnames=None, usewebapi=True, timeout=10, **kwargs):
        """
        Check if grasp model is generated for given setup
        :param graspsetname: str. Name of graspset like 'all5d'
        :param targeturi: str. uri of target scene like 'mujin:4902201402644.mujin.dae'
        :param toolname: str. Name of manipulator of the robot like 'suction0'
        :param usewebapi:
        :return:
        """
        taskparameters = {
            'command': 'CheckGraspModelIk',
            'graspsetname': graspsetname,
            'targeturi': targeturi,
            'toolname': toolname,
            'ikparamnames': ikparamnames,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def SetCurrentLayoutDataFromPLC(self, containername, containerLayoutSize, destObstacleName, ioVariableName, timeout=10, usewebapi=True, **kwargs):
        """
        sets current layout from plc
        """
        taskparameters = {
            'command': 'SetCurrentLayoutDataFromPLC',
            'containername': containername,
            'containerLayoutSize': containerLayoutSize,
            'ioVariableName': ioVariableName,
            'destObstacleName': destObstacleName
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=False)

    def ClearVisualization(self, timeout=10, usewebapi=True, fireandforget=False, **kwargs):
        """
        clears visualization
        """
        taskparameters = {'command': 'ClearVisualization'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def GetPlanStatistics(self, timeout=1, usewebapi=True, fireandforget=False, **kwargs):
        """
        get plan and execute statistics of the last pick and place
        """
        taskparameters = {'command': 'GetPlanStatistics'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def SetCurrentLayoutDataSendOnObjectUpdateData(self, doUpdate, containername=None, containerLayoutSize=None, ioVariableName=None, usewebapi=False, fireandforget=True, **kwargs):
        """
        Sets currentLayoutDataSendOnObjectUpdateData structure
        :param doUpdate: if True then currentLayoutData will be send on every ObjectUpdate, else currentLayoutDataSendOnObjectUpdate structure is reset
        """
        taskparameters = {
            'command': 'SetCurrentLayoutDataSendOnObjectUpdateData',
            'doUpdate': doUpdate,
        }
        if containername is not None:
            taskparameters['containername'] = containername
        if containerLayoutSize is not None:
            taskparameters['containerLayoutSize'] = containerLayoutSize
        if ioVariableName is not None:
            taskparameters['ioVariableName'] = ioVariableName
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, fireandforget=fireandforget)

    def StartPackFormationComputationThread(self, timeout=10, debuglevel=4, toolname=None, usewebapi=None, **kwargs):
        """Start a background loop to copmute packing formation.
        """
        taskparameters = {
            'command': 'StartPackFormationComputationThread',
            'debuglevel': debuglevel,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout, usewebapi=usewebapi)

    def StopPackFormationComputationThread(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """stops the packing computation thread thread started with StartPackFormationComputationThread
        """
        taskparameters = {
            'command': 'StopPackFormationComputationThread',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def VisualizePackingState(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """stops the packing computation thread thread started with StartPackFormationComputationThread
        """
        taskparameters = {
            'command': 'VisualizePackingState',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    
    def GetPackFormationSolution(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """stops the packing computation thread thread started with StartPackFormationComputationThread
        """
        taskparameters = {
            'command': 'GetPackFormationSolution',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def SendPackFormationComputationResult(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """stops the packing computation thread thread started with StartPackFormationComputationThread
        """
        taskparameters = {
            'command': 'SendPackFormationComputationResult',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def GetLatestPackFormationResultList(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """
        Gets latest pack formation computation result
        """
        taskparameters = {
            'command': 'GetLatestPackFormationResultList',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def ValidatePackFormationResultList(self, packFormationResultList, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """
        Validates pack formation result list and compute info (fillRatio, packageDimensions, packedItemsInfo, etc) about it .
        kwargs should be packing parameters
        :return dictionary {'validatedPackFormationResultList':[{'validationStatus', 'errorCode', 'errorDesc', (optional)'packFormationResult'}]}
        """
        taskparameters = {
            'command': 'ValidatePackFormationResultList',
            'packFormationResultList': packFormationResultList
        }
        taskparameters.update(kwargs)
        ret = self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
        return ret 

    def ComputeSamePartPackResultBySimulation(self, timeout=100, usewebapi=None, **kwargs):
        """
        Compute pack formation for single part type.
        """
        taskparameters = {
            'command': 'ComputeSamePartPackResultBySimulation',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)
