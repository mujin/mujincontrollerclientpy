# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc
"""
Mujin controller client
"""

# system imports
import time
import datetime
import weakref

from urlparse import urlparse, urlunparse
import os
import base64
from numpy import fromstring, uint32, unique

try:
    import ujson as json
except ImportError:
    import json

# logging
import logging
log = logging.getLogger(__name__)

# mujin imports
from . import ControllerClientError
from . import controllerclientraw
from . import ugettext as _

class ControllerClient(object):
    """mujin controller client base
    """
    _webclient = None
    _userinfo = None # a dict storing user info, like locale

    controllerurl = '' # url to controller
    controllerusername = '' # username to login with
    controllerpassword = '' # password to login with

    controllerIp = '' # hostname of the controller web server
    controllerPort = 80 # port of the controller web server

    def __init__(self, controllerurl='http://127.0.0.1', controllerusername='', controllerpassword=''):
        """logs into the mujin controller
        :param controllerurl: url of the mujin controller, e.g. http://controller14
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        """

        # parse controllerurl
        scheme, netloc, path, params, query, fragment = urlparse(controllerurl)

        # parse any credential in the url
        if '@' in netloc:
            creds, netloc = netloc.rsplit('@', 1)
            self.controllerusername, self.controllerpassword = creds.split(':', 1)

        # parse ip (hostname really) and port
        self.controllerIp = netloc.split(':', 1)[0]
        self.controllerPort = 80
        if ':' in netloc:
            hostname, port = netloc.split(':')
            self.controllerIp = hostname
            self.controllerPort = int(port)

        self.controllerurl = urlunparse((scheme, netloc, '', '', '', ''))
        self.controllerusername = controllerusername or self.controllerusername
        self.controllerpassword = controllerpassword or self.controllerpassword

        self._userinfo = {
            'username': self.controllerusername,
            'locale': os.environ.get('LANG', ''),
        }
        self._webclient = controllerclientraw.ControllerWebClient(self.controllerurl, self.controllerusername, self.controllerpassword)
        
    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self.SetDestroy()

        if self._webclient is not None:
            self._webclient.Destroy()
            self._webclient = None
    
    def SetDestroy(self):
        if self._webclient is not None:
            self._webclient.SetDestroy()
    
    def SetLocale(self, locale):
        self._userinfo['locale'] = locale
        self._webclient.SetLocale(locale)

    def RestartController(self):
        """ restarts controller
        """
        self._webclient.Request('POST', '/restartserver/', timeout=1)
        # no reason to check response since it's probably an error (server is restarting after all)

    def IsLoggedIn(self):
        return self._webclient.IsLoggedIn()

    def Login(self, timeout=5):
        """Force webclient to login if it is not currently logged in. Useful for checking that the credential works.
        """
        self._webclient.Login(timeout=timeout)

    def Ping(self, usewebapi=True, timeout=5):
        """Sends a dummy HEAD request to api endpoint
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('HEAD', '', timeout=timeout)
        assert(status == 200)

    #
    # Scene related
    #

    def UploadSceneFile(self, f, timeout=5):
        """uploads a file managed by file handle f
        
        """
        # note that /fileupload does not have trailing slash for some reason
        response = self._webclient.Request('POST', '/fileupload', files={'files[]': f}, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(response.content)
        
        try:
            content = json.loads(response.content)
        except ValueError:
            raise ControllerClientError(response.content)
        
        return content['filename']

    def GetScenes(self, fields=None, usewebapi=True, timeout=5):
        """list all available scene on controller
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/', fields=fields, timeout=timeout, url_params={
            'limit': 0,
        })
        assert(status == 200)
        return response['objects']

    def GetScene(self, pk, fields=None, usewebapi=True, timeout=5):
        """returns requested scene
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/' % pk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def GetObject(self, pk, fields=None, usewebapi=True, timeout=5):
        """returns requested object
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'object/%s/' % pk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def GetRobot(self, pk, fields=None, usewebapi=True, timeout=5):
        """returns requested robot
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'robot/%s/' % pk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    #
    # Scene related
    #

    def CreateScene(self, scenedata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'scene/', data=scenedata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetScene(self, scenepk, scenedata, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'scene/%s/' % scenepk, data=scenedata, timeout=timeout)
        assert(status == 202)

    def DeleteScene(self, scenepk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'scene/%s/' % scenepk, timeout=timeout)
        assert(status == 204)

    #
    # InstObject related
    #

    def CreateSceneInstObject(self, scenepk, instobjectdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'scene/%s/instobject/' % scenepk, data=instobjectdata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def GetSceneInstObjects(self, scenepk, fields=None, usewebapi=True, timeout=5):
        """ returns the instance objects of the scene
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response['instobjects']

    def SetSceneInstObject(self, scenepk, instobjectpk, instobjectdata, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'scene/%s/instobject/%s/' % (scenepk, instobjectpk), data=instobjectdata, timeout=timeout)
        assert(status == 202)

    def DeleteSceneInstObject(self, scenepk, instobjectpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'scene/%s/instobject/%s/' % (scenepk, instobjectpk), timeout=timeout)
        assert(status == 204)

    #
    # IKParam related
    #

    def CreateObjectIKParam(self, objectpk, ikparamdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'object/%s/ikparam/' % objectpk, data=ikparamdata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetObjectIKParam(self, objectpk, ikparampk, ikparamdata, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'object/%s/ikparam/%s/' % (objectpk, ikparampk), data=ikparamdata, timeout=timeout)
        assert(status == 202)
        
    def DeleteObjectIKParam(self, objectpk, ikparampk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'object/%s/ikparam/%s/' % (objectpk, ikparampk), timeout=timeout)
        assert(status == 204)
        
    #
    # GraspSet related
    #

    def CreateObjectGraspSet(self, objectpk, graspsetdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'object/%s/graspset/' % objectpk, data=graspsetdata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetObjectGraspSet(self, objectpk, graspsetpk, graspsetdata, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'object/%s/graspset/%s/' % (objectpk, graspsetpk), data=graspsetdata, timeout=timeout)
        assert(status == 202)

    def DeleteObjectGraspSet(self, objectpk, graspsetpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'object/%s/graspset/%s/' % (objectpk, graspsetpk), timeout=timeout)
        assert(status == 204)

    #
    # Tools related
    #

    def CreateRobotTool(self, robotpk, tooldata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'robot/%s/tool/' % robotpk, data=tooldata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetRobotTool(self, robotpk, toolpk, tooldata, usewebapi=True, timeout=5):
        """sets the tool values via a WebAPI PUT call
        :param tooldata: key-value pairs of the data to modify on the tool
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'robot/%s/tool/%s/' % (robotpk, toolpk), data=tooldata, timeout=timeout)
        assert(status == 202)

    def DeleteRobotTool(self, robotpk, toolpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'robot/%s/tool/%s/' % (robotpk, toolpk), timeout=timeout)
        assert(status == 204)

    #
    # Attached sensors related
    #

    def CreateRobotAttachedSensor(self, robotpk, attachedsensordata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'robot/%s/attachedsensor/' % robotpk, data=attachedsensordata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetRobotAttachedSensor(self, robotpk, attachedsensorpk, attachedsensordata, usewebapi=True, timeout=5):
        """sets the attachedsensor values via a WebAPI PUT call
        :param attachedsensordata: key-value pairs of the data to modify on the attachedsensor
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'robot/%s/attachedsensor/%s/' % (robotpk, attachedsensorpk), data=attachedsensordata, timeout=timeout)
        assert(status == 202)

    def DeleteRobotAttachedSensor(self, robotpk, attachedsensorpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'robot/%s/attachedsensor/%s/' % (robotpk, attachedsensorpk), timeout=timeout)
        assert(status == 204)

    #
    # Task related
    #

    def GetSceneTasks(self, scenepk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/task/' % scenepk, fields=fields, timeout=timeout, url_params={
            'limit': 0,
        })
        assert(status == 200)
        return response['objects']

    def GetSceneTask(self, scenepk, taskpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/task/%s/' % (scenepk, taskpk), fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def CreateSceneTask(self, scenepk, taskdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('POST', u'scene/%s/task/' % scenepk, data=taskdata, fields=fields, timeout=timeout)
        assert(status == 201)
        return response

    def SetSceneTask(self, scenepk, taskpk, taskdata, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'scene/%s/task/%s/' % (scenepk, taskpk), data=taskdata, timeout=timeout)
        assert(status == 202)

    def DeleteSceneTask(self, scenepk, taskpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'scene/%s/task/%s/' % (scenepk, taskpk), timeout=timeout)
        assert(status == 204)



    #
    # Result related
    #

    def GetResult(self, resultpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'planningresult/%s/' % resultpk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def GetResultProgram(self, resultpk, programtype=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        params = {'format': 'dat'}
        if programtype is not None and len(programtype) > 0:
            params['type'] = programtype
        # custom http call because APICall currently only supports json
        response = self._webclient.Request('GET', u'/api/v1/planningresult/%s/program/' % resultpk, params=params, timeout=timeout)
        assert(response.status_code == 200)
        return response.content

    def SetResult(self, resultpk, resultdata, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('PUT', u'planningresult/%s/' % resultpk, data=resultdata, timeout=timeout)
        assert(status == 202)

    def DeleteResult(self, resultpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'planningresult/%s/' % resultpk, timeout=timeout)
        assert(status == 204)

    #
    # Job related
    #

    def GetJobs(self, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'job/', fields=fields, timeout=timeout, url_params={
            'limit': 0,
        })
        assert(status == 200)
        return response['objects']

    def DeleteJob(self, jobpk, usewebapi=True, timeout=5):
        """ cancels the job with the corresponding jobk
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'job/%s/' % jobpk, timeout=timeout)
        assert(status == 204)

    def DeleteJobs(self, usewebapi=True, timeout=5):
        """ cancels all jobs
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('DELETE', u'job/', timeout=timeout)
        assert(status == 204)

    #
    # Geometry related
    #
    
    def GetObjectGeometry(self, objectpk, usewebapi=True, timeout=5):
        """ return a list of geometries (a dictionary with key: positions, indices)) of given object
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'object/%s/geometry/' % objectpk, timeout=timeout)
        assert(status == 200)
        geometries = []
        for encodedGeometry in response['geometries']:
            geometry = {}
            positions = fromstring(base64.b64decode(encodedGeometry['positions_base64']), dtype=float)
            positions.resize(len(positions) / 3, 3)
            geometry['positions'] = positions
            indices = fromstring(base64.b64decode(encodedGeometry['positions_base64']), dtype=uint32)
            indices.resize(len(indices) / 3, 3)
            geometry['indices'] = indices
            geometries.append(geometry)
        return geometries

    #
    # Instobject related
    #

    def GetSceneInstanceObjectsViaWebapi(self, scenepk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, fields=fields, timeout=timeout)
        assert(status == 200)
        return response['instobjects']

    #
    # Sensor mappings related
    #

    def GetSceneSensorMapping(self, scenepk=None, usewebapi=True, timeout=5):
        """ return the camerafullname to cameraid mapping. e.g. {'sourcecamera/ensenso_l_rectified': '150353', 'sourcecamera/ensenso_r_rectified':'150353_Right' ...}
        """
        assert(usewebapi)
        if scenepk is None:
            scenepk = self.scenepk
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, timeout=timeout)
        assert(status == 200)
        instobjects = response['instobjects']
        sensormapping = {}
        for instobject in instobjects:
            if len(instobject['attachedsensors']) > 0:
                status, response = self._webclient.APICall('GET', u'robot/%s/attachedsensor/' % instobject['object_pk'])
                assert (status == 200)
                for attachedsensor in response['attachedsensors']:
                    camerafullname = instobject['name'] + '/' + attachedsensor['name']
                    if 'hardware_id' in attachedsensor['sensordata']:
                        sensormapping[camerafullname] = attachedsensor['sensordata']['hardware_id']
                    else:
                        sensormapping[camerafullname] = None
                        log.warn(u'attached sensor %s/%s does not have hardware_id', instobject['name'], attachedsensor.get('name',None))
        return sensormapping

    def SetSceneSensorMapping(self, sensormapping, scenepk=None, usewebapi=True, timeout=5):
        """
        :param sensormapping: the camerafullname to cameraid mapping. e.g. {'sourcecamera/ensenso_l_rectified': '150353', 'sourcecamera/ensenso_r_rectified':'150353_Right' ...}
        """
        assert(usewebapi)
        if scenepk is None:
            scenepk = self.scenepk
        status, response = self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, timeout=timeout)
        assert(status == 200)
        instobjects = response['instobjects']
        cameracontainernames = unique([camerafullname.split('/')[0] for camerafullname in sensormapping.keys()])
        for instobject in instobjects:
            if len(instobject['attachedsensors']) > 0 and instobject['name'] in cameracontainernames:
                cameracontainerpk = instobject['object_pk']
                status, response = self._webclient.APICall('GET', u'robot/%s/attachedsensor/' % cameracontainerpk)
                assert (status == 200)
                for attachedsensor in response['attachedsensors']:
                    camerafullname = instobject['name'] + '/' + attachedsensor['name']
                    cameraid = attachedsensor['sensordata'].get('hardware_id', None)
                    sensorpk = attachedsensor['pk']
                    if camerafullname in sensormapping.keys():
                        if cameraid != sensormapping[camerafullname]:
                            status, response = self._webclient.APICall('PUT', u'robot/%s/attachedsensor/%s' % (cameracontainerpk, sensorpk), data={'sensordata': {'hardware_id': str(sensormapping[camerafullname])}})

    #
    # WebDAV related
    #
    
    def FileExists(self, path, timeout=5):
        """check if a file exists on server
        """
        response = self._webclient.Request('HEAD', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')), timeout=timeout)
        if response.status_code not in [200, 301, 404]:
            raise ControllerClientError(response.content)
        return response.status_code != 404

    def ConstructFileFullURL(self, filename):
        """construct full url to file including credentials
        """
        scheme, netloc, path, params, query, fragment = urlparse(self.controllerurl)
        return urlunparse((
            scheme,
            '%s:%s@%s' % (self.controllerusername, self.controllerpassword, netloc),
            '/u/%s/%s' % (self.controllerusername, filename),
            '',
            '',
            '',
        ))

    def DownloadFile(self, filename, timeout=5):
        """downloads a file given filename

        :return: a streaming response
        """
        response = self._webclient.Request('GET', u'/u/%s/%s' % (self.controllerusername, filename), stream=True, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(response.content)
        
        return response

    def UploadFile(self, path, f, timeout=5):
        response = self._webclient.Request('PUT', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')), data=f, timeout=timeout)
        if response.status_code not in [201, 201, 204]:
            raise ControllerClientError(response.content)

    def ListFiles(self, path='', timeout=5):
        path = u'/u/%s/%s' % (self.controllerusername, path.rstrip('/'))
        response = self._webclient.Request('PROPFIND', path, timeout=timeout)
        if response.status_code not in [207]:
            raise ControllerClientError(response.content)

        import xml.etree.cElementTree as xml
        import email.utils

        tree = xml.fromstring(response.content)

        def prop(e, name, default=None):
            child = e.find('.//{DAV:}' + name)
            return default if child is None else child.text

        files = {}
        for e in tree.findall('{DAV:}response'):
            name = prop(e, 'href')
            assert(name.startswith(path))
            name = name[len(path):].strip('/')
            size = int(prop(e, 'getcontentlength', 0))
            isdir = prop(e, 'getcontenttype', '') == 'httpd/unix-directory'
            modified = email.utils.parsedate(prop(e, 'getlastmodified', ''))
            if modified is not None:
                modified = datetime.datetime(*modified[:6])
            files[name] = {
                'name': name,
                'size': size,
                'isdir': isdir,
                'modified': modified,
            }

        return files

    def DeleteFile(self, path, timeout=5):
        response = self._webclient.Request('DELETE', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')), timeout=timeout)
        if response.status_code not in [204, 404]:
            raise ControllerClientError(response.content)

    def DeleteDirectory(self, path, timeout=5):
        self.DeleteFile(path, timeout=timeout)

    def MakeDirectory(self, path, timeout=5):
        response = self._webclient.Request('MKCOL', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')), timeout=timeout)
        if response.status_code not in [201, 301, 405]:
            raise ControllerClientError(response.content)

    def MakeDirectories(self, path, timeout=5):
        parts = []
        for part in path.strip('/').split('/'):
            parts.append(part)
            self.MakeDirectory('/'.join(parts), timeout=timeout)
