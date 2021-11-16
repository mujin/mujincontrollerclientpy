# -*- coding: utf-8 -*-
# Copyright (C) 2012-2016 MUJIN Inc
"""
Planning client
"""

# System imports
import threading
import weakref
import os
import time

# Mujin imports
from . import APIServerError, GetMonotonicTime
from . import controllerclientbase, zmqclient
from . import zmq

# Logging
import logging
log = logging.getLogger(__name__)

def GetAPIServerErrorFromZMQ(response):
    """If response is an error, return the APIServerError instantiated from the response's error field. Otherwise return None
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
    """Mujin controller client for planning tasks
    """
    _usewebapi = True  # if True use the HTTP webapi, otherwise the zeromq webapi (internal use only)
    _sceneparams = None
    scenepk = None  # The scenepk this controller is configured for
    _ctx = None  # zmq context shared among all clients
    _ctxown = None  # zmq context owned by this class
    _isok = False  # If False, client is about to be destroyed
    _heartbeatthread = None  # Thread for monitoring controller heartbeat
    _isokheartbeat = False  # If False, then stop heartbeat monitor
    _taskstate = None  # Latest task status from heartbeat message
    _commandsocket = None  # zmq client to the command port
    _configsocket = None  # zmq client to the config port

    def __init__(self, taskzmqport, taskheartbeatport, taskheartbeattimeout, tasktype, scenepk, usewebapi=True, ctx=None, slaverequestid=None, **kwargs):
        """Logs into the mujin controller and initializes the task's zmq connection
        :param taskzmqport: Port of the task's zmq server, e.g. 7110
        :param taskheartbeatport: Port of the task's zmq server's heartbeat publisher, e.g. 7111
        :param taskheartbeattimeout: Seconds until reinitializing task's zmq server if no heartbeat is received, e.g. 7
        :param tasktype: Type of the task
        :param scenepk: Primary key (pk) of the bin picking task scene, e.g. irex2013.mujin.dae
        """
        super(PlanningControllerClient, self).__init__(**kwargs)
        self._slaverequestid = slaverequestid
        self._sceneparams = {}
        self._isok = True

        # Task
        self.tasktype = tasktype
        self._usewebapi = usewebapi

        # Connects to task's zmq server
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
        commandsocket = self._commandsocket
        if commandsocket is not None:
            commandsocket.SetDestroy()
        configsocket = self._configsocket
        if configsocket is not None:
            configsocket.SetDestroy()
        super(PlanningControllerClient, self).SetDestroy()

    def GetSlaveRequestId(self):
        return self._slaverequestid

    def GetCommandSocketRaw(self):
        return self._commandsocket

    def DeleteJobs(self, usewebapi=True, timeout=5):
        """Cancels all jobs
        """
        if usewebapi:
            super(PlanningControllerClient, self).DeleteJobs(usewebapi, timeout)
        else:
            # Cancel on the zmq configure
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
        """Return most recent published state. If publishing is disabled, then will return None
        """
        if self._heartbeatthread is None or not self._isokheartbeat:
            log.warn('Heartbeat thread not running taskheartbeatport=%s, so cannot get latest taskstate', self.taskheartbeatport)
        return self._taskstate
    
    def SetScenePrimaryKey(self, scenepk):
        self.scenepk = scenepk
        sceneuri = controllerclientbase.GetURIFromPrimaryKey(scenepk)
        # for now (HACK) need to set the correct scenefilename. newer version of mujin controller need only scenepk, so remove scenefilename eventually
        mujinpath = os.path.join(os.environ.get('MUJIN_MEDIA_ROOT_DIR', '/var/www/media/u'), self.controllerusername)
        scenefilename = controllerclientbase.GetFilenameFromURI(sceneuri, mujinpath)[1]
        self._sceneparams = {'scenetype': 'mujin', 'sceneuri': sceneuri, 'scenefilename': scenefilename, 'scale': [1.0, 1.0, 1.0]}  # TODO: set scenetype according to the scene
    
    #
    # Tasks related
    #

    def RunSceneTaskAsync(self, scenepk, taskpk, slaverequestid=None, fields=None, usewebapi=True, timeout=5):
        """
        :return: {'jobpk': 'xxx', 'msg': 'xxx'}
        Notice: This overwrites the base in controllerclientbase, to accept slaverequestid.
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
        '''Executes task with a particular task type without creating a new task
        :param taskparameters: A dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        :param forcecancel: If True, cancel all previously running jobs before running this one
        '''
        # Execute task
        try:
            return self._webclient.APICall('GET', u'scene/%s/resultget' % (scenepk), data={
                'tasktype': tasktype,
                'taskparameters': taskparameters,
                'slaverequestid': slaverequestid,
                'timeout': timeout,
            }, timeout=timeout)
        except Exception as e:
            import traceback
            log.warn('Failed in executing sync command through webstack, exception was %s, perhaps planning server or planning slave is not responding, or another sync command is going on? scenepk=%r, tasktype=%r, taskparameters=%r, slaverequestid=%r. Coming from:\n%s', e, scenepk, tasktype, taskparameters, slaverequestid, ''.join(traceback.format_stack()))
            raise
    
    def _ExecuteCommandViaWebAPI(self, taskparameters, slaverequestid='', timeout=None):
        """Executes command via web api
        """
        return self.ExecuteTaskSync(self.scenepk, self.tasktype, taskparameters, slaverequestid=slaverequestid, timeout=timeout)

    def _ExecuteCommandViaZMQ(self, taskparameters, slaverequestid='', timeout=None, fireandforget=None, checkpreempt=True, respawnopts=None):
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
        response = self._commandsocket.SendCommand(command, timeout=timeout, fireandforget=fireandforget, checkpreempt=checkpreempt)

        if fireandforget:
            # For fire and forget commands, no response will be available
            return None

        error = GetAPIServerErrorFromZMQ(response)
        if error is not None:
            log.warn('GetAPIServerErrorFromZMQ returned error for %r', response)
            raise error
        if response is None:
            log.warn(u'got no response from task %r', taskparameters)
            return None

        return response['output']

    def ExecuteCommand(self, taskparameters, usewebapi=None, slaverequestid=None, timeout=None, fireandforget=None, respawnopts=None):
        """Executes command with taskparameters
        :param taskparameters: Task parameters in json format
        :param timeout: Timeout in seconds for web api call
        :param fireandforget: Whether we should return immediately after sending the command
        :return: Server response in json format
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

    #
    # Config
    #

    def Configure(self, configuration, usewebapi=None, timeout=None, fireandforget=None):
        configuration['command'] = 'configure'
        return self.SendConfig(configuration, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def SetLogLevel(self, componentLevels, fireandforget=None, timeout=5):
        """Set webstack and planning log level
        :param componentLevels: Mapping from component name to level name, for example {"some.specific.component": "DEBUG"}
                                If component name is empty string, it sets the root logger
                                If level name is empty string, it unsets the level previously set
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
            # For fire and forget commands, no response will be available
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
        Sends a command that moves the camera to one of the following point of view names:
        +x, -x, +y, -y, +z, -z.
        For each point of view, the camera will be aligned to the scene's bounding box center, and the whole scene will be visible. The camera will look at the 
        scene from the opposite direction of the point of view's name's axis (for instance, the camera placed at +x will look at the scene from the -x direction).
        """
        viewercommand = {
            'command': 'MoveCameraPointOfView',
            'axis': pointOfViewName,
        }
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def SetCameraTransform(self, pose=None, transform=None, distanceToFocus=0.0, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        """Sets the camera transform
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
