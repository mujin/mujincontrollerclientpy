# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
# Mujin controller client for bin picking task

import json

# logging
import logging
log = logging.getLogger(__name__)

# mujin imports
from . import controllerclientbase
from . import ugettext as _


class ITLPlanning2ControllerClient(controllerclientbase.ControllerClientBase):
    """mujin controller client for itlplanning2 task
    """
    tasktype = 'itlplanning2'
    _robotControllerUri = None  # URI of the robot controller, e.g. tcp://192.168.13.201:7000?densowavearmgroup=5
    _robotDeviceIOUri = None  # the device io uri (usually PLC used in the robot bridge)
    

    def __init__(self, controllerurl, controllerusername, controllerpassword, robotControllerUri, scenepk, robotname, itlplanning2zmqport=None, itlplanning2heartbeatport=None, itlplanning2heartbeattimeout=None, usewebapi=False, initializezmq=True, ctx=None):
        """logs into the mujin controller, initializes itlplanning2 task, and sets up parameters
        :param controllerurl: url of the mujin controller, e.g. http://controller13
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        :param itlplanning2zmqport: port of the itlplanning2 task's zmq server, e.g. 7110
        :param itlplanning2heartbeatport: port of the itlplanning2 task's zmq server's heartbeat publisher, e.g. 7111
        :param itlplanning2heartbeattimeout: seconds until reinitializing itlplanning2 task's zmq server if no hearbeat is received, e.g. 7
        :param scenepk: pk of the bin picking task scene, e.g. komatsu_ntc.mujin.dae
        :param robotname: name of the robot, e.g. VP-5243I
        :param robotspeed: speed of the robot, e.g. 0.4
        :param regionname: name of the bin, e.g. container1
        :param targetname: name of the target, e.g. plasticnut-center
        :param toolname: name of the manipulator, e.g. 2BaseZ
        :param envclearance: environment clearance in milimeter, e.g. 20
        :param usewebapi: whether to use webapi for controller commands
        :param robotaccelmult: optional multiplier for forcing the acceleration
        """
        super(ITLPlanning2ControllerClient, self).__init__(controllerurl, controllerusername, controllerpassword, itlplanning2zmqport, itlplanning2heartbeatport, itlplanning2heartbeattimeout, self.tasktype, scenepk, initializezmq, usewebapi, ctx)
        
        # robot controller
        self._robotControllerUri = robotControllerUri
        # bin picking task
        self.robotname = robotname

                
    def SetRobotControllerUri(self, robotControllerUri):
        self._robotControllerUri = robotControllerUri
        
    def SetRobotDeviceIOUri(self, robotDeviceIOUri):
        self._robotDeviceIOUri = robotDeviceIOUri
    
    def GetRobotControllerUri(self):
        return self._robotControllerUri
        
    def GetRobotDeviceIOUri(self):
        return self._robotDeviceIOUri
    
    def ReloadModule(self, timeout=10, **kwargs):
        return self.ExecuteCommand({'command': 'ReloadModule'}, timeout=timeout, **kwargs)

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
        taskparameters['robot'] = robotname
        taskparameters['robotControllerUri'] = self._robotControllerUri
        taskparameters['robotDeviceIOUri'] = self._robotDeviceIOUri

        return self.ExecuteCommand(taskparameters, usewebapi, timeout=timeout)
    
    def ExecuteTrajectory(self, trajectoryxml, robotspeed=None, timeout=10, **kwargs):
        """Executes a trajectory on the robot from a serialized Mujin Trajectory XML file.
        """
        taskparameters = {'command': 'ExecuteTrajectory',
                          'trajectory': trajectoryxml,
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
            log.warn(u'no jointindices specified, moving joints with default jointindices: %s', jointindices)
        taskparameters = {'command': 'MoveJoints',
                          'goaljoints': list(jointvalues),
                          'jointindices': list(jointindices),
                          'envclearance': self.envclearance,
                          'execute': execute,
                          }
        if startvalues is not None:
            taskparameters['startvalues'] = list(startvalues)
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, timeout=timeout)
    


    def ConvertCodetoITL(self, timeout=None, **kwargs):
        testGCODE = '''
        OTEST-CA_G01_G01-3
        F200
        G01X-717.0Y-507.826Z-177.644C169.848A28.421
        G08.4P1A3.U105.V105.
        G09G08.1X-711.917Y-511.079Z-176.461C169.848A28.421W1
        W0
        G01X-717.0Y-507.826Z-177.644C169.848A28.421
        '''
        taskparameters = {'command': 'ConvertCodetoITL',
                          'gcode'  : testGCODE
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)


    def ExecuteProgram(self, itlprogram, programpath, timeout=None, **kwargs):
        """
        converts the current program
        """
        taskparameters = { 'command' : 'ExecuteProgram',
                           'program' : itlprogram,
                           'programpath' : programpath
                         }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)


    def ExecuteSequentialPrograms(self, programinfo, timeout=None, **kwargs):
        pass
    
    def GetJointValues(self, timeout=10, **kwargs):
        """gets the current robot joint values
        :return: current joint values in a json dictionary with
        - currentjointvalues: [0,0,0,0,0,0]
        """
        taskparameters = {'command': 'GetJointValues',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)
    

    def UpdateObjects(self, envstate, targetname=None, state=None, unit="m", timeout=10, **kwargs):
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
                          'unit': unit,
                          }
        taskparameters.update(kwargs)
        if state is not None:
            taskparameters['state'] = json.dumps(state)
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
    

    
    def RemoveObjectsWithPrefix(self, prefix=None, prefixes=None, timeout=10, **kwargs):
        """removes objects with prefix
        """
        taskparameters = {'command': 'RemoveObjectsWithPrefix',
                          }
        taskparameters.update(kwargs)
        if prefix is not None:
            taskparameters['prefix'] = unicode(prefix)
        if prefixes is not None:
            taskparameters['prefixes'] = [unicode(prefix) for prefix in prefixes]
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
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout)
    

    def Pause(self, timeout=10, **kwargs):
        taskparameters = {'command': 'Pause',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)
    
    def Resume(self, timeout=10, **kwargs):
        taskparameters = {'command': 'Resume',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)
    
    def GetRobotBridgeState(self, timeout=10, **kwargs):
        taskparameters = {'command': 'GetRobotBridgeState',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)
    
    def GetITLPlanning2State(self, timeout=10, **kwargs):
        taskparameters = {'command': 'GetITLPlanning2State',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)
    
    def GetPublishedTaskState(self):
        """return most recent published state. if publishing is disabled, then will return None
        """
        return self._taskstate
    
    def SetRobotBridgeIOVariables(self, iovalues, timeout=10, **kwargs):
        taskparameters = {'command': 'SetRobotBridgeIOVariables',
                          'iovalues': list(iovalues)
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)
    
    def SetStopPickPlaceAfterExecutionCycle(self, timeout=10, **kwargs):
        taskparameters = {'command': 'SetStopPickPlaceAfterExecutionCycle',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)

    def SetViewerFromParameters(self, viewerparameters, usewebapi=False, timeout=10, **kwargs):
        taskparameters = {'command': 'SetViewerFromParameters',
                          'viewerparameters':viewerparameters
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
        
    def MoveCameraZoomOut(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, **kwargs):
        taskparameters = {'command': 'MoveCameraZoomOut',
                          'zoomdelta':float(zoomdelta),
                          'zoommult': float(zoommult)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def MoveCameraZoomIn(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, **kwargs):
        taskparameters = {'command': 'MoveCameraZoomIn',
                          'zoomdelta':float(zoomdelta),
                          'zoommult':float(zoommult)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def MoveCameraLeft(self, ispan=True, panangle=5.0, pandelta=40, usewebapi=False, timeout=10, **kwargs):
        taskparameters = {'command': 'MoveCameraLeft',
                          'pandelta':float(pandelta),
                          'panangle':float(panangle),
                          'ispan':bool(ispan)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def MoveCameraRight(self, ispan=True, panangle=5.0, pandelta=40, usewebapi=False, timeout=10, **kwargs):
        taskparameters = {'command': 'MoveCameraRight',
                          'pandelta':float(pandelta),
                          'panangle':float(panangle),
                          'ispan':bool(ispan)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def MoveCameraUp(self, ispan=True, angledelta=3.0, usewebapi=False, timeout=10, **kwargs):
        taskparameters = {'command': 'MoveCameraUp',
                          'angledelta':float(angledelta),
                          'ispan':bool(ispan)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def MoveCameraDown(self, ispan=True, angledelta=3.0, usewebapi=False, timeout=10, **kwargs):
        taskparameters = {'command': 'MoveCameraDown',
                          'angledelta':float(angledelta),
                          'ispan':bool(ispan)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def SetCameraTransform(self, pose=None, transform=None, distanceToFocus=0.0, usewebapi=False, timeout=10, **kwargs):
        """sets the camera transform
        :param transform: 4x4 matrix
        """        
        taskparameters = {'command': 'SetCameraTransform',
                          'distanceToFocus':float(distanceToFocus),
                          }
        if transform is not None:
            taskparameters['transform'] = [list(row) for row in transform]
        if pose is not None:
            taskparameters['pose'] = [float(f) for f in pose]
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def GetCameraTransform(self, usewebapi=False, timeout=10, **kwargs):
        """gets the camera transform, and other
        """
        taskparameters = {'command': 'GetCameraTransform'
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

