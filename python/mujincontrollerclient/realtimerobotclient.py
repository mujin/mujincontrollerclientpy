# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc

from . import json
from . import planningclient

import logging
log = logging.getLogger(__name__)

class RealtimeRobotControllerClient(planningclient.PlanningControllerClient):
    """Mujin controller client for realtimerobot task"""
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
            robotspeed (float, optional):
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'ExecuteTrajectory',
                          'trajectory': trajectoryxml,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)

    def GetJointValues(self, timeout=10, **kwargs):
        """Gets the current robot joint values

        Args:
            timeout (float, optional):  (Default: 10)
        
        Returns:
            dict: Current joint values in a json dictionary with currentjointvalues: [0,0,0,0,0,0]
        """
        taskparameters = {'command': 'GetJointValues'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def MoveToolLinear(self, goaltype, goals, toolname=None, timeout=10, robotspeed=None, **kwargs):
        """Moves the tool linear

        Args:
            goaltype (str): Type of the goal, e.g. translationdirection5d
            goals (list[float]): Flat list of goals, e.g. two 5D ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]
            toolname (str, optional): Name of the manipulator. Default: self.toolname
            timeout (float, optional):  (Default: 10)
            robotspeed (float, optional):
            workmaxdeviationangle (float): How much the tool tip can rotationally deviate from the linear path. In deg.
            workspeed (float): [anglespeed, transspeed] in deg/s and mm/s
            workaccel (float): [angleaccel, transaccel] in deg/s^2 and mm/s^2
            worksteplength (float): Discretization for planning MoveHandStraight, in seconds.
            plannername (str):
            numspeedcandidates (int): If speed/accel are not specified, the number of candiates to consider
            workignorefirstcollisionee (float): time, necessary in case initial is in collision, has to be multiples of step length?
            workignorelastcollisionee (float): time, necessary in case goal is in collision, has to be multiples of step length?
            workignorefirstcollision (float):
        """
        taskparameters = {'command': 'MoveToolLinear',
                          'goaltype': goaltype,
                          'goals': goals,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotspeed=robotspeed, toolname=toolname, timeout=timeout)

    def MoveToHandPosition(self, goaltype, goals, toolname=None, envclearance=None, closegripper=0, robotspeed=None, robotaccelmult=None, timeout=10, **kwargs):
        """Computes the inverse kinematics and moves the manipulator to any one of the goals specified.

        Args:
            goaltype (str): Type of the goal, e.g. translationdirection5d
            goals (list[float]): Flat list of goals, e.g. two 5d ik goals: [380,450,50,0,0,1, 380,450,50,0,0,-1]
            toolname (str, optional): Name of the manipulator. Default: self.toolname
            envclearance (float): Clearance in millimeter. Default: self.envclearances
            closegripper: Whether to close gripper once the goal is reached. Default: 0
            robotspeed (float, optional):
            robotaccelmult (float, optional):
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'MoveToHandPosition',
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
            targetname (optional):
            state (optional):
            unit (str, optional): Unit of envstate. Default: mm
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'UpdateObjects',
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
            targetname (str): Name of the object
            toolname (str, optional): Name of the manipulator. Default: self.toolname
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'Grab',
                          'targetname': targetname,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout)

    def Release(self, targetname, timeout=10, **kwargs):
        """Releases a grabbed object.

        Args:
            targetname (str): Name of the object
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'Release',
                          'targetname': targetname,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetGrabbed(self, timeout=10, **kwargs):
        """Gets the names of the objects currently grabbed

        Args:
            timeout (float, optional):  (Default: 10)

        Returns:
            dict: Names of the grabbed object in a JSON dictionary, e.g. {'names': ['target_0']}
        """
        taskparameters = {'command': 'GetGrabbed',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetTransform(self, targetname, connectedBodyName='', linkName='', geometryName='', geometryPk='', unit='mm', timeout=10, **kwargs):
        """Gets the transform of an object

        Args:
            targetname (str): OpenRave kinbody name
            connectedBodyName (str, optional): OpenRave connected body name
            linkName (str, optional): OpenRave link name
            geometryName (str, optional): OpenRave geometry id name
            geometryPk (str, optional): OpenRave geometry primary key (pk)
            unit (str, optional): Unit of the result translation (Default: 'mm')
            timeout (float, optional):  (Default: 10)

        Returns:
            dict: Transform of the object in a json dictionary, e.g. {'translation': [100,200,300], 'rotationmat': [[1,0,0],[0,1,0],[0,0,1]], 'quaternion': [1,0,0,0]}
        """

        taskparameters = {'command': 'GetTransform',
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
        """Sets the transform of an object

        Args:
            targetname (str): Name of the object
            translation (list[float]): List of x,y,z value of the object in millimeters
            unit (str, optional): Unit of translation (Default: 'mm')
            rotationmat (list[float], optional): List specifying the rotation matrix in row major format, e.g. [1,0,0,0,1,0,0,0,1]
            quaternion (list[float], optional): List specifying the quaternion in w,x,y,z format, e.g. [1,0,0,0]
            timeout (float, optional):  (Default: 10)
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
            log.warn('no rotation is specified, using identity quaternion')
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetOBB(self, targetname, unit='mm', timeout=10, **kwargs):
        """Get the oriented bounding box (OBB) of object.

        Args:
            targetname (str): Name of the object
            unit (str, optional): Unit of the OBB. Default: mm
            timeout (float, optional):  (Default: 10)
            linkname (str, optional): Name of link to use for AABB. If not specified, uses entire target.

        Returns:
            dict: A dict describing the OBB of the object with keys: extents, boxLocalTranslation, originalBodyTranslation, quaternion, rotationmat, translation
        """
        taskparameters = {'command': 'GetOBB',
                          'targetname': targetname,
                          'unit': unit,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def GetInnerEmptyRegionOBB(self, targetname, linkname=None, unit='mm', timeout=10, **kwargs):
        """Get the inner empty oriented bounding box (OBB) of a container.

        Args:
            targetname (str): Name of the object
            linkname (str, optional): Can target a specific link
            unit (str, optional): Unit of the OBB. Default: mm
            timeout (float, optional):  (Default: 10)

        Returns:
            dict: A dict describing the OBB of the object with keys: extents, boxLocalTranslation, originalBodyTranslation, quaternion, rotationmat, translation
        """
        taskparameters = {'command': 'GetInnerEmptyRegionOBB',
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
            instobjectnames (list[str], optional):
            sensornames (list[str], optional):
            unit (str, optional):  (Default: 'mm')
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'GetInstObjectAndSensorInfo', 'unit':unit}
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
            unit (str, optional):  (Default: 'mm')
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'GetInstObjectInfoFromURI', 'unit':unit}
        if instobjecturi is not None:
            taskparameters['objecturi'] = instobjecturi
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def GetAABB(self, targetname, unit='mm', timeout=10, **kwargs):
        """Gets the axis-aligned bounding box (AABB) of an object.

        Args:
            targetname (str): Name of the object
            unit (str, optional): Unit of the AABB. (Default: mm)
            timeout (float, optional):  (Default: 10)
            linkname (str, optional): Name of link to use for AABB. If not specified, uses entire target

        Returns:
            dict: AABB of the object, e.g. {'pos': [1000,400,100], 'extents': [100,200,50]}
        """
        taskparameters = {'command': 'GetAABB',
                          'targetname': targetname,
                          'unit': unit,
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    
    def SetLocationTracking(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Resets the tracking of specific containers

        Args:
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
            cycleIndex: The cycle index to track the locations for
            locationReplaceInfos: A dict that should have the keys: name, containerDynamicProperties, rejectContainerIds, uri, pose, cycleIndex
            removeLocationNames:
            doRemoveOnlyDynamic:
        """
        taskparameters = {'command': 'SetLocationTracking'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def ResetLocationTracking(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Resets tracking updates for locations

        Args:
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
            resetAllLocations (bool): If True, then will reset all the locations
            resetLocationName (str): Resets only the location with matching name
            resetLocationNames (list[str]): Resets only locations with matching name
            checkIdAndResetLocationName: (locationName, containerId) - only reset the location if the container id matches

        Returns:
            clearedLocationNames
        """
        taskparameters = {'command': 'ResetLocationTracking' }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)['clearedLocationNames']
    
    def GetLocationTrackingInfos(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Gets the active tracked locations

        Args:
            fireandforget (bool, optional):  (Default: False)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            timeout (float, optional):  (Default: 10)
        
        Returns:
            dict: activeLocationTrackingInfos
        """
        taskparameters = {'command': 'GetLocationTrackingInfos' }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)['activeLocationTrackingInfos']
    
    def UpdateLocationContainerIdType(self, locationName, containerName, containerId, containerType, trackingCycleIndex=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Resets the tracking of specific containers

        Args:
            locationName (str):
            containerName (str):
            containerId (str):
            containerType (str):
            trackingCycleIndex (optional): if specified then cycle with same cycleIndex will update location tracking in the same call
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
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
            locationName (str):
            checkContainerId: if checkContainerId is specified and not empty and it matches the current containerId of the tracking location, then reset the current tracking location
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
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
            prefix (str, optional):
            removeNamePrefixes (list[str], optional): Names of prefixes to match with when removing items
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
            removeLocationNames (list[str], optional):
            doRemoveOnlyDynamic (bool): If True, then remove objects that were added through dynamic means like UpdateObjects/UpdateEnvironmentState

        Returns:
            dict: With key 'removedBodyNames' for the removed object names
        """
        taskparameters = {'command': 'RemoveObjectsWithPrefix',
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
            timeout (float, optional):  (Default: 10)
            startindex (int): Start of the trajectory to get. If negative, will start counting from the end. For example, -1 is the last element, -2 is the 
            num (int): Number of trajectories from startindex to return. If 0 will return all the trajectories starting from startindex
            includejointvalues (bool): If True, will include timedjointvalues. If False, will just give back the trajectories. (Default: False)

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
                
                Where timedjointvalues is a list joint values and the trajectory time. For a 3DOF robot sampled at 0.008s, this is
                [J1, J2, J3, 0, J1, J2, J3, 0.008, J1, J2, J3, 0.016, ...]
        """
        taskparameters = {'command': 'GetTrajectoryLog',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ChuckGripper(self, robotname=None, grippername=None, timeout=10, usewebapi=None, **kwargs):
        """Chucks the manipulator

        Args:
            robotname (str, optional): Name of the robot
            grippername (str, optional): Name of the gripper
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
        """
        taskparameters = {'command': 'ChuckGripper', 'grippername':grippername}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def UnchuckGripper(self, robotname=None, grippername=None, timeout=10, usewebapi=None, **kwargs):
        """Unchucks the manipulator and releases the target

        Args:
            robotname (str, optional): Name of the robot
            grippername (str, optional): Name of the gripper
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            targetname (str): Name of the target
        """
        taskparameters = {'command': 'UnchuckGripper', 'grippername':grippername}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)

    def CalibrateGripper(self, robotname=None, grippername=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Goes through the gripper calibration procedure

        Args:
            robotname (str, optional): Name of the robot
            grippername (str, optional): Name of the gripper
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
        """
        taskparameters = {'command': 'CalibrateGripper', 'grippername':grippername}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)

    def StopGripper(self, robotname=None, grippername=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """

        Args:
            robotname (str, optional): Name of the robot
            grippername (str, optional): Name of the gripper
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
        """
        taskparameters = {'command': 'StopGripper', 'grippername':grippername}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def MoveGripper(self, grippervalues, robotname=None, grippername=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Moves the chuck of the manipulator to a given value.

        Args:
            grippervalues (list[float]): Target value of the chuck
            robotname (str, optional): Name of the robot
            grippername (str, optional): Name of the manipulator.
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
        """
        taskparameters = {
            'command': 'MoveGripper',
            'grippername':grippername,
            'grippervalues': grippervalues,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def ExecuteRobotProgram(self, robotProgramName, robotname=None, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Execute a robot specific program by name

        Args:
            robotProgramName (list[str]):
            robotname (str, optional): Name of the robot
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
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
            timeout (float, optional):  (Default: 10)
            filename (str): e.g. /tmp/testscene.mujin.dae, if not specified, it will be saved with an auto-generated filename
            preserveexternalrefs (bool): If True, any bodies that are currently being externally referenced from the environment will be saved as external references.
            externalref (str): If '*', then each of the objects will be saved as externally referencing their original filename. Otherwise will force saving specific bodies as external references.
            saveclone: If 1, will save the scenes for all the cloned environments
            saveReferenceUriAsHint (bool): If True, use save the reference uris as referenceUriHint so that webstack does not get confused and deletes content

        Returns:
            dict: The filename the scene is saved to, in a json dictionary, e.g. {'filename': '2013-11-01-17-10-00-UTC.dae'}
        """
        taskparameters = {'command': 'SaveScene'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def SaveGripper(self, timeout=10, robotname=None, **kwargs):
        """Separate gripper from a robot in a scene and save it.

        Args:
            timeout (float, optional):  (Default: 10)
            robotname (str, optional): Name of robot waiting for extracting hand from.
            filename (str): File name to save on the file system. e.g. /tmp/robotgripper/mujin.dae
            manipname (str): Name of manipulator.
        """

        taskparameters = {'command': 'SaveGripper'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout)

    def MoveJointsToJointConfigurationStates(self, jointConfigurationStates, robotname=None, robotspeed=None, robotaccelmult=None, execute=1, startJointConfigurationStates=None, envclearance=None, timeout=10, usewebapi=True, **kwargs):
        """Moves the robot to desired joint angles specified in jointStates

        Args:
            jointConfigurationStates:
            robotname (str, optional): Name of the robot
            robotspeed (float, optional): Value in (0,1] setting the percentage of robot speed to move at
            robotaccelmult (float, optional): Value in (0,1] setting the percentage of robot acceleration to move at
            execute:  (Default: 1)
            startJointConfigurationStates (optional):
            envclearance (float, optional): Environment clearance in millimeters
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: True)
            jointStates (list): List[{'jointName':str, 'jointValue':float}]
            jointindices (list): List of corresponding joint indices, default is range(len(jointvalues))
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
            jointvalues: List of joint values
            jointindices: List of corresponding joint indices, default is range(len(jointvalues))
            robotname (str, optional): Name of the robot
            robotspeed (float, optional): Value in (0,1] setting the percentage of robot speed to move at
            robotaccelmult (float, optional): Value in (0,1] setting the percentage of robot acceleration to move at
            execute:  (Default: 1)
            startvalues (list[float], optional):
            envclearance (float, optional): Environment clearance in millimeters
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: True)
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
            positionConfigurationCandidateNames (optional): If specified, goes to the first position that is defined for the robot. If no positions exist, returns without moving the robot.
            robotname (str, optional): Name of the robot
            robotspeed (float, optional): Value in (0,1] setting the percentage of robot speed to move at
            robotaccelmult (float, optional): Value in (0,1] setting the percentage of robot acceleration to move at
            execute:  (Default: 1)
            startvalues (list[float], optional):
            envclearance (float, optional): Environment clearance in millimeters
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: True)
        
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
        """Returns the data of the IO in ascii hex as a string

        Args:
            ioname (str, optional): One IO name to read
            ionames (list[str], optional): A list of the IO names to read
            robotname (str, optional): Name of the robot
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
        """
        taskparameters = {
            'command': 'GetRobotBridgeIOVariables'
        }
        if ioname is not None and len(ioname) > 0:
            taskparameters['ioname'] = ioname
        if ionames is not None and len(ionames) > 0:
            taskparameters['ionames'] = ionames

        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)
    
    def SetRobotBridgeIOVariables(self, iovalues, robotname=None, timeout=10, usewebapi=None, **kwargs):
        """

        Args:
            iovalues:
            robotname (str, optional): Name of the robot
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
        """
        taskparameters = {
            'command': 'SetRobotBridgeIOVariables',
            'iovalues': list(iovalues)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, usewebapi=usewebapi)
    
    def ComputeIkParamPosition(self, name, robotname=None, timeout=10, usewebapi=None, **kwargs):
        """

        Args:
            name (str):
            robotname (str, optional): Name of the robot
            timeout (float, optional):  (Default: 10)
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
            freeinc (float, optional): (deprecated) The discretization of the free joints of the robot when computing ik.
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
        taskparameters = {'command': 'ComputeIKFromParameters',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout)

    def ReloadModule(self, timeout=10, **kwargs):
        """

        Args:
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'ReloadModule'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ShutdownRobotBridge(self, timeout=10, **kwargs):
        """

        Args:
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'ShutdownRobotBridge'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def GetRobotBridgeState(self, timeout=10, **kwargs):
        """

        Args:
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'GetRobotBridgeState'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def ClearRobotBridgeError(self, timeout=10, usewebapi=None, **kwargs):
        """

        Args:
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
        """
        taskparameters = {
            'command': 'ClearRobotBridgeError',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)

    def SetRobotBridgePause(self, timeout=10, **kwargs):
        """

        Args:
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'SetRobotBridgePause'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    def SetRobotBridgeResume(self, timeout=10, **kwargs):
        """

        Args:
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {'command': 'SetRobotBridgeResume'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)

    #
    # jogging related
    #

    def SetJogModeVelocities(self, movejointsigns, robotname=None, toolname=None, robotspeed=None, robotaccelmult=None, canJogInCheckMode=None, usewebapi=False, timeout=1, fireandforget=False, **kwargs):
        """

        Args:
            movejointsigns:
            robotname (str, optional): Name of the robot
            toolname (str, optional): Name of the manipulator. Default: self.toolname
            robotspeed (float, optional): Value in (0,1] setting the percentage of robot speed to move at
            robotaccelmult (float, optional): Value in (0,1] setting the percentage of robot acceleration to move at
            canJogInCheckMode: if true, then allow jogging even if in check mode. By default it is false.
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
            timeout (float, optional):  (Default: 1)
            fireandforget (bool, optional):  (Default: False)
            jogtype (str): One of 'joints', 'world', 'robot', 'tool'
            checkSelfCollisionWhileJogging:
            force:
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
            usewebapi (bool, optional):  (Default: False)
            timeout (float, optional):  (Default: 1)
            fireandforget (bool, optional):  (Default: False)
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
            timeout (float, optional):  (Default: 3)
            fireandforget (bool, optional):  (Default: False)
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
            timeout (float, optional):  (Default: 3)
            fireandforget (bool, optional):  (Default: False)
        """
        taskparameters = {
            'command': 'SetRobotBridgeLockMode',
            'islockmode': islockmode
        }
        return self.ExecuteCommand(taskparameters, robotname=robotname, timeout=timeout, fireandforget=fireandforget, usewebapi=usewebapi)

    def ResetSafetyFault(self, timeout=3, fireandforget=False):
        """

        Args:
            timeout (float, optional):  (Default: 3)
            fireandforget (bool, optional):  (Default: False)
        """
        taskparameters = {
            'command': 'ResetSafetyFault',
        }
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def SetRobotBridgeControlMode(self, controlMode, timeout=3, fireandforget=False):
        """

        Args:
            controlMode (str): The control mode to use, e.g. "Manual".
            timeout (float, optional):  (Default: 3)
            fireandforget (bool, optional):  (Default: False)
        """
        taskparameters = {
            'command': 'SetRobotBridgeControlMode',
            'controlMode': controlMode
        }
        return self.ExecuteCommand(taskparameters, timeout=timeout, fireandforget=fireandforget)

    def GetDynamicObjects(self, usewebapi=False, timeout=1, **kwargs):
        """Get a list of dynamically added objects in the scene, from vision detection and physics simulation.

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
            timeout (float, optional):  (Default: 1)
        """
        taskparameters = {
            'command': 'GetDynamicObjects',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def ResetCacheTemplates(self, usewebapi=False, timeout=1, fireandforget=False, **kwargs):
        """Resets any cached templates

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
            timeout (float, optional):  (Default: 1)
            fireandforget (bool, optional):  (Default: False)
        """
        taskparameters = {
            'command': 'ResetCacheTemplates',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def SetRobotBridgeExternalIOPublishing(self, enable, usewebapi=False, timeout=2, fireandforget=False, **kwargs):
        """Enables publishing collision data to the robotbridge

        Args:
            enable:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
            timeout (float, optional):  (Default: 2)
            fireandforget (bool, optional):  (Default: False)
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
        """runs step response test on specified joint and returns result

        Args:
            jointName (str): The name of the joint.
            amplitude (float): The amplitude.
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
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
        """runs maximum length sequence test on specified joint and returns result

        Args:
            jointName (str): The name of the joint.
            amplitude (float): The amplitude.
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
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
            timeout (float, optional):  (Default: 120)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
        """
        taskparameters = {
            'command': 'RunMotorControlTuningDecayingChirp',
            'jointName': jointName,
            'freqMax': freqMax,
            'amplitude': amplitude,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def RunMotorControlTuningGaussianImpulse(self, jointName, amplitude, timeout=20, usewebapi=False, **kwargs):
        """runs Gaussian Impulse test on specified joint and returns result

        Args:
            jointName (str): The name of the joint.
            amplitude (float): The amplitude.
            timeout (float, optional):  (Default: 20)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
        """
        taskparameters = {
            'command': 'RunMotorControlTuningGaussianImpulse',
            'jointName': jointName,
            'amplitude': amplitude,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def RunMotorControlTuningBangBangResponse(self, jointName, amplitude, timeout=60, usewebapi=False, **kwargs):
        """runs bangbang trajectory in acceleration or jerk space and returns result

        Args:
            jointName (str): The name of the joint.
            amplitude (float): The amplitude.
            timeout (float, optional):  (Default: 60)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
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
            timeout:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
        """
        taskparameters = dict()
        taskparameters['command'] = 'RunDynamicsIdentificationTest'
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetTimeToRunDynamicsIdentificationTest(self, usewebapi=False, timeout=10, **kwargs):
        """

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = dict()
        taskparameters['command'] = 'GetTimeToRunDynamicsIdentificationTest'
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetInertiaChildJointStartValues(self, usewebapi=False, timeout=10, **kwargs):
        """

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = dict()
        taskparameters['command'] = 'GetInertiaChildJointStartValues'
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def CalculateTestRangeFromCollision(self, usewebapi=False, timeout=10, **kwargs):
        """

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = dict()
        taskparameters['command'] = 'CalculateTestRangeFromCollision'
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetMotorControlParameterSchema(self, usewebapi=False, timeout=10, **kwargs):
        """Gets motor control parameter schema

        Args:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {
            'command': 'GetMotorControlParameterSchema',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetMotorControlParameter(self, jointName, parameterName, usewebapi=False, timeout=10, **kwargs):
        """Gets motor control parameters as name-value dict

        Args:
            jointName (str): The name of the joint.
            parameterName:
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
            timeout (float, optional):  (Default: 10)
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
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
            timeout (float, optional):  (Default: 10)
        """
        taskparameters = {
            'command': 'GetMotorControlParameters',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def SetMotorControlParameter(self, jointName, parameterName, parameterValue, timeout=10, usewebapi=False, **kwargs):
        """Sets motor control parameter

        Args:
            jointName (str): The name of the joint.
            parameterName:
            parameterValue:
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
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
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
        """
        return self.ExecuteCommand({'command': 'IsProfilingRunning'}, usewebapi=usewebapi, timeout=timeout)

    def StartProfiling(self, clocktype='cpu', timeout=10, usewebapi=False):
        """Start profiling planning

        Args:
            clocktype:  (Default: 'cpu')
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
        """
        return self.ExecuteCommand({'command': 'StartProfiling', 'clocktype': clocktype}, usewebapi=usewebapi, timeout=timeout)

    def StopProfiling(self, timeout=10, usewebapi=False):
        """Stop profiling planning

        Args:
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ. (Default: False)
        """
        return self.ExecuteCommand({'command': 'StopProfiling'}, usewebapi=usewebapi, timeout=timeout)
    
    def ReplaceBodies(self, bodieslist, timeout=10, **kwargs):
        """Replaces bodies in the environment with new uris

        Args:
            bodieslist:
            timeout (float, optional):  (Default: 10)
            replaceInfos (list[dict]): list of dicts with keys: name, uri, containerDynamicProperties
            testLocationName (str): If specified, will test if the container in this location matches testLocationContainerId, and only execute the replace if it matches and testLocationContainerId is not empty.
            testLocationContainerId (str): containerId used for testing logic with testLocationName
            removeNamePrefixes:
            removeLocationNames:
            doRemoveOnlyDynamic:
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
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
        """
        taskparameters = {'command': 'GetState'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def EnsureSyncWithRobotBridge(self, syncTimeStampUS, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """Ensures that planning has synchronized with robotbridge data that is newer than syncTimeStampUS

        Args:
            syncTimeStampUS: us (linux time) of the timestamp
            timeout (float, optional):  (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
        """
        taskparameters = {'command': 'EnsureSyncWithRobotBridge', 'syncTimeStampUS':syncTimeStampUS}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
    
    def ResetCachedRobotConfigurationState(self, timeout=10, usewebapi=None, fireandforget=False, **kwargs):
        """
        Resets cached robot configuration (position of the robot) in the planning slave received from slave notification. Need to perform every time robot moved not from the task slaves.

        Args:
            timeout (float, optional): (Default: 10)
            usewebapi (bool, optional): If True, send command through Web API. Otherwise, through ZMQ.
            fireandforget (bool, optional):  (Default: False)
        """
        taskparameters = {
            'command': 'ResetCachedRobotConfigurationState',
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
