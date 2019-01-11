# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
# Mujin controller client for bin picking task

# mujin imports
from . import realtimerobotclient

# logging
import logging
log = logging.getLogger(__name__)


class ITLPlanning2ControllerClient(realtimerobotclient.RealtimeRobotControllerClient):
    """mujin controller client for itlplanning2 task
    """

    def __init__(self, **kwargs):

        """logs into the mujin controller, initializes itlplanning2 task, and sets up parameters
        :param controllerurl: url of the mujin controller, e.g. http://controller13
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        :param taskzmqport: port of the itlplanning2 task's zmq server, e.g. 7110
        :param taskheartbeatport: port of the itlplanning2 task's zmq server's heartbeat publisher, e.g. 7111
        :param taskheartbeattimeout: seconds until reinitializing itlplanning2 task's zmq server if no hearbeat is received, e.g. 7
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
        super(ITLPlanning2ControllerClient, self).__init__(tasktype='itlplanning2', **kwargs)

    # def SetDOFValues(self, values, timeout=1, usewebapi=False, **kwargs):
    #     taskparameters = {'command': 'SetDOFValues',
    #                       'robotvalues'  : values
    #                       }
    #     taskparameters.update(kwargs)
    #     return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    # def GetToolValuesFromJointValues(self, jointvalues, valuetype=None, timeout=1, usewebapi=False, **kwargs):
    #     taskparameters = {
    #         'command': 'GetToolValuesFromJointValues',
    #         'jointvalues': jointvalues,
    #     }
    #     if valuetype is not None:
    #         taskparameters['valuetype'] = valuetype
    #     taskparameters.update(kwargs)
    #     return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    # def GetJointName(self, index, timeout=1, usewebapi=False, **kwargs):
    #     taskparameters = {'command': 'GetJointName',
    #                       'jointindex'  : index
    #                       }
    #     taskparameters.update(kwargs)
    #     return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    # def GetDOF(self, timeout=1, usewebapi=False, **kwargs):
    #     taskparameters = {'command': 'GetDOF',
    #                       }
    #     taskparameters.update(kwargs)
    #     return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def ReloadModule(self, timeout=10, **kwargs):
        return self.ExecuteCommand({'command': 'ReloadModule'}, timeout=timeout, **kwargs)

    def GetJointValuesFromToolValues(self, toolvalues, initjointvalues=None, timeout=1, usewebapi=True, **kwargs):
        taskparameters = {
            'command': 'GetJointValuesFromToolValues',
            'toolvalues': toolvalues,
        }
        if initjointvalues is not None:
            taskparameters['initjointvalues'] = initjointvalues
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def ComputeCommandPosition(self, movecommand, jointvalues=None, usewebapi=True, timeout=5, **kwargs):
        """
        computes the position from the command
        """
        taskparameters = {
            'command': 'ComputeCommandPosition',
            'movecommand': movecommand,
        }
        if jointvalues is not None:
            taskparameters['jointvalues'] = jointvalues
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    def JogCommandPosition(self, movecommand, direction=None, rotation=None, movealongsurface=True, fireandforget=False, timeout=5, usewebapi=False, **kwargs):
        taskparameters = {
            'command': 'JogCommandPosition',
            'movecommand': movecommand,
            'movealongsurface': movealongsurface,
        }
        if direction is not None:
            taskparameters['direction'] = direction
        if rotation is not None:
            taskparameters['rotation'] = rotation
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, fireandforget=fireandforget, timeout=timeout, usewebapi=usewebapi)

    def MoveToSurface(self, distancetosurface, robotspeed=None, robotaccelmult=None, toolname=None, timeout=10, usewebapi=True, **kwargs):
        taskparameters = {
            'command': 'MoveToSurface',
            'distancetosurface': distancetosurface,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout, usewebapi=usewebapi)

    def MoveToCommand(self, movecommand, toinitial=False, robotspeed=None, robotaccelmult=None, toolname=None, timeout=10, usewebapi=True, **kwargs):
        taskparameters = {
            'command': 'MoveToCommand',
            'movecommand': movecommand,
            'toinitial': toinitial,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, toolname=toolname, timeout=timeout, usewebapi=usewebapi)

    def SetJointValues(self, jointvalues, timeout=10, usewebapi=True, **kwargs):
        taskparameters = {
            'command': 'SetJointValues',
            'jointvalues': jointvalues,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)

    # def ConvertCodetoITL(self, timeout=None, **kwargs):
    #     taskparameters = {'command': 'ConvertCodetoITL',
    #                       'gcode'  : testGCODE
    #                       }
    #     taskparameters.update(kwargs)
    #     return self.ExecuteCommand(taskparameters, timeout=timeout)
    #
    # def ExecuteProgram(self, itlprogram, programname, execute=True, timeout=None, usewebapi=True,  **kwargs):
    #     """
    #     converts the current program
    #     """
    #     taskparameters = { 'command' : 'ExecuteProgram',
    #                        'program' : itlprogram,
    #                        'programname' : programname,
    #                        'execute' : execute
    #                      }
    #
    #     taskparameters.update(kwargs)
    #     return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)
    #
    # def ExecuteSequentialPrograms(self, programinfo, timeout=None, **kwargs):
    #     pass

    def GetITLState(self, timeout=10, usewebapi=True, **kwargs):
        taskparameters = {'command': 'GetITLState'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)

    # def GetJointValues(self, timeout=10,  usewebapi=False, **kwargs):
    #     """gets the current robot joint values
    #     :return: current joint values in a json dictionary with
    #     - currentjointvalues: [0,0,0,0,0,0]
    #     """
    #     taskparameters = {'command': 'GetJointValues',
    #                       }
    #     taskparameters.update(kwargs)
    #     return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

    # def UpdateObjects(self, envstate, targetname=None, state=None, unit="m", timeout=10, **kwargs):
    #     """updates objects in the scene with the envstate
    #     :param envstate: a list of dictionaries for each instance object in world frame. quaternion is specified in w,x,y,z order. e.g. [{'name': 'target_0', 'translation_': [1,2,3], 'quat_': [1,0,0,0]}, {'name': 'target_1', 'translation_': [2,2,3], 'quat_': [1,0,0,0]}]
    #     :param unit: unit of envstate
    #     """
    #     if targetname is None:
    #         targetname = self.targetname
    #     taskparameters = {'command': 'UpdateObjects',
    #                       'objectname': targetname,
    #                       'object_uri': u'mujin:/%s.mujin.dae' % (targetname),
    #                       'robot': self._robotname,
    #                       'envstate': envstate,
    #                       'unit': unit,
    #                       }
    #     taskparameters.update(kwargs)
    #     if state is not None:
    #         taskparameters['state'] = json.dumps(state)
    #     return self.ExecuteCommand(taskparameters, timeout=timeout)

    # def GetTransform(self, targetname, unit='mm', timeout=10, **kwargs):
    #     """gets the transform of an object
    #     :param targetname: name of the object
    #     :param unit: unit of the result translation
    #     :return: transform of the object in a json dictionary, e.g. {'translation': [100,200,300], 'rotationmat': [[1,0,0],[0,1,0],[0,0,1]], 'quaternion': [1,0,0,0]}
    #     """
    #     taskparameters = {'command': 'GetTransform',
    #                       'targetname': targetname,
    #                       'unit': unit,
    #                       }
    #     taskparameters.update(kwargs)
    #     return self.ExecuteCommand(taskparameters, timeout=timeout)

    # def SetTransform(self, targetname, translation, unit='mm', rotationmat=None, quaternion=None, timeout=10, **kwargs):
    #     """sets the transform of an object
    #     :param targetname: name of the object
    #     :param translation: list of x,y,z value of the object in milimeter
    #     :param unit: unit of translation
    #     :param rotationmat: list specifying the rotation matrix in row major format, e.g. [1,0,0,0,1,0,0,0,1]
    #     :param quaternion: list specifying the quaternion in w,x,y,z format, e.g. [1,0,0,0]
    #     """
    #     taskparameters = {'command': 'SetTransform',
    #                       'targetname': targetname,
    #                       'unit': unit,
    #                       'translation': translation,
    #                       }
    #     taskparameters.update(kwargs)
    #     if rotationmat is not None:
    #         taskparameters['rotationmat'] = rotationmat
    #     if quaternion is not None:
    #         taskparameters['quaternion'] = quaternion
    #     if rotationmat is None and quaternion is None:
    #         taskparameters['quaternion'] = [1, 0, 0, 0]
    #         log.warn('no rotation is specified, using identity quaternion ', taskparameters['quaternion'])
    #     return self.ExecuteCommand(taskparameters, timeout=timeout)

    # def Pause(self, timeout=10, usewebapi=False, **kwargs):
    #     taskparameters = {'command': 'Pause'}
    #     taskparameters.update(kwargs)
    #     return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)

    # def Resume(self, timeout=10, usewebapi=False, **kwargs):
    #     taskparameters = {'command': 'Resume'}
    #     taskparameters.update(kwargs)
    #     return self.ExecuteCommand(taskparameters, timeout=timeout, usewebapi=usewebapi)

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
    #         return jobpk  # for tracking the job
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
    #                 return True  # does not guarantee the trajectory duration > 0
    #     except APIServerError:
    #         return False  # does not exist

    def PlotGraph(self, programname, updatestamp, ikparams=None, highlight=-1, maniptrajectories=None, deltatime=None, usewebapi=False, timeout=10, fireandforget=True):
        taskparameters = {
            'command': 'PlotGraph',
            'programname': programname,
            'updatestamp': int(updatestamp),
        }
        if ikparams is not None:
            taskparameters['ikparams'] = ikparams
            taskparameters['highlight'] = highlight
        if maniptrajectories is not None:
            taskparameters['maniptrajectories'] = maniptrajectories
        if deltatime is not None:
            taskparameters['deltatime'] = float(deltatime)

        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def ExecuteTrajectory(self, trajectories, robotspeed=None, robotaccelmult=None, usewebapi=True, timeout=10, cycles=1, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'ExecuteTrajectory',
            'trajectories': trajectories,
            'cycles': cycles,
        }
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
