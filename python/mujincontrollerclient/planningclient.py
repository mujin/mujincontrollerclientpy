# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 MUJIN Inc
"""
Planning client
"""

# system imports
import threading
import weakref
import os
import time

# mujin imports
from . import APIServerError, GetMonotonicTime
from . import controllerclientbase, zmqclient
from . import zmq

# logging
import logging
log = logging.getLogger(__name__)

def GetAPIServerErrorFromZMQ(response):
    """If response is in error, return the APIServerError instantiated from the response's error field. Otherwise return None
    """
    if response is None:
        return None
    
    if 'error' in response:
        if isinstance(response['error'], dict):
            return APIServerError(response['error']['description'], response['error']['errorcode'], response['error'].get('inputcommand',None), response['error'].get('detailInfoType',None), response['error'].get('detailInfo',None))
        
        else:
            return APIServerError(response['error'])
    
    elif 'exception' in response:
        return APIServerError(response['exception'])
    
    elif 'status' in response and response['status'] != 'succeeded':
        # something happened so raise exception
        return APIServerError(u'Resulting status is %s' % response['status'])

class PlanningControllerClient(controllerclientbase.ControllerClient):
    """mujin controller client for planning tasks
    """
    _usewebapi = True  # if True use the HTTP webapi, otherwise the zeromq webapi (internal use only)
    _sceneparams = None
    scenepk = None  # the scenepk this controller is configured for
    _ctx = None  # zmq context shared among all clients
    _ctxown = None  # zmq context owned by this class
    _isok = False  # if False, client is about to be destroyed
    _heartbeatthread = None  # thread for monitoring controller heartbeat
    _isokheartbeat = False  # if False, then stop heartbeat monitor
    _taskstate = None  # latest task status from heartbeat message
    _commandsocket = None  # zmq client to the command port
    _configsocket = None  # zmq client to the config port

    def __init__(self, taskzmqport, taskheartbeatport, taskheartbeattimeout, tasktype, scenepk, usewebapi=True, ctx=None, slaverequestid=None, **kwargs):
        """logs into the mujin controller and initializes the task's zmq connection
        :param taskzmqport: port of the task's zmq server, e.g. 7110
        :param taskheartbeatport: port of the task's zmq server's heartbeat publisher, e.g. 7111
        :param taskheartbeattimeout: seconds until reinitializing task's zmq server if no hearbeat is received, e.g. 7
        :param tasktype: type of the task
        :param scenepk: pk of the bin picking task scene, e.g. irex2013.mujin.dae
        """
        super(PlanningControllerClient, self).__init__(**kwargs)
        self._slaverequestid = slaverequestid
        self._sceneparams = {}
        self._isok = True

        # task
        self.tasktype = tasktype
        self._usewebapi = usewebapi

        # connects to task's zmq server
        self._commandsocket = None
        self._configsocket = None
        if taskzmqport is not None:
            if ctx is None:
                self._ctx = zmq.Context()
                self._ctxown = self._ctx
            else:
                self._ctx = ctx
            self.taskzmqport = taskzmqport
            self._commandsocket = zmqclient.ZmqClient(self.controllerIp, taskzmqport, ctx)
            self._configsocket = zmqclient.ZmqClient(self.controllerIp, taskzmqport + 2, ctx)

            self.taskheartbeatport = taskheartbeatport
            self.taskheartbeattimeout = taskheartbeattimeout
            if self.taskheartbeatport is not None:
                self._isokheartbeat = True
                self._heartbeatthread = threading.Thread(target=weakref.proxy(self)._RunHeartbeatMonitorThread)
                self._heartbeatthread.start()

        self.SetScenePrimaryKey(scenepk)

    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self.SetDestroy()

        if self._heartbeatthread is not None:
            self._isokheartbeat = False
            self._heartbeatthread.join()
            self._heartbeatthread = None
        if self._commandsocket is not None:
            self._commandsocket.Destroy()
            self._commandsocket = None
        if self._configsocket is not None:
            self._configsocket.Destroy()
            self._configsocket = None
        if self._ctxown is not None:
            try:
                self._ctxown.destroy()
            except Exception:
                pass
            self._ctxown = None

        super(PlanningControllerClient, self).Destroy()

    def SetDestroy(self):
        self._isok = False
        self._isokheartbeat = False
        if self._commandsocket is not None:
            self._commandsocket.SetDestroy()
        if self._configsocket is not None:
            self._configsocket.SetDestroy()
        super(PlanningControllerClient, self).SetDestroy()

    def GetSlaveRequestId(self):
        return self._slaverequestid

    def GetCommandSocketRaw(self):
        return self._commandsocket

    def DeleteJobs(self, usewebapi=True, timeout=5):
        """ cancels all jobs
        """
        if usewebapi:
            super(PlanningControllerClient, self).DeleteJobs(usewebapi, timeout)
        else:
            # cancel on the zmq configure
            if self._configsocket is not None:
                self._SendConfigViaZMQ({'command': 'cancel'}, slaverequestid=self._slaverequestid, timeout=timeout, fireandforget=False)

    def _RunHeartbeatMonitorThread(self, reinitializetimeout=10.0):
        while self._isok and self._isokheartbeat:
            log.info(u'subscribing to %s:%s' % (self.controllerIp, self.taskheartbeatport))
            socket = self._ctx.socket(zmq.SUB)
            socket.setsockopt(zmq.TCP_KEEPALIVE, 1) # turn on tcp keepalive, do these configuration before connect
            socket.setsockopt(zmq.TCP_KEEPALIVE_IDLE, 2) # the interval between the last data packet sent (simple ACKs are not considered data) and the first keepalive probe; after the connection is marked to need keepalive, this counter is not used any further
            socket.setsockopt(zmq.TCP_KEEPALIVE_INTVL, 2) # the interval between subsequential keepalive probes, regardless of what the connection has exchanged in the meantime
            socket.setsockopt(zmq.TCP_KEEPALIVE_CNT, 2) # the number of unacknowledged probes to send before considering the connection dead and notifying the application layer
            socket.connect('tcp://%s:%s' % (self.controllerIp, self.taskheartbeatport))
            socket.setsockopt(zmq.SUBSCRIBE, '')
            poller = zmq.Poller()
            poller.register(socket, zmq.POLLIN)
            
            lastheartbeatts = GetMonotonicTime()
            while self._isokheartbeat and GetMonotonicTime() - lastheartbeatts < reinitializetimeout:
                socks = dict(poller.poll(50))
                if socket in socks and socks.get(socket) == zmq.POLLIN:
                    try:
                        reply = socket.recv_json(zmq.NOBLOCK)
                        if 'slavestates' in reply:
                            self._taskstate = reply.get('slavestates', {}).get('slaverequestid-%s'%self._slaverequestid, None)
                            lastheartbeatts = GetMonotonicTime()
                        else:
                            self._taskstate = None
                    except zmq.ZMQError as e:
                        log.exception('failed to receive from publisher: %s', e)
            if self._isokheartbeat:
                log.warn('%f secs since last heartbeat from controller' % (GetMonotonicTime() - lastheartbeatts))
    
    def GetPublishedTaskState(self):
        """return most recent published state. if publishing is disabled, then will return None
        """
        if self._heartbeatthread is None or not self._isokheartbeat:
            log.warn('heartbeat thread not running taskheartbeatport=%s, so cannot get latest taskstate', self.taskheartbeatport)
        return self._taskstate
    
    def SetScenePrimaryKey(self, scenepk):
        self.scenepk = scenepk
        sceneuri = controllerclientbase.GetURIFromPrimaryKey(scenepk)
        # for now (HACK) need to set the correct scenefilename. newer version of mujin controller need only scenepk, so remove scenefilename eventually
        mujinpath = os.path.join(os.environ.get('MUJIN_MEDIA_ROOT_DIR', '/var/www/media/u'), self.controllerusername)
        scenefilename = controllerclientbase.GetFilenameFromURI(sceneuri, mujinpath)[1]
        self._sceneparams = {'scenetype': 'mujincollada', 'sceneuri': sceneuri, 'scenefilename': scenefilename, 'scale': [1.0, 1.0, 1.0]}  # TODO: set scenetype according to the scene

    #
    # Tasks related
    #

    def RunSceneTaskAsync(self, scenepk, taskpk, slaverequestid=None, fields=None, usewebapi=True, timeout=5):
        """
        :return: {'jobpk': 'xxx', 'msg': 'xxx'}
        Notice: overwrite function in controllerclientbase. This function with additional slaverequestid
        """
        assert(usewebapi)
        if slaverequestid is None:
            slaverequestid = self._slaverequestid
        data = {
            'scenepk': scenepk,
            'target_pk': taskpk,
            'resource_type': 'task',
            'slaverequestid': slaverequestid,
        }
        return self._webclient.APICall('POST', u'job/', data=data, expectedStatusCode=200, timeout=timeout)

    def ExecuteTaskSync(self, scenepk, tasktype, taskparameters, slaverequestid='', timeout=None):
        '''executes task with a particular task type without creating a new task
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        :param forcecancel: if True, then cancel all previously running jobs before running this one
        '''
        # execute task
        return self._webclient.APICall('GET', u'scene/%s/resultget' % (scenepk), data={
            'tasktype': tasktype,
            'taskparameters': taskparameters,
            'slaverequestid': slaverequestid,
            'timeout': timeout,
        }, timeout=timeout)

    def _ExecuteCommandViaWebAPI(self, taskparameters, slaverequestid='', timeout=None):
        """executes command via web api
        """
        return self.ExecuteTaskSync(self.scenepk, self.tasktype, taskparameters, slaverequestid=slaverequestid, timeout=timeout)

    def _ExecuteCommandViaZMQRaw(self, taskparameters, slaverequestid='', timeout=None, fireandforget=None, checkpreempt=True, respawnopts=None):
        command = {
            'fnname': 'RunCommand',
            'taskparams': {
                'tasktype': self.tasktype,
                'sceneparams': self._sceneparams,
                'taskparameters': taskparameters,
            },
            'userinfo': self._userinfo,
            'slaverequestid': slaverequestid,
            'stamp': time.time(),
            'respawnopts': respawnopts,
        }
        if self.tasktype == 'binpicking':
            command['fnname'] = '%s.%s' % (self.tasktype, command['fnname'])
        response = self._commandsocket.SendCommand(command, timeout=timeout, fireandforget=fireandforget, checkpreempt=checkpreempt)

        if fireandforget:
            # for fire and forget commands, no response will be available
            return None

        error = GetAPIServerErrorFromZMQ(response)
        if error is not None:
            log.warn('GetAPIServerErrorFromZMQ returned error for %r', response)
            raise error
        if response is None:
            log.warn(u'got no response from task %r', taskparameters)
            return None

        return response

    def _ExecuteCommandViaZMQ(self, taskparameters, slaverequestid='', timeout=None, fireandforget=None, checkpreempt=True, respawnopts=None):
        response = self._ExecuteCommandViaZMQRaw(taskparameters=taskparameters, slaverequestid=slaverequestid, timeout=timeout, fireandforget=fireandforget, checkpreempt=checkpreempt, respawnopts=respawnopts)
        return response['output'] if response is not None else response

    def ExecuteCommand(self, taskparameters, usewebapi=None, slaverequestid=None, timeout=None, fireandforget=None, respawnopts=None):
        """executes command with taskparameters
        :param taskparameters: task parameters in json format
        :param timeout: timeout in seconds for web api call
        :param fireandforget: whether we should return immediately after sending the command
        :return: return the server response in json format
        """
        if 'stamp' not in taskparameters:
            taskparameters['stamp'] = time.time()
        # log.debug('Executing task with parameters: %r', taskparameters)
        if slaverequestid is None:
            slaverequestid = self._slaverequestid

        if usewebapi is None:
            usewebapi = self._usewebapi

        if usewebapi:
            return self._ExecuteCommandViaWebAPI(taskparameters, timeout=timeout, slaverequestid=slaverequestid)
        else:
            return self._ExecuteCommandViaZMQ(taskparameters, timeout=timeout, slaverequestid=slaverequestid, fireandforget=fireandforget, respawnopts=respawnopts)

    def RespawnPlanningProcess(self, slaverequestid=None, timeout=None, fireandforget=None, respawnopts=None):
        """respawns a planning process
        :return: True if the planning process was respawned, otherwise false.
        """
        if slaverequestid is None:
            slaverequestid = self._slaverequestid

        response = self._ExecuteCommandViaZMQRaw(taskparameters={'command': 'Ping'}, slaverequestid=slaverequestid, timeout=timeout, fireandforget=fireandforget, respawnopts=respawnopts)
        return response.get('wasProcessRespawned', False)

    #
    # Config
    #

    def Configure(self, configuration, usewebapi=None, timeout=None, fireandforget=None):
        configuration['command'] = 'configure'
        return self.SendConfig(configuration, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def SetLogLevel(self, componentLevels, fireandforget=None, timeout=5):
        """ Set webstack and planning log level
        :param componentLevels: mapping from component name to level name, for example {"some.speicifc.component": "DEBUG"}
                                if component name is empty stirng, it sets the root logger
                                if level name is empty string, it unsets the level previously set
        """
        super(PlanningControllerClient, self).SetLogLevel(componentLevels, timeout=timeout)
        configuration = {
            'command': 'setloglevel',
            'componentLevels': componentLevels
        }
        return self.SendConfig(configuration, timeout=timeout, fireandforget=fireandforget)

    def SendConfig(self, command, usewebapi=None, slaverequestid=None, timeout=None, fireandforget=None):
        # log.debug('Send config: %r', command)
        if slaverequestid is None:
            slaverequestid = self._slaverequestid

        return self._SendConfigViaZMQ(command, slaverequestid=slaverequestid, timeout=timeout, fireandforget=fireandforget)

    def _SendConfigViaZMQ(self, command, slaverequestid='', timeout=None, fireandforget=None, checkpreempt=True):
        command['slaverequestid'] = slaverequestid
        response = self._configsocket.SendCommand(command, timeout=timeout, fireandforget=fireandforget, checkpreempt=checkpreempt)
        if fireandforget:
            # for fire and forget commands, no response will be available
            return None

        error = GetAPIServerErrorFromZMQ(response)
        if error is not None:
            raise error
        return response['output']

    #
    # Viewer Parameters Related
    #

    def SetViewerFromParameters(self, viewerparameters, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewerparameters.update(kwargs)
        return self.Configure({'viewerparameters': viewerparameters}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def MoveCameraZoomOut(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, fireandforget=True, ispan=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraZoomOut',
            'zoomdelta': float(zoomdelta),
            'zoommult': float(zoommult),
            'ispan': bool(ispan)
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def MoveCameraZoomIn(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, fireandforget=True, ispan=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraZoomIn',
            'zoomdelta': float(zoomdelta),
            'zoommult': float(zoommult),
            'ispan': bool(ispan)
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def MoveCameraLeft(self, ispan=True, panangle=5.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraLeft',
            'pandelta': float(pandelta),
            'panangle': float(panangle),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def MoveCameraRight(self, ispan=True, panangle=5.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraRight',
            'pandelta': float(pandelta),
            'panangle': float(panangle),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def MoveCameraUp(self, ispan=True, angledelta=3.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraUp',
            'pandelta': float(pandelta),
            'angledelta': float(angledelta),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def MoveCameraDown(self, ispan=True, angledelta=3.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraDown',
            'pandelta': float(pandelta),
            'angledelta': float(angledelta),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def MoveCameraPointOfView(self, pointOfViewName, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        """
        Sends a command that moves the camera to the one of the following point of view names:
        +x, -x, +y, -y, +z, -z.
        For each point of view, the camera will be aligned to the scene's bounding box center, and the whole scene will be visible. Camera will look at the 
        scene using the oposite direction of the point of view name axis (for instance, the camera placed at +x will make it look at the scene in the -x direction).
        """
        viewercommand = {
            'command': 'MoveCameraPointOfView',
            'axis': pointOfViewName,
        }
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def SetCameraTransform(self, pose=None, transform=None, distanceToFocus=0.0, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        """sets the camera transform
        :param transform: 4x4 matrix
        """
        viewercommand = {
            'command': 'SetCameraTransform',
            'distanceToFocus': float(distanceToFocus),
        }
        if transform is not None:
            viewercommand['transform'] = [list(row) for row in transform]
        if pose is not None:
            viewercommand['pose'] = [float(f) for f in pose]
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def StartIPython(self, timeout=1, usewebapi=False, fireandforget=True, **kwargs):
        configuration = {'startipython': True}
        configuration.update(kwargs)
        return self.Configure(configuration, timeout=timeout, usewebapi=usewebapi, fireandforget=fireandforget)
