# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

from . import json
from . import planningclient

import logging
log = logging.getLogger(__name__)

class RealtimeRobotControllerClient(planningclient.PlanningControllerClient):
    """Mujin controller client for RealtimeRobotControllerClient task"""
    _robotname = None  # Optional name of the robot selected
    _robotspeed = None  # Speed of the robot, e.g. 0.4
    _robotaccelmult = None  # Current robot accel mult
    _envclearance = None  # Environment clearance in millimeters, e.g. 20
    _robotBridgeConnectionInfo = None  # dict holding the connection info for the robot bridge.
    
    def __init__(self, robotname, robotspeed=None, robotaccelmult=None, envclearance=10.0, robotBridgeConnectionInfo=None, **kwargs):
        """
        Args:
            robotname (str): Name of the robot selected. Optional (can be empty)
            robotspeed (str, optional): Speed of the robot, e.g. 0.4.
            robotaccelmult (str, optional): Current robot acceleration multiplication.
            envclearance (str): Environment clearance in millimeter, e.g. 20
            robotBridgeConnectionInfo (str, optional): dict holding the connection info for the robot bridge.
            taskzmqport (int): Port of the task's ZMQ server, e.g. 7110
            taskheartbeatport (int): Port of the task's ZMQ server's heartbeat publisher, e.g. 7111
            taskheartbeattimeout (float): Seconds until reinitializing task's ZMQ server if no heartbeat is received, e.g. 7
            tasktype (str): Type of the task, e.g. 'binpicking', 'handeyecalibration', 'itlrealtimeplanning3'
            scenepk (str): Primary key (pk) of the scene, e.g. irex_demo.mujin.dae
            controllerurl (str): URL of the mujin controller, e.g. http://controller14
            controllerusername (str): Username for the Mujin controller, e.g. testuser
            controllerpassword (str): Password for the Mujin controller
        """
        super(RealtimeRobotControllerClient, self).__init__(**kwargs)
        self._robotname = robotname
        self._robotspeed = robotspeed
        self._robotaccelmult = robotaccelmult
        self._envclearance = envclearance
        self._robotBridgeConnectionInfo = robotBridgeConnectionInfo

    def GetRobotConnectionInfo(self):
        """ """
        return self._robotBridgeConnectionInfo
    
    def SetRobotConnectionInfo(self, robotBridgeConnectionInfo):
        """

        Args:
            robotBridgeConnectionInfo:
        """
        self._robotBridgeConnectionInfo = robotBridgeConnectionInfo
    
    def GetRobotName(self):
        """ """
        return self._robotname

    def SetRobotName(self, robotname):
        """

        Args:
            robotname (str):
        """
        self._robotname = robotname

    def SetRobotSpeed(self, robotspeed):
        """

        Args:
            robotspeed:
        """
        self._robotspeed = robotspeed

    def SetRobotAccelMult(self, robotaccelmult):
        """

        Args:
            robotaccelmult:
        """
        self._robotaccelmult = robotaccelmult

    def ExecuteCommand(self, taskparameters, robotname=None, toolname=None, robotspeed=None, robotaccelmult=None, envclearance=None, usewebapi=None, timeout=10, fireandforget=False, respawnopts=None):
        """Wrapper to ExecuteCommand with robot info specified in taskparameters.

        Executes a command in the task.

        Args:
            taskparameters (dict): Specifies the arguments of the task/command being called.
            robotname (str, optional): Name of the robot
            robotaccelmult (float, optional):
            envclearance (float, optional):
            respawnopts (optional):
            toolname (str, optional): Name of the manipulator. Default: self.toolname
            timeout (float, optional):  (Default: 10)
            fireandforget (bool, optional):  (Default: False)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            robotspeed (float, optional):

        Returns:
            dict: Contains:
                - robottype (str): robot type
                - currentjointvalues (list[float]): current joint values, vector length = DOF
                - elapsedtime (float): elapsed time in seconds
                - numpoints (int): the number of points
                - error (dict): optional error info
                - desc (str): error message
                - type (str): error type
                    - errorcode (str): error code
        """
        if robotname is None:
            robotname = self._robotname
        
        # caller wants to use a different tool
        if toolname is not None:
            # set at the first level
            taskparameters['toolname'] = toolname
        
        if robotname is not None:
            taskparameters['robotname'] = robotname
        
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
        
        if self._robotBridgeConnectionInfo is not None:
            taskparameters['robotBridgeConnectionInfo'] = self._robotBridgeConnectionInfo
        
        if 'envclearance' not in taskparameters or taskparameters['envclearance'] is None:
            if envclearance is None:
                envclearance = self._envclearance
            if envclearance is not None:
                taskparameters['envclearance'] = envclearance

        return super(RealtimeRobotControllerClient, self).ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget, respawnopts=respawnopts)

    def ExecuteTrajectory(self, trajectoryxml, robotspeed=None, timeout=10, **kwargs):
        """Executes a trajectory on the robot from a serialized Mujin Trajectory XML file.

        Args:
            trajectoryxml:
            robotspeed (float, optional): Value in (0,1] setting the percentage of robot speed to move at
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            kwargs:
        """
        taskparameters = {
            'command': 'ExecuteTrajectory',
            'trajectory': trajectoryxml,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)

    def GetJointValues(self, timeout=10, **kwargs):
        """Gets the current robot joint values

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            executetimeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            unit (str, optional): The unit of the given values. (Default: 'mm')
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.

        Returns:
            dict: Current joint values in a json dictionary with currentjointvalues: [0,0,0,0,0,0]
        """
        taskparameters = {
            'command': 'GetJointValues',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def MoveToolLinear(self, goaltype, goals, toolname=None, timeout=10, robotspeed=None, **kwargs):
        """Moves the tool linear

        Args:
            goaltype (str): Type of the goal, e.g. translationdirection5d
            goals (list): Flat list of goals, e.g. two 5D ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]
            toolname (str, optional): Tool name(s)
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            robotspeed (float, optional): Value in (0,1] setting the percentage of robot speed to move at
            workmaxdeviationangle (float, optional): How much the tool tip can rotationally deviate from the linear path. In deg.
            workspeed (float, optional): [anglespeed, transspeed] in deg/s and mm/s
            workaccel (float, optional): [angleaccel, transaccel] in deg/s^2 and mm/s^2
            worksteplength (float, optional): Discretization for planning MoveHandStraight, in seconds.
            plannername (str, optional):
            workminimumcompletetime (float, optional): (DEPRECATED, UNUSED) Set to trajduration - 0.016s. EMU_MUJIN example requires at least this much
            workminimumcompleteratio (float, optional): (DEPRECATED, UNUSED) In case the duration of the trajectory is now known, can specify in terms of [0,1]. 1 is complete everything.
            numspeedcandidates (int, optional): If speed/accel are not specified, the number of candiates to consider
            workignorefirstcollisionee (float, optional): time, necessary in case initial is in collision, has to be multiples of step length?
            workignorelastcollisionee (float, optional): time, necessary in case goal is in collision, has to be multiples of step length?
            workignorefirstcollision (float, optional):
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotaccelmult:
            ionames:
            ignoreGrabbingTarget (bool, optional):
            currentlimitratios (list, optional): The joints' current limt ratios.
            instobjectname (str, optional): If goaltype is not set and both instobjectname and ikparamname are set, use ikparamname of instobjectname as target position.
            ikparamname (str, optional): If goaltype is not set and both instobjectname and ikparamname are set, use ikparamname of instobjectname as target position.
            execute:
            moveStraightParams (dict, optional): Parameters used for linear movement like grasp approach, grasp depart, etc.
        """
        taskparameters = {
            'command': 'MoveToolLinear',
            'goaltype': goaltype,
            'goals': goals,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotspeed=robotspeed, toolname=toolname, timeout=timeout)

    def MoveToHandPosition(self, goaltype, goals, toolname=None, envclearance=None, closegripper=0, robotspeed=None, robotaccelmult=None, timeout=10, **kwargs):
        """Computes the inverse kinematics and moves the manipulator to any one of the goals specified.

        Args:
            goaltype (str): Type of the goal, e.g. translationdirection5d
            goals (list): Flat list of goals, e.g. two 5d ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]
            toolname (str, optional): Name of the manipulator. Defaults to currently selected tool
            envclearance (float, optional): Environment clearance in millimeters
            closegripper (bool, optional): Whether to close gripper once the goal is reached. (Default: 0)
            robotspeed (float, optional): Value in (0,1] setting the percentage of robot speed to move at
            robotaccelmult (float, optional): Value in (0,1] setting the percentage of robot acceleration to move at
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            ionames:
            minimumgoalpaths (int, optional): Number of solutions the planner must provide before it is allowed to finish.
            chuckgripper (bool, optional):
            currentlimitratios (list, optional): The joints' current limt ratios.
            instobjectname (str, optional): If goaltype is not set and both instobjectname and ikparamname are set, use ikparamname of instobjectname as target position.
            ikparamname (str, optional): If goaltype is not set and both instobjectname and ikparamname are set, use ikparamname of instobjectname as target position.
            ikparamoffset (list, optional):
            pathPlannerParameters:
            smootherParameters:
            ignoreGrabbingTarget (bool, optional):
            jitter (float, optional):
            maxJitterLinkDist:
            execute:
            filtertraj (bool, optional):
            executionFilterFactor (float, optional):
            departOffsetDir (list, optional): Direction in which to apply the offset when departing from the pick/place operation.
            departOffsetAwayFromGravity (float, optional): Overridden by departOffsetDir
            departAccel (float, optional):
            moveStraightParams (dict, optional): Parameters used for linear movement like grasp approach, grasp depart, etc.
        """
        taskparameters = {
            'command': 'MoveToHandPosition',
            'goaltype': goaltype,
            'goals': goals,
            'closegripper': closegripper,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotspeed=robotspeed, robotaccelmult=robotaccelmult, envclearance=envclearance, toolname=toolname, timeout=timeout)

    def UpdateObjects(self, envstate, targetname=None, state=None, unit="mm", timeout=10, **kwargs):
        """Updates objects in the scene with the envstate

        Args:
            envstate: A list of dictionaries for each instance object in world frame. Quaternion is specified in w,x,y,z order. e.g. [{'name': 'target_0', 'translation_': [1,2,3], 'quat_': [1,0,0,0], 'object_uri':'mujin:/asdfas.mujin.dae'}, {'name': 'target_1', 'translation_': [2,2,3], 'quat_': [1,0,0,0]}]
            targetname (str, optional): Name of the target object
            state (dict, optional):
            unit (str, optional): The unit of the given values. (Default: 'mm')
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            callerid (str, optional): The name of the caller (only used internally)
            detectionResultState (dict, optional): Information about the detected objects (received from detectors)
            targetUpdateNamePrefix (str, optional):
            cameranames (list, optional):
            countOverlappingPoints (bool, optional):
            overlapUpAxis (list, optional):
            zthresholdmult (float, optional):
            addUnpickableRegionAcrossShortEdgeDist (bool, optional):
            sizeRoundUp (bool, optional): If False, then round down. (Default: True)
            sizePrecisionXYZ (list, optional): mm (x,y,z) for rounding up incoming boxes from the detector. This allows previous grasping models to be cached and re-used since the sizes will be multiples of the current precision.
            points (list, optional): The point cloud passed in along with the detection results. Used in selective cases to count point overlap of random box.
            pointsize (float, optional): Size of points in the point cloud.
            pointcloudid (str, optional):
            locationName (str, optional): Name of the location to update.
            containerName (str, optional): Name of the container to update. Requires locationName to be set. If containerName is empty, will use the container in locationName.
            locationContainerId (str, optional):
            isFromStateSlaveNotify (bool, optional):
            imageStartTimeStampMS (int, optional):
            imageEndTimeStampMS (int, optional):
            belowBoxOverlap (float, optional): mm, Threshold on how much to ignore the relative heights of two neighboring targets to determine if the candidate is *below* the current pickup target. Positive value the pickup target is allowed to be under the other non-pickup targets by this amount, and still be pickable. When two targets are deemed to be overlapping on the face orthogonal to overlapUpAxis based on neighOverlapThresh, then check the heights of the targets to make sure that one target is really above the other. Sometimes detection error can cause two targets on the same height to be overlapped a little, but that doesn't mean that one target is on top of the other. (Default: 0)
            ignoreOverlapPointsFromWall (float, optional): mm, distance from the container inner walls within which pointcloud points do not count towards overlapping points (Default: 0)
            ignoreOverlapPointsFromNearbyTargets (float, optional): mm, amount of target extents reduction when counting the number of overlapping pointcloud points. This is so that pointcloud near the edges of the target (can come from noises from nearby targets, for example) can be ignored. (Default: 0)
            castPointCloudShadowFromCamera (bool, optional): If True, bottom parts of pointcloud obstacle are generated by casting shadow from camera. otherwise, vertical down (-z).
            pointsProjectedDirection (list, optional): The negative direction in which the points were projected when creating the obstacles. If specified, then take into account when computing the overlap. When container up is +Z, then pointsProjectedDirection will be (0,0,1).
            randomBoxOrigin (list, optional): Specifies where to place the origin of the incoming box detections. By default, this is [0,0,1], which means the origin will be at the center of the +Z (top) face.
            rollStepDegree (float, optional): Step of 6D grasp rotation around z axis in degrees, defaults to 45 degrees. (Default: 90)
            clampToContainer (bool, optional): If True, crop to container dimensions.
            medianFilterHalfSize (float, optional): If clampcontainer is True, this is used for filtering.
            useEmptyRegionForCropping (bool, optional): If clampcontainer is True, this is used for filtering.
            cropContainerMarginsXYZXYZ (list, optional): Margin defining an axis aligned bounding box to limit point cloud data for the container. Values are measured from the interior of container edges. Positive value means cropping, negative value means additional margin. 
            ioSignalsInfo (dict, optional): Struct for dictating if any IO signals should be written on receiving detection results
            addPointOffsetInfo (dict, optional): Special offsets from pointcloud
        """
        taskparameters = {
            'command': 'UpdateObjects',
            'envstate': envstate,
            'unit': unit,
        }
        if targetname is not None:
            taskparameters['object_uri'] = u'mujin:/%s.mujin.dae' % (targetname)
        taskparameters.update(kwargs)
        if state is not None:
            taskparameters['state'] = json.dumps(state)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def Grab(self, targetname, toolname=None, timeout=10, **kwargs):
        """Grabs an object with tool

        Args:
            targetname (str): Name of the target object
            toolname (str, optional): Name of the manipulator. Defaults to currently selected tool
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
        """
        taskparameters = {
            'command': 'Grab',
            'targetname': targetname,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout)

    def Release(self, targetname, timeout=10, **kwargs):
        """Releases a grabbed object.

        Args:
            targetname (str): Name of the target object
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
        """
        taskparameters = {
            'command': 'Release',
            'targetname': targetname,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetGrabbed(self, timeout=10, **kwargs):
        """Gets the names of the objects currently grabbed

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)

        Returns:
            dict: Names of the grabbed object in a JSON dictionary, e.g. {'names': ['target_0']}
        """
        taskparameters = {
            'command': 'GetGrabbed',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetTransform(self, targetname, connectedBodyName='', linkName='', geometryName='', geometryPk='', unit='mm', timeout=10, **kwargs):
        """Gets the transform of an object

        Args:
            targetname (str): OpenRave Kinbody name
            connectedBodyName (str, optional): OpenRave connected body name
            linkName (str, optional): OpenRave link name
            geometryName (str, optional): OpenRave geometry id name
            geometryPk (str, optional): OpenRave geometry primary key (pk)
            unit (str, optional): The unit of the given values. (Default: 'mm')
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)

        Returns:
            Transform of the object in a json dictionary, e.g. {'translation': [100,200,300], 'rotationmat': [[1,0,0],[0,1,0],[0,0,1]], 'quaternion': [1,0,0,0]}

        """
        taskparameters = {
            'command': 'GetTransform',
            'targetname': targetname,
            'connectedBodyName': connectedBodyName,
            'linkName': linkName,
            'geometryName': geometryName,
            'geometryPk': geometryPk,
            'unit': unit,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def SetTransform(self, targetname, translation, unit='mm', rotationmat=None, quaternion=None, timeout=10, **kwargs):
        """Sets the transform of an object. Rotation can be specified by either quaternion or rotation matrix.

        Args:
            targetname (str): Name of the target object
            translation (list): List of x,y,z values of the object in millimeters.
            unit (str, optional): The unit of the given values. (Default: 'mm')
            rotationmat (list, optional): List specifying the rotation matrix in row major format, e.g. [1,0,0,0,1,0,0,0,1]
            quaternion (list, optional): List specifying the quaternion in w,x,y,z format, e.g. [1,0,0,0].
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
        """
        taskparameters = {
            'command': 'SetTransform',
            'targetname': targetname,
            'translation': translation,
            'unit': unit,
        }
        taskparameters.update(kwargs)
        if rotationmat is not None:
            taskparameters['rotationmat'] = rotationmat
        if quaternion is not None:
            taskparameters['quaternion'] = quaternion
        if rotationmat is None and quaternion is None:
            taskparameters['quaternion'] = [1, 0, 0, 0]
            log.warn('no rotation is specified, using identity quaternion')
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetOBB(self, targetname, unit='mm', timeout=10, **kwargs):
        """Get the oriented bounding box (OBB) of object.

        Args:
            targetname (str): Name of the object
            unit (str, optional): The unit of the given values. (Default: 'mm')
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            linkname (str, optional): Name of link to use for OBB. If not specified, uses entire target.

        Returns:
            dict: A dict describing the OBB of the object with keys: extents, boxLocalTranslation, originalBodyTranslation, quaternion, rotationmat, translation
        """
        taskparameters = {
            'command': 'GetOBB',
            'targetname': targetname,
            'unit': unit,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def GetInnerEmptyRegionOBB(self, targetname, linkname=None, unit='mm', timeout=10, **kwargs):
        """Get the inner empty oriented bounding box (OBB) of a container.

        Args:
            targetname (str): Name of the object
            linkname (str, optional): Name of link to use for OBB. If not specified, uses entire target.
            unit (str, optional): The unit of the given values. (Default: 'mm')
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)

        Returns:
            dict: A dict describing the OBB of the object with keys: extents, boxLocalTranslation, originalBodyTranslation, quaternion, rotationmat, translation
        """
        taskparameters = {
            'command': 'GetInnerEmptyRegionOBB',
            'targetname': targetname,
            'unit': unit,
        }
        if linkname is not None:
            taskparameters['linkname'] = linkname
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def GetInstObjectAndSensorInfo(self, instobjectnames=None, sensornames=None, unit='mm', timeout=10, **kwargs):
        """Returns information about the inst objects and sensors that are a part of those inst objects.

        Args:
            instobjectnames (list, optional):
            sensornames (list, optional):
            unit (str, optional): The unit of the given values. (Default: 'mm')
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            ignoreMissingObjects (bool, optional): If False, will raise an error if the object is not found in the scene. Default: True.
        """
        taskparameters = {
            'command': 'GetInstObjectAndSensorInfo',
            'unit': unit,
        }
        if instobjectnames is not None:
            taskparameters['instobjectnames'] = instobjectnames
        if sensornames is not None:
            taskparameters['sensornames'] = sensornames
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def GetInstObjectInfoFromURI(self, instobjecturi=None, unit='mm', timeout=10, **kwargs):
        """Opens a URI and returns info about the internal/external and geometry info from it.

        Args:
            instobjecturi (str, optional):
            unit (str, optional): The unit of the given values. (Default: 'mm')
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            instobjectpose (list, optional): Pose to be assigned to the retrieved object. 7-element list
        """
        taskparameters = {
            'command': 'GetInstObjectInfoFromURI',
            'unit': unit,
        }
        if instobjecturi is not None:
            taskparameters['objecturi'] = instobjecturi
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def GetAABB(self, targetname, unit='mm', timeout=10, **kwargs):
        """Gets the axis-aligned bounding box (AABB) of an object.

        Args:
            targetname (str): Name of the object
            unit (str, optional): The unit of the given values. (Default: 'mm')
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            linkname (str, optional): Name of link to use for the AABB. If not specified, uses entire target.

        Returns:
            dict: AABB of the object, e.g. {'pos': [1000,400,100], 'extents': [100,200,50]}
        """
        taskparameters = {
            'command': 'GetAABB',
            'targetname': targetname,
            'unit': unit,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def SetLocationTracking(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Resets the tracking of specific containers

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            cycleIndex: The cycle index to track the locations for
            locationReplaceInfos: A dict that should have the keys: name, containerDynamicProperties, rejectContainerIds, uri, pose, cycleIndex
            removeLocationNames (list, optional):
            doRemoveOnlyDynamic: 
            minRobotBridgeTimeStampUS (int, optional): The minimum expected time stamp.
            dynamicObstacleBaseName (str, optional):
            targetUpdateBaseName (str, optional):
            ioSignalsInfo (dict, optional): Struct for dictating if any IO signals should be written on receiving detection results
            unit (str, optional): The unit of the given values. (Default: 'mm')
        """
        taskparameters = {
            'command': 'SetLocationTracking',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def ResetLocationTracking(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Resets tracking updates for locations

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            resetAllLocations (bool, optional): If True, then will reset all the locations
            resetLocationName (str, optional): Resets only the location with matching name
            resetLocationNames (list, optional): Resets only locations with matching name
            checkIdAndResetLocationName: (locationName, containerId) - only reset the location if the container id matches

        Returns:
            clearedLocationNames
        """
        taskparameters = {
            'command': 'ResetLocationTracking',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)['clearedLocationNames']
    
    def GetLocationTrackingInfos(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Gets the active tracked locations

        Args:
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)

        Returns:
            dict: activeLocationTrackingInfos
        """
        taskparameters = {
            'command': 'GetLocationTrackingInfos',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)['activeLocationTrackingInfos']
    
    def UpdateLocationContainerIdType(self, locationName, containerName, containerId, containerType, trackingCycleIndex=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Resets the tracking of specific containers

        Args:
            locationName (str): Name of the location the container is in
            containerName (str): Name of the container
            containerId (str): ID of the container
            containerType (str): Type of the container
            trackingCycleIndex: If specified, then the cycle with same cycleIndex will update location tracking in the same call.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            unit (str, optional): The unit of the given values. (Default: 'mm')
        """
        taskparameters = {
            'command': 'UpdateLocationContainerIdType',
            'locationName': locationName,
            'containerName': containerName,
            'containerId': containerId,
            'containerType': containerType,
        }
        if trackingCycleIndex is not None:
            taskparameters['trackingCycleIndex'] = trackingCycleIndex
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def ResetLocationTrackingContainerId(self, locationName, checkContainerId, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Resets the containerId of self._activeLocationTrackingInfos if it matches checkContainerId.

        Args:
            locationName (str): The name of the location that may be reset.
            checkContainerId: If checkContainerId is specified and not empty and it matches the current containerId of the tracking location, then reset the current tracking location
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
        """
        taskparameters = {
            'command': 'ResetLocationTrackingContainerId',
            'locationName': locationName,
            'checkContainerId': checkContainerId,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def RemoveObjectsWithPrefix(self, prefix=None, removeNamePrefixes=None, timeout=10, usewebapi=None, fireandforget=False, removeLocationNames=None, **kwargs):
        """Removes objects with prefix.

        Args:
            prefix (str, optional): (DEPRECATED)
            removeNamePrefixes (list, optional): Names of prefixes to match with when removing items
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            removeLocationNames (list, optional):
            doRemoveOnlyDynamic (bool): If True, then remove objects that were added through dynamic means like UpdateObjects/UpdateEnvironmentState

        Returns:
            dict: With key 'removedBodyNames' for the removed object names
        """
        taskparameters = {
            'command': 'RemoveObjectsWithPrefix',
        }
        taskparameters.update(kwargs)
        if prefix is not None:
            log.warn('prefix is deprecated')
            taskparameters['prefix'] = prefix
        if removeNamePrefixes is not None:
            taskparameters['removeNamePrefixes'] = removeNamePrefixes
        if removeLocationNames is not None:
            taskparameters['removeLocationNames'] = removeLocationNames
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def GetTrajectoryLog(self, timeout=10, **kwargs):
        """Gets the recent trajectories executed on the binpicking server. The internal server keeps trajectories around for 10 minutes before clearing them.

        Args:
            startindex (int): Start of the trajectory to get. If negative, will start counting from the end. For example, -1 is the last element, -2 is the second to last.
            num (int): Number of trajectories from startindex to return. If 0 will return all the trajectories starting from startindex
            includejointvalues (bool, optional): If True, will include timedjointvalues. If False, will just give back the trajectories.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            saverawtrajectories (bool, optional): If True, will save the raw trajectories.

        Returns:
            dict: With structure:
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
                
                Where timedjointvalues is a list of joint values and the trajectory time. For a 3DOF robot sampled at 0.008s, this is
                [J1, J2, J3, 0, J1, J2, J3, 0.008, J1, J2, J3, 0.016, ...]
        """
        taskparameters = {
            'command': 'GetTrajectoryLog',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ChuckGripper(self, robotname=None, grippername=None, timeout=10, usewebapi=None, **kwargs):
        """Chucks the manipulator

        Args:
            robotname (str, optional): Name of the robot
            grippername (str, optional): Name of the gripper.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            toolname (str, optional): Name of the manipulator. Defaults to currently selected tool
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'ChuckGripper',
            'grippername': grippername,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def UnchuckGripper(self, robotname=None, grippername=None, timeout=10, usewebapi=None, **kwargs):
        """Unchucks the manipulator and releases the target

        Args:
            robotname (str, optional): Name of the robot
            grippername (str, optional): Name of the gripper.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            targetname (str): Name of the target object.
            toolname (str, optional): Name of the manipulator. Defaults to currently selected tool
            pulloutdist (float, optional): Distance to move away along the tool direction after releasing.
            deletetarget (int, optional): If 1, removes the target object from the environment after releasing. (Default: 1)
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'UnchuckGripper',
            'grippername': grippername,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def CalibrateGripper(self, robotname=None, grippername=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Goes through the gripper calibration procedure

        Args:
            robotname (str, optional): Name of the robot
            grippername (str, optional): Name of the gripper.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            toolname (str, optional): Name of the manipulator. Defaults to currently selected tool
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'CalibrateGripper',
            'grippername': grippername,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def StopGripper(self, robotname=None, grippername=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """

        Args:
            robotname (str, optional): Name of the robot
            grippername (str, optional): Name of the gripper.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            toolname (str, optional): Name of the manipulator. Defaults to currently selected tool
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'StopGripper',
            'grippername': grippername,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def MoveGripper(self, grippervalues, robotname=None, grippername=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Moves the chuck of the manipulator to a given value.

        Args:
            grippervalues (list): Target value(s) of the chuck.
            robotname (str, optional): Name of the robot
            grippername (str, optional): Name of the gripper.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            toolname (str, optional): Name of the manipulator. Defaults to currently selected tool
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'MoveGripper',
            'grippername': grippername,
            'grippervalues': grippervalues,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def ExecuteRobotProgram(self, robotProgramName, robotname=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Execute a robot specific program by name

        Args:
            robotProgramName (str):
            robotname (str, optional): Name of the robot
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'ExecuteRobotProgram',
            'robotProgramName': robotProgramName,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def SaveScene(self, timeout=10, **kwargs):
        """Saves the current scene to file

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            filename (str, optional): e.g. /tmp/testscene.mujin.dae, if not specified, it will be saved with an auto-generated filename
            preserveexternalrefs (bool, optional): If True, any bodies that are currently being externally referenced from the environment will be saved as external references.
            externalref (str, optional): If '*', then each of the objects will be saved as externally referencing their original filename. Otherwise will force saving specific bodies as external references.
            saveclone: If 1, will save the scenes for all the cloned environments
            saveReferenceUriAsHint (bool, optional): If True, use save the reference uris as referenceUriHint so that webstack does not get confused and deletes content

        Returns:
            dict: The filename the scene is saved to, in a json dictionary, e.g. {'filename': '2013-11-01-17-10-00-UTC.dae'}
        """
        taskparameters = {
            'command': 'SaveScene',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def SaveGripper(self, timeout=10, robotname=None, **kwargs):
        """Separate gripper from a robot in a scene and save it.

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            robotname (str, optional): Name of the robot
            filename (str, optional): File name to save on the file system. e.g. /tmp/robotgripper/mujin.dae
            manipname (str, optional): Name of the manipulator.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
        """
        taskparameters = {
            'command': 'SaveGripper',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout)

    def MoveJointsToJointConfigurationStates(self, jointConfigurationStates, robotname=None, robotspeed=None, robotaccelmult=None, execute=1, startJointConfigurationStates=None, envclearance=None, timeout=10, usewebapi=True, **kwargs):
        """Moves the robot to desired joint angles specified in jointStates

        Args:
            jointConfigurationStates:
            robotname (str, optional): Name of the robot
            startJointConfigurationStates:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: True)
            jointStates (list, optional): List[{'jointName':str, 'jointValue':float}]
            jointindices (list, optional): List of corresponding joint indices, default is range(len(jointvalues))
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
            constraintToolDirection (list, optional):
            departOffsetDir (list, optional): Direction in which to apply the offset when departing from the pick/place operation.
            departOffsetAwayFromGravity (float, optional): Overridden by departOffsetDir
            trajname (str, optional):
            disablebodies (bool, optional):
            ignoreGrabbingTarget (bool, optional):
            jointthresh (float, optional):
            envclearance:
            jitter (float, optional):
            execute:
            executionFilterFactor (float, optional):
            filtertraj (bool, optional):
            currentlimitratios (list, optional): The joints' current limt ratios.
            goalJointThreshold (list, optional): Threshold of the sum of abs joint differences between what the robot is able to achieve and where the goal is, in degrees. If not within this threshold, robot tries to reach goal, during some time.
            goalWorkspaceThreshold (float, optional): Threshold in mm. If the robot manipulator is within this threshold to the goal position, then trajectory is assumed to be successful.
            calibrategripper (bool, optional):
            departAccel (float, optional):
            maxManipAccel (float, optional):
            maxJitterLinkDist:
        """
        taskparameters = {
            'command': 'MoveJointsToJointConfigurationStates',
            'goalJointConfigurationStates': jointConfigurationStates,
            'execute': execute,
        }

        if envclearance is not None:
            taskparameters['envclearance'] = envclearance

        if startJointConfigurationStates is not None:
            taskparameters['startJointConfigurationStates'] = startJointConfigurationStates

        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, robotspeed=robotspeed, robotaccelmult=robotaccelmult, timeout=timeout, usewebapi=usewebapi)

    def MoveJoints(self, jointvalues, jointindices=None, robotname=None, robotspeed=None, robotaccelmult=None, execute=1, startvalues=None, envclearance=None, timeout=10, usewebapi=True, **kwargs):
        """Moves the robot to desired joint angles specified in jointvalues

        Args:
            goaljoints (list): List of joint values to move to.
            jointindices (list, optional): List of corresponding joint indices, default is range(len(jointvalues))
            robotname (str, optional): Name of the robot
            startvalues (list, optional): The robot joint values to start the motion from.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: True)
            robotProgramName (str, optional):
            jointvalues (list): (DEPRECATED: use goaljoints) List of joint values to move to.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
            constraintToolDirection (list, optional):
            departOffsetDir (list, optional): Direction in which to apply the offset when departing from the pick/place operation.
            departOffsetAwayFromGravity (float, optional): Overridden by departOffsetDir
            trajname (str, optional):
            disablebodies (bool, optional):
            ignoreGrabbingTarget (bool, optional):
            jointthresh (float, optional):
            envclearance:
            jitter (float, optional):
            execute:
            executionFilterFactor (float, optional):
            filtertraj (bool, optional):
            currentlimitratios (list, optional): The joints' current limt ratios.
            goalJointThreshold (list, optional): Threshold of the sum of abs joint differences between what the robot is able to achieve and where the goal is, in degrees. If not within this threshold, robot tries to reach goal, during some time.
            goalWorkspaceThreshold (float, optional): Threshold in mm. If the robot manipulator is within this threshold to the goal position, then trajectory is assumed to be successful.
            calibrategripper (bool, optional):
            departAccel (float, optional):
            maxManipAccel (float, optional):
            maxJitterLinkDist:
            forceTorqueBasedEstimatorParameters (dict, optional): A set of parameters for force-torque based estimation.
        """
        if jointindices is None:
            jointindices = range(len(jointvalues))
            log.warn(u'No jointindices specified. Moving joints with default jointindices: %s', jointindices)

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
        return self.ExecuteCommand(taskparameters, robotname=robotname, robotspeed=robotspeed, robotaccelmult=robotaccelmult, timeout=timeout, usewebapi=usewebapi)
    
    def MoveJointsToPositionConfiguration(self, positionConfigurationName=None, positionConfigurationCandidateNames=None, robotname=None, robotspeed=None, robotaccelmult=None, execute=1, startvalues=None, envclearance=None, timeout=10, usewebapi=True, **kwargs):
        """Moves the robot to desired position configuration specified in positionConfigurationName
        
        Args:
            positionConfigurationName (str, optional): If specified, the name of position configuration to move to. If it does not exist, will raise an error.
            positionConfigurationCandidateNames (list, optional): If specified, goes to the first position that is defined for the robot. If no positions exist, returns without moving the robot.
            robotname (str, optional): Name of the robot
            startvalues (list, optional): The robot joint values to start the motion from.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: True)
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
            constraintToolDirection (list, optional):
            departOffsetDir (list, optional): Direction in which to apply the offset when departing from the pick/place operation.
            departOffsetAwayFromGravity (float, optional): Overridden by departOffsetDir
            trajname (str, optional):
            disablebodies (bool, optional):
            ignoreGrabbingTarget (bool, optional):
            jointthresh (float, optional):
            envclearance:
            jitter (float, optional):
            execute:
            executionFilterFactor (float, optional):
            filtertraj (bool, optional):
            currentlimitratios (list, optional): The joints' current limt ratios.
            goalJointThreshold (list, optional): Threshold of the sum of abs joint differences between what the robot is able to achieve and where the goal is, in degrees. If not within this threshold, robot tries to reach goal, during some time.
            goalWorkspaceThreshold (float, optional): Threshold in mm. If the robot manipulator is within this threshold to the goal position, then trajectory is assumed to be successful.
            calibrategripper (bool, optional):
            departAccel (float, optional):
            maxManipAccel (float, optional):
            maxJitterLinkDist:
            startJointConfigurationStates (list, optional): List of dicts for each joint.
            robotProgramName (str, optional):
            forceTorqueBasedEstimatorParameters (dict, optional): A set of parameters for force-torque based estimation.

        Returns:
            dictionary of keys: goalPositionName, goalConfiguration
        """
        taskparameters = {
            'command': 'MoveJointsToPositionConfiguration',
            'execute': execute,
        }
        if positionConfigurationName:
            taskparameters['positionConfigurationName'] = positionConfigurationName
        if positionConfigurationCandidateNames:
            taskparameters['positionConfigurationCandidateNames'] = positionConfigurationCandidateNames
        if envclearance is not None:
            taskparameters['envclearance'] = envclearance
        if startvalues is not None:
            taskparameters['startvalues'] = list(startvalues)
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, robotspeed=robotspeed, robotaccelmult=robotaccelmult, timeout=timeout, usewebapi=usewebapi)

    def GetRobotBridgeIOVariables(self, ioname=None, ionames=None, robotname=None, timeout=10, usewebapi=None, **kwargs):
        """Returns the data of the IO in ASCII hex as a string

        Args:
            ioname (str, optional): One IO name to read
            ionames (list, optional): A list of the IO names to read
            robotname (str, optional): Name of the robot
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
        """
        taskparameters = {
            'command': 'GetRobotBridgeIOVariables',
        }
        if ioname is not None and len(ioname) > 0:
            taskparameters['ioname'] = ioname
        if ionames is not None and len(ionames) > 0:
            taskparameters['ionames'] = ionames

        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def SetRobotBridgeIOVariables(self, iovalues, robotname=None, timeout=10, usewebapi=None, **kwargs):
        """Sets a set of IO variables in the robot bridge.

        This should not lock self.env since it can happen during the runtime of a task and lock out other functions waiting in the queue.

        Args:
            iovalues:
            robotname (str, optional): Name of the robot
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            forceasync (bool, optional):
        """
        taskparameters = {
            'command': 'SetRobotBridgeIOVariables',
            'iovalues': list(iovalues)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)
    
    def ComputeIkParamPosition(self, name, robotname=None, timeout=10, usewebapi=None, **kwargs):
        """Given the name of a kinbody, computes the manipulator in the kinbody frame to generate parameters for an ikparam

        Args:
            name (str):
            robotname (str, optional): Name of the robot
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            limit (int): Number of solutions to return
            ikparamnames (list[str]): The ikparameter names, also contains information about the grasp like the preshape
            targetname (str): The target object name that the ikparamnames belong to
            freeincvalue (float): The discretization of the free joints of the robot when computing ik.
            filteroptionslist (list[str]): A list of filter option strings. Can be: CheckEnvCollisions, IgnoreCustomFilters, IgnoreEndEffectorCollisions, IgnoreEndEffectorEnvCollisions, IgnoreEndEffectorSelfCollisions, IgnoreJointLimits, IgnoreSelfCollisions
            filteroptions (int): OpenRAVE IkFilterOptions bitmask. By default this is 1, which means all collisions are checked
        """
        taskparameters = {
            'command': 'ComputeIkParamPosition',
            'name': name,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def ComputeIKFromParameters(self, toolname=None, timeout=10, **kwargs):
        """

        Args:
            toolname (str, optional): Tool name
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            targetname (str, optional): Name of the target object
            graspsetname (str, optional): Name of the grasp set to use
            ikparamnames (list, optional): If graspset does not exist, use the ikparamnames to initialize the grasp.
            limit (float, optional): Number of solutions to return
            useSolutionIndices (bool, optional): 
            disabletarget (bool, optional): 
            unit (str, optional): The unit of the given values. (Default: mm)
            randomBoxInfo (dict, optional): info structure for maintaining grasp parameters for random box picking. Used when picking up randomized boxes (targetIsRandomBox is True), Keys are: usefaces, dictFacePriorities, boxDirAngle, toolTranslationOffsets
            freeincvalue (float, optional): The discretization of the free joints of the robot when computing ik.
            freeinc (float, optional): The discretization of the free joints of the robot when computing ik.
            applyapproachoffset (bool, optional):
            inPlaneAngleDeviation (float, optional):
            outOfPlaneAngleDeviation (float, optional):
            searchfreeparams (bool, optional):
            returnClosestToCurrent (bool, optional):
            filteroptionslist (list, optional): A list of filter option strings. Can be: CheckEnvCollisions, IgnoreCustomFilters, IgnoreEndEffectorCollisions, IgnoreEndEffectorEnvCollisions, IgnoreEndEffectorSelfCollisions, IgnoreJointLimits, IgnoreSelfCollisions. Overrides filteroptions.
            filteroptions (int, optional): OpenRAVE IkFilterOptions bitmask. By default this is 1, which means all collisions are checked

        Returns:
            A dictionary of:
            - solutions: array of IK solutions (each of which is an array of DOF values), sorted by minimum travel distance and truncated to match the limit
        """
        taskparameters = {
            'command': 'ComputeIKFromParameters',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout)

    def ReloadModule(self, timeout=10, **kwargs):
        """

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
        """
        taskparameters = {
            'command': 'ReloadModule',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ShutdownRobotBridge(self, timeout=10, **kwargs):
        """

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
        """
        taskparameters = {
            'command': 'ShutdownRobotBridge',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetRobotBridgeState(self, timeout=10, **kwargs):
        """

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            ionames (list, optional): A list of IO names to read/write
        """
        taskparameters = {
            'command': 'GetRobotBridgeState',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ClearRobotBridgeError(self, timeout=10, usewebapi=None, **kwargs):
        """

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
        """
        taskparameters = {
            'command': 'ClearRobotBridgeError',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)

    def SetRobotBridgePause(self, timeout=10, **kwargs):
        """

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
        """
        taskparameters = {
            'command': 'SetRobotBridgePause',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def SetRobotBridgeResume(self, timeout=10, **kwargs):
        """

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
        """
        taskparameters = {
            'command': 'SetRobotBridgeResume',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    #
    # jogging related
    #

    def SetJogModeVelocities(self, movejointsigns, robotname=None, toolname=None, robotspeed=None, robotaccelmult=None, canJogInCheckMode=None, usewebapi=False, timeout=1, fireandforget=False, **kwargs):
        """

        Args:
            movejointsigns (list): Joint signs used for jogging. If less than the number of joints, will be padded with zeros.
            robotname (str, optional): Name of the robot
            toolname (str, optional): Name of the manipulator. Defaults to self.toolname
            robotspeed (float, optional): Value in (0,1] setting the percentage of robot speed to move at
            robotaccelmult (float, optional): Value in (0,1] setting the percentage of robot acceleration to move at
            canJogInCheckMode (bool, optional): If True, then allow jogging even if in check mode. (Default: False)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 1)
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            jogtype (str, optional): One of 'joints', 'world', 'robot', 'tool'. (DEPRECATED: set this as a field in robotJogParameters instead)
            checkSelfCollisionWhileJogging (bool, optional):
            force (bool, optional): If true, forces the velocities to be set.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotJogParameters (dict, optional): A dictionary. Includes field 'jogtype' (One of 'joints', 'world', 'robot', 'tool').
            simulationtimestep (float, optional): Time step of the simulation.
            plotDirection (bool, optional): If True, plot the direction.
        """
        taskparameters = {
            'command': 'SetJogModeVelocities',
            'movejointsigns': movejointsigns,
        }
        if canJogInCheckMode is not None:
            taskparameters['canJogInCheckMode'] = canJogInCheckMode
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, toolname=toolname, robotspeed=robotspeed, robotaccelmult=robotaccelmult, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def EndJogMode(self, usewebapi=False, timeout=1, fireandforget=False, **kwargs):
        """

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 1)
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
        """
        taskparameters = {
            'command': 'EndJogMode',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def SetRobotBridgeServoOn(self, servoon, robotname=None, timeout=3, fireandforget=False):
        """

        Args:
            servoon (bool): If True, turns servo on.
            robotname (str, optional): Name of the robot
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 3)
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
        """
        taskparameters = {
            'command': 'SetRobotBridgeServoOn',
            'isservoon': servoon
        }
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, fireandforget=fireandforget)

    def SetRobotBridgeLockMode(self, islockmode, robotname=None, timeout=3, fireandforget=False, usewebapi=False):
        """

        Args:
            islockmode (bool): If True, turns on Lock Mode. During Lock Mode, all communication with the physical robot is turned off and the hardware will not move.
            robotname (str, optional): Name of the robot
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 3)
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
        """
        taskparameters = {
            'command': 'SetRobotBridgeLockMode',
            'islockmode': islockmode,
        }
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, fireandforget=fireandforget, usewebapi=usewebapi)

    def ResetSafetyFault(self, timeout=3, fireandforget=False):
        """

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 3)
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
        """
        taskparameters = {
            'command': 'ResetSafetyFault',
        }
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def SetRobotBridgeControlMode(self, controlMode, timeout=3, fireandforget=False):
        """

        Args:
            controlMode (str): The control mode to use, e.g. "Manual".
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 3)
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
        """
        taskparameters = {
            'command': 'SetRobotBridgeControlMode',
            'controlMode': controlMode,
        }
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def GetDynamicObjects(self, usewebapi=False, timeout=1, **kwargs):
        """Get a list of dynamically added objects in the scene, from vision detection and physics simulation.

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 1)
        """
        taskparameters = {
            'command': 'GetDynamicObjects',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def ComputeRobotConfigsForGraspVisualization(self, targetname, graspname, robotname=None, toolname=None, unit='mm', usewebapi=False, timeout=10, **kwargs):
        """Returns robot configs for grasp visualization

        Args:
            targetname (str): Target object's name.
            graspname (str): Name of the grasp for which to visualize grasps.
            robotname (str, optional): Name of the robot
            toolname (str, optional): Name of the manipulator. (Default: 'self.toolname')
            unit (str, optional): The unit of the given values. (Default: 'mm')
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            approachoffset (float, optional):
            departoffsetdir (list, optional): Direction in which to apply the offset when departing from the pick/place operation.
            departoffsetintool (list, optional):
            shadowrobotname (str, optional):
            shadowrobottoolname (str, optional):
        """
        taskparameters = {
            'command': 'ComputeRobotConfigsForGraspVisualization',
            'targetname': targetname,
            'graspname': graspname
        }
        if unit is not None:
            taskparameters['unit'] = unit
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, toolname=toolname, usewebapi=usewebapi, timeout=timeout)

    def ResetCacheTemplates(self, usewebapi=False, timeout=1, fireandforget=False, **kwargs):
        """Resets any cached templates

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 1)
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
        """
        taskparameters = {
            'command': 'ResetCacheTemplates',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def SetRobotBridgeExternalIOPublishing(self, enable, usewebapi=False, timeout=2, fireandforget=False, **kwargs):
        """Enables publishing collision data to the robotbridge

        Args:
            enable (bool): If True, collision data will be published to robotbridge.
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2)
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
        """
        taskparameters = {
            'command': 'SetRobotBridgeExternalIOPublishing',
            'enable': bool(enable)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def RestoreSceneInitialState(self, usewebapi=None, timeout=1, **kwargs):
        """Restore scene to the state on filesystem

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional):  (Default: 1)
        """
        taskparameters = {
            'command': 'RestoreSceneInitialState',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    #
    # Motor test related.
    #

    def RunMotorControlTuningStepTest(self, jointName, amplitude, timeout=10, usewebapi=False, **kwargs):
        """Runs step response test on specified joint and returns result

        Args:
            jointName (str): The name of the joint.
            amplitude (float): The amplitude.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            kwargs:
        """
        taskparameters = {
            'command': 'RunMotorControlTuningStepTest',
            'jointName': jointName,
            'amplitude': amplitude,
        }
        taskparameters.update(kwargs)
        log.warn('sending taskparameters=%r', taskparameters)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def RunMotorControlTuningMaximulLengthSequence(self, jointName, amplitude, timeout=10, usewebapi=False, **kwargs):
        """Runs maximum length sequence test on specified joint and returns result

        Args:
            jointName (str): The name of the joint.
            amplitude (float): The amplitude.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'RunMotorControlTuningMaximulLengthSequence',
            'jointName': jointName,
            'amplitude': amplitude,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def RunMotorControlTuningDecayingChirp(self, jointName, amplitude, freqMax, timeout=120, usewebapi=False, **kwargs):
        """runs chirp test on specified joint and returns result

        Args:
            jointName (str): The name of the joint.
            amplitude (float): The amplitude.
            freqMax (float): The maximum frequency in Hz
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 120)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'RunMotorControlTuningDecayingChirp',
            'jointName': jointName,
            'amplitude': amplitude,
            'freqMax': freqMax,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def RunMotorControlTuningGaussianImpulse(self, jointName, amplitude, timeout=20, usewebapi=False, **kwargs):
        """Runs Gaussian Impulse test on specified joint and returns result

        Args:
            jointName (str): The name of the joint.
            amplitude (float): The amplitude.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 20)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'RunMotorControlTuningGaussianImpulse',
            'jointName': jointName,
            'amplitude': amplitude,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def RunMotorControlTuningBangBangResponse(self, jointName, amplitude, timeout=60, usewebapi=False, **kwargs):
        """Runs bangbang trajectory in acceleration or jerk space and returns result

        Args:
            jointName (str): The name of the joint.
            amplitude (float): The amplitude.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 60)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'RunMotorControlTuningBangBangResponse',
            'jointName': jointName,
            'amplitude': amplitude,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def RunDynamicsIdentificationTest(self, timeout, usewebapi=False, **kwargs):
        """

        Args:
            timeout (float): Time in seconds after which the command is assumed to have failed. (Default: 4.0)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'RunDynamicsIdentificationTest',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetTimeToRunDynamicsIdentificationTest(self, usewebapi=False, timeout=10, **kwargs):
        """

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            jointName (str, optional): The name of the joint.
            minJointAngle (float, optional): The joint angle to start the dynamics identification test at.
            maxJointAngle (float, optional): The joint angle to finish the dynamics identification test at.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'GetTimeToRunDynamicsIdentificationTest',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetInertiaChildJointStartValues(self, usewebapi=False, timeout=10, **kwargs):
        """

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            kwargs:
        """
        taskparameters = {
            'command': 'GetInertiaChildJointStartValues',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def CalculateTestRangeFromCollision(self, usewebapi=False, timeout=10, **kwargs):
        """

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            jointName (str, optional): The name of the joint.
            unit (str, optional): The unit of the given values. (Default: 'mm')
            envclearance (float, optional): Environment clearance in millimeters
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'CalculateTestRangeFromCollision',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetMotorControlParameterSchema(self, usewebapi=False, timeout=10, **kwargs):
        """Gets motor control parameter schema

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
        """
        taskparameters = {
            'command': 'GetMotorControlParameterSchema',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetMotorControlParameter(self, jointName, parameterName, usewebapi=False, timeout=10, **kwargs):
        """Gets motor control parameters as a name-value dict, e.g.: {'J1':{'KP':1}, 'J2':{'KV':2}}

        Args:
            jointName (str):
            parameterName (str):
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'GetMotorControlParameter',
            'jointName': jointName,
            'parameterName': parameterName,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetMotorControlParameters(self, usewebapi=False, timeout=10, **kwargs):
        """Gets cached motor control parameters as name-value dict

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
        """
        taskparameters = {
            'command': 'GetMotorControlParameters',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def SetMotorControlParameter(self, jointName, parameterName, parameterValue, timeout=10, usewebapi=False, **kwargs):
        """Sets motor control parameter

        Args:
            jointName (str):
            parameterName (str): The name of the parameter to set.
            parameterValue: The value to assign to the parameter.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
            robotspeed:
            robotaccelmult:
            ionames:
        """
        taskparameters = {
            'command': 'SetMotorControlParameter',
            'jointName': jointName,
            'parameterName': parameterName,
            'parameterValue': parameterValue,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def IsProfilingRunning(self, timeout=10, usewebapi=False):
        """Queries if profiling is running on planning

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
        """
        taskparameters = {
            'command': 'IsProfilingRunning',
        }
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)

    def StartProfiling(self, clocktype='cpu', timeout=10, usewebapi=False):
        """Start profiling planning

        Args:
            clocktype (str, optional): (Default: 'cpu')
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
        """
        taskparameters = {
            'command': 'StartProfiling',
            'clocktype': clocktype,
        }
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)

    def StopProfiling(self, timeout=10, usewebapi=False):
        """Stop profiling planning

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
        """
        taskparameters = {
            'command': 'StopProfiling',
        }
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)

    def ReplaceBodies(self, bodieslist, timeout=10, **kwargs):
        """Replaces bodies in the environment with new uris

        Args:
            bodieslist:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            replaceInfos (list, optional): list of dicts with keys: name, uri, containerDynamicProperties
            testLocationName (str, optional): If specified, will test if the container in this location matches testLocationContainerId, and only execute the replace if it matches and testLocationContainerId is not empty.
            testLocationContainerId (str, optional): containerId used for testing logic with testLocationName
            removeNamePrefixes (list, optional): Names of prefixes to match with when removing items
            removeLocationNames (list, optional):
            doRemoveOnlyDynamic (bool, optional): If True, then remove objects that were added through dynamic means like UpdateObjects/UpdateEnvironmentState
            unit (str, optional): The unit of the given values. (Default: 'mm')
        """
        taskparameters = {
            'command': 'ReplaceBodies',
            'bodieslist': bodieslist, # for back compatibility for now
            'replaceInfos': bodieslist,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def GetState(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 4.0)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
            unit:
            robotBridgeConnectionInfo:
            locationCollisionInfos (dict, optional): List of external collision IOs to be computed and sent in realtime.
        """
        taskparameters = {
            'command': 'GetState',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def EnsureSyncWithRobotBridge(self, syncTimeStampUS, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Ensures that planning has synchronized with robotbridge data that is newer than syncTimeStampUS

        Args:
            syncTimeStampUS: us (microseconds, linux time) of the timestamp
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
        """
        taskparameters = {
            'command': 'EnsureSyncWithRobotBridge',
            'syncTimeStampUS': syncTimeStampUS,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def ResetCachedRobotConfigurationState(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Resets cached robot configuration (position of the robot) in the planning slave received from slave notification. Need to perform every time robot moved not from the task slaves.

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional): If True, does not wait for the command to finish and returns immediately. The command remains queued on the server.
        """
        taskparameters = {
            'command': 'ResetCachedRobotConfigurationState',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
