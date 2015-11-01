# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
# Mujin controller client for bin picking task

import json

# logging
import logging
log = logging.getLogger(__name__)



# mujin imports
from . import ControllerClientError, APIServerError
from . import controllerclientbase, viewermixin
from . import ugettext as _


class ITLPlanning2ControllerClient(controllerclientbase.ControllerClientBase, viewermixin.ViewerMixin):
    """mujin controller client for itlplanning2 task
    """
    tasktype = 'itlplanning2'
    _robotControllerUri = None  # URI of the robot controller, e.g. tcp://192.168.13.201:7000?densowavearmgroup=5
    _robotDeviceIOUri = None  # the device io uri (usually PLC used in the robot bridge)
    
    #TODO : add robotdeviceIOuri
    def __init__(self, controllerurl, controllerusername, controllerpassword, robotControllerUri, scenepk, robotname, itlplanning2zmqport=None, itlplanning2heartbeatport=None, itlplanning2heartbeattimeout=None, usewebapi=False, initializezmq=True, ctx=None, slaverequestid=None):
        
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
        super(ITLPlanning2ControllerClient, self).__init__(controllerurl, controllerusername, controllerpassword, itlplanning2zmqport, itlplanning2heartbeatport, itlplanning2heartbeattimeout, self.tasktype, scenepk, initializezmq, usewebapi, ctx, slaverequestid=slaverequestid)
        
        # robot controller
        self._robotControllerUri = robotControllerUri
        # bin picking task
        self.robotname = robotname


    def SetDOFValues(self, values, timeout=1, usewebapi=False, **kwargs):
        taskparameters = {'command': 'SetDOFValues',
                          'robotvalues'  : values
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetToolValuesFromJointValues(self, jointvalues, valuetype=None, timeout=1, usewebapi=False, **kwargs):
        taskparameters = {
            'command': 'GetToolValuesFromJointValues',
            'jointvalues': jointvalues,
        }
        if valuetype is not None:
            taskparameters['valuetype'] = valuetype
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetJointName(self, index, timeout=1, usewebapi=False, **kwargs):
        taskparameters = {'command': 'GetJointName',
                          'jointindex'  : index
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def GetDOF(self, timeout=1, usewebapi=False, **kwargs):
        taskparameters = {'command': 'GetDOF',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)


    def GetJointValuesFromToolValues(self, toolvalues, initjointvalues=None, timeout=1, usewebapi=False, **kwargs):
        taskparameters = {
            'command': 'GetJointValuesFromToolValues',
            'toolvalues': toolvalues,
        }
        if initjointvalues is not None:
            taskparameters['initjointvalues'] = initjointvalues
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

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
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def ExecuteTrajectory(self, resourcepk, timeout=1000):
        """ executes trajectory if the program exists
        (incomplete function)
        """
        try:
            status, response = self._webclient.APICall('POST', u'planningresult/%s/program' %resourcepk, url_params={'type': 'robotbridgeexecution', 'force':1}, timeout=1000)
        except APIServerError:
            return False

    def ComputeCommandPosition(self, command, jointvalues=None, usewebapi=False, timeout=5, **kwargs):
        """
        computes the position from the command
        """
        taskparameters = {
            'command':'ComputeCommandPosition',
            'movecommand': command,
        }
        if jointvalues is not None:
            taskparameters['jointvalues'] = jointvalues
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    
    def MoveJoints(self, jointvalues, maxJointSpeedRatio, maxJointAccelRatio, jointoffsets, checkcollision, startvalues=None, jointindices=None, execute=1, robotspeed=1, usewebapi=False, timeout=None, **kwargs):
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
                          'maxjointspeedratio':maxJointSpeedRatio,
                          'maxjointaccelratio':maxJointAccelRatio,
                          'jointoffsets':jointoffsets,
                          'execute': execute,
                          'checkcollision':checkcollision
                          }
        if startvalues is not None:
            taskparameters['startvalues'] = list(startvalues)
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, robotspeed=robotspeed, usewebapi=usewebapi, timeout=timeout)
    


    def ConvertCodetoITL(self, timeout=None, **kwargs):
        taskparameters = {'command': 'ConvertCodetoITL',
                          'gcode'  : testGCODE
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout)


    def ExecuteProgram(self, itlprogram, programname, execute=True, timeout=None, usewebapi=True,  **kwargs):
        """
        converts the current program
        """
        taskparameters = { 'command' : 'ExecuteProgram',
                           'program' : itlprogram,
                           'programname' : programname,
                           'execute' : execute
                         }
        
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)



    def ExecuteSequentialPrograms(self, programinfo, timeout=None, **kwargs):
        pass
    
    def GetJointValues(self, timeout=10,  usewebapi=False, **kwargs):
        """gets the current robot joint values
        :return: current joint values in a json dictionary with
        - currentjointvalues: [0,0,0,0,0,0]
        """
        taskparameters = {'command': 'GetJointValues',
                          }
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)
    

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
    
    def Pause(self, timeout=10, usewebapi=False, **kwargs):
        taskparameters = {'command': 'Pause'}
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)
    
    def Resume(self, timeout=10, usewebapi=False, **kwargs):
        taskparameters = {'command': 'Resume'}
        taskparameters.update(kwargs)
        return self.ExecuteRobotCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)
    
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
        assert(False)

    # def _ExecuteCommandViaWebAPI(self, taskparameters, timeout=3000):
    #     """executes command via web api
    #     """
    #     assert(self.tasktype == 'itlplanning2')
    #     if self.tasktype == 'itlplanning2' and len(taskparameters.get('programname','')) > 0:
    #         if taskparameters.get('execute', False):
    #             return self._ExecuteITLPlanning2Task(self.scenepk, self.tasktype, taskparameters, slaverequestid=self._slaverequestid, async=True)
    #         else:
    #             return self._ExecuteITLPlanning2Task(self.scenepk, self.tasktype, taskparameters, slaverequestid=self._slaverequestid, async=False)
    #     return super(ITLPlanning2ControllerClient, self)._ExecuteCommandViaWebAPI(taskparameters, timeout=timeout)

    # def _ExecuteITLPlanning2Task(self, scenepk, tasktype, taskparameters, forcecancel=False, slaverequestid='', timeout=1000, async=True, taskpk=None):
    #     '''executes task with a particular task type without creating a new task
    #     :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
    #     :param forcecancel: if True, then cancel all previously running jobs before running this one
    #     '''
    #     if taskpk is None:
    #         taskpk = self.GetOrCreateSceneTask(scenepk, taskparameters.get('programname',''), 'itlplanning2')
    #     putresponse = self._webclient.APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'itlplanning2', 'taskparameters': taskparameters, 'slaverequestid': slaverequestid}, timeout=5)
    #     if async:
    #         # set the task parameters
    #         # just in case, delete all previous tasks
    #         if forcecancel:
    #             self._webclient.APICall('DELETE', 'job', timeout=5)
    #         # execute the task
    #         status, response = self._webclient.APICall('POST', u'scene/%s/task/%s' % (scenepk, taskpk), timeout=timeout)
    #         assert(status == 200)
    #         # the jobpk allows us to track the job
    #         jobpk = response['jobpk']
    #         return jobpk # for tracking the job
    #     else:
    #         return putresponse[1]['pk']

    # def CheckITLTrajectoryAvailable(self, resourcepk, programtype='mujinxml', timeout=1000):
    #     ''' checks if the resource for trajectory is available for a given
    #     resource pk
    #     '''
    #     try:
    #         status, response = self._webclient.APICall('GET', u'planningresult/%s/program' % resourcepk, url_params={'type': programtype}, timeout=5)
    #         if status == 200:
    #             if len(response > 0):
    #                 return True # does not guarantee the trajectory duration > 0
    #     except APIServerError:
    #         return False # does not exist

    def PlotGraph(self, programname, updatestamp, ikparams=None, maniptrajectories=None, deltatime=None, usewebapi=False, timeout=10, fireandforget=True):
        taskparameters = {
            'command': 'PlotGraph',
            'programname': programname,
            'updatestamp': int(updatestamp),
        }
        if ikparams is not None:
            taskparameters['ikparams'] = ikparams
        if maniptrajectories is not None:
            taskparameters['maniptrajectories'] = maniptrajectories
        if deltatime is not None:
            taskparameters['deltatime'] = float(deltatime)

        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
