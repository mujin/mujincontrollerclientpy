# -*- coding: utf-8 -*-
# Copyright (C) 2012-2015 MUJIN Inc
"""
Mujin controller client
"""

# system imports
import os
import datetime
import base64
import email.utils

# mujin imports
from . import ControllerClientError
from . import controllerclientraw
from . import ugettext as _
from . import json
from . import urlparse
from . import uriutils

# logging
import logging
log = logging.getLogger(__name__)


def GetFilenameFromURI(uri, mujinpath):
    """returns the filesystem path that the URI points to.
    :param uri: points to mujin:/ resource

    example:

      GetFilenameFromURI(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae',u'/var/www/media/u/testuser')
      returns: (ParseResult(scheme=u'mujin', netloc='', path=u'/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae', params='', query='', fragment=''), u'/var/www/media/u/testuser/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae')
    """
    mri = uriutils.MujinResourceIdentifier(uri=uri, mujinPath=mujinpath, fragmentSeparator=uriutils.FRAGMENT_SEPARATOR_AT)
    return mri.parseResult, mri.filename


def GetURIFromPrimaryKey(pk):
    """Given the encoded primary key (has to be str object), returns the unicode URL.
    If pk is a unicode object, will use inside url as is, otherwise will decode

    example:

      GetURIFromPrimaryKey('%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122')
      returns: u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae'
    """
    return uriutils.GetURIFromPrimaryKey(pk, primaryKeySeparator=uriutils.PRIMARY_KEY_SEPARATOR_AT, fragmentSeparator=uriutils.FRAGMENT_SEPARATOR_AT)


def GetUnicodeFromPrimaryKey(pk):
    """Given the encoded primary key (has to be str object), returns the unicode string.
    If pk is a unicode object, will return the string as is.

    example:

      GetUnicodeFromPrimaryKey('%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122')
      returns: u'\u691c\u8a3c\u52d5\u4f5c1_121122'
    """
    return uriutils.GetFilenameFromPrimaryKey(pk, primaryKeySeparator=uriutils.PRIMARY_KEY_SEPARATOR_AT)


def GetPrimaryKeyFromURI(uri):
    """
    example:

      GetPrimaryKeyFromURI(u'mujin:/\u691c\u8a3c\u52d5\u4f5c1_121122.mujin.dae')
      returns u'%E6%A4%9C%E8%A8%BC%E5%8B%95%E4%BD%9C1_121122'
    """
    return uriutils.GetPrimaryKeyFromURI(uri, fragmentSeparator=uriutils.FRAGMENT_SEPARATOR_AT, primaryKeySeparator=uriutils.PRIMARY_KEY_SEPARATOR_AT)


def _FormatHTTPDate(dt):
    """Return a string representation of a date according to RFC 1123 (HTTP/1.1).

    The supplied date must be in UTC.
    """
    weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][dt.weekday()]
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][dt.month - 1]
    return '%s, %02d %s %04d %02d:%02d:%02d GMT' % (weekday, dt.day, month, dt.year, dt.hour, dt.minute, dt.second)


class ControllerClient(object):
    """mujin controller client base
    """

    class ObjectsWrapper(list):
        """wrap response for list of objects, provides extra meta data
        """
        _meta = None  # meta dict returned from server

        def __init__(self, data):
            super(ControllerClient.ObjectsWrapper, self).__init__(data['objects'])
            self._meta = data['meta']

        @property
        def totalCount(self):
            return self._meta['total_count']

        @property
        def limit(self):
            return self._meta['limit']

        @property
        def offset(self):
            return self._meta['offset']

    _webclient = None
    _userinfo = None  # a dict storing user info, like locale

    controllerurl = ''  # url to controller
    controllerusername = ''  # username to login with
    controllerpassword = ''  # password to login with

    controllerIp = ''  # hostname of the controller web server
    controllerPort = 80  # port of the controller web server

    def __init__(self, controllerurl='http://127.0.0.1', controllerusername='', controllerpassword='', author=None):
        """logs into the mujin controller
        :param controllerurl: url of the mujin controller, e.g. http://controller14
        :param controllerusername: username of the mujin controller, e.g. testuser
        :param controllerpassword: password of the mujin controller
        """

        # parse controllerurl
        scheme, netloc, path, params, query, fragment = urlparse.urlparse(controllerurl)

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

        self.controllerurl = urlparse.urlunparse((scheme, netloc, '', '', '', ''))
        self.controllerusername = controllerusername or self.controllerusername
        self.controllerpassword = controllerpassword or self.controllerpassword

        self._userinfo = {
            'username': self.controllerusername,
            'locale': os.environ.get('LANG', ''),
        }
        self._webclient = controllerclientraw.ControllerWebClient(self.controllerurl, self.controllerusername, self.controllerpassword, author=author)

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
        return True

    def Login(self, timeout=5):
        """Force webclient to login if it is not currently logged in. Useful for checking that the credential works.
        """
        self.Ping(timeout=timeout)

    def Ping(self, usewebapi=True, timeout=5):
        """Sends a dummy HEAD request to api endpoint
        """
        assert(usewebapi)
        response = self._webclient.Request('HEAD', u'/u/%s' % self.controllerusername, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(_('failed to ping controller, status code is: %d') % response.status_code)

    def SetLogLevel(self, level, timeout=5):
        """ Set webstack log level
        """
        response = self._webclient.Request('POST', '/loglevel/', data={'level': level}, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(_('failed to set webstack log level, status code is: %d') % response.status_code)

    #
    # Scene related
    #

    def UploadSceneFile(self, f, timeout=5):
        """uploads a file managed by file handle f

        """
        return self.UploadFile(f, timeout=timeout)['filename']

    def GetScenes(self, fields=None, offset=0, limit=0, usewebapi=True, timeout=5, **kwargs):
        """list all available scene on controller
        """
        assert(usewebapi)
        params = {
            'offset': offset,
            'limit': limit,
        }
        params.update(kwargs)
        return self.ObjectsWrapper(self._webclient.APICall('GET', u'scene/', fields=fields, timeout=timeout, params=params))

    def GetScene(self, pk, fields=None, usewebapi=True, timeout=5):
        """returns requested scene
        """
        assert(usewebapi)
        return self._webclient.APICall('GET', u'scene/%s/' % pk, fields=fields, timeout=timeout)

    def GetObject(self, pk, fields=None, usewebapi=True, timeout=5):
        """returns requested object
        """
        assert(usewebapi)
        return self._webclient.APICall('GET', u'object/%s/' % pk, fields=fields, timeout=timeout)

    def SetObject(self, pk, objectdata, fields=None, usewebapi=True, timeout=5):
        """do partial update on object resource
        """
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'object/%s/' % pk, data=objectdata, fields=fields, timeout=timeout)

    def GetRobot(self, pk, fields=None, usewebapi=True, timeout=5):
        """returns requested robot
        """
        assert(usewebapi)
        return self._webclient.APICall('GET', u'robot/%s/' % pk, fields=fields, timeout=timeout)

    def SetRobot(self, pk, robotdata, fields=None, usewebapi=True, timeout=5):
        """do partial update on robot resource
        """
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'robot/%s/' % pk, data=robotdata, fields=fields, timeout=timeout)

    #
    # Scene related
    #

    def CreateScene(self, scenedata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('POST', u'scene/', data=scenedata, fields=fields, timeout=timeout)

    def SetScene(self, scenepk, scenedata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'scene/%s/' % scenepk, data=scenedata, fields=fields, timeout=timeout)

    def DeleteScene(self, scenepk, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('DELETE', u'scene/%s/' % scenepk, timeout=timeout)

    #
    # InstObject related
    #

    def CreateSceneInstObject(self, scenepk, instobjectdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('POST', u'scene/%s/instobject/' % scenepk, data=instobjectdata, fields=fields, timeout=timeout)

    def GetSceneInstObjects(self, scenepk, fields=None, usewebapi=True, timeout=5):
        """ returns the instance objects of the scene
        """
        assert(usewebapi)
        return self.ObjectsWrapper(self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, fields=fields, timeout=timeout))

    def GetSceneInstObject(self, scenepk, instobjectpk, fields=None, usewebapi=True, timeout=5):
        """ returns the instance objects of the scene
        """
        assert(usewebapi)
        return self._webclient.APICall('GET', u'scene/%s/instobject/%s' % (scenepk, instobjectpk), fields=fields, timeout=timeout)

    def SetSceneInstObject(self, scenepk, instobjectpk, instobjectdata, fields=None, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'scene/%s/instobject/%s/' % (scenepk, instobjectpk), data=instobjectdata, fields=fields, timeout=timeout)

    def DeleteSceneInstObject(self, scenepk, instobjectpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('DELETE', u'scene/%s/instobject/%s/' % (scenepk, instobjectpk), timeout=timeout)

    #
    # IKParam related
    #

    def CreateObjectIKParam(self, objectpk, ikparamdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('POST', u'object/%s/ikparam/' % objectpk, data=ikparamdata, fields=fields, timeout=timeout)

    def SetObjectIKParam(self, objectpk, ikparampk, ikparamdata, fields=None, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'object/%s/ikparam/%s/' % (objectpk, ikparampk), data=ikparamdata, fields=fields, timeout=timeout)

    def DeleteObjectIKParam(self, objectpk, ikparampk, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('DELETE', u'object/%s/ikparam/%s/' % (objectpk, ikparampk), timeout=timeout)

    #
    # GraspSet related
    #

    def CreateObjectGraspSet(self, objectpk, graspsetdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('POST', u'object/%s/graspset/' % objectpk, data=graspsetdata, fields=fields, timeout=timeout)

    def SetObjectGraspSet(self, objectpk, graspsetpk, graspsetdata, fields=None, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'object/%s/graspset/%s/' % (objectpk, graspsetpk), data=graspsetdata, fields=fields, timeout=timeout)

    def DeleteObjectGraspSet(self, objectpk, graspsetpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('DELETE', u'object/%s/graspset/%s/' % (objectpk, graspsetpk), timeout=timeout)

    #
    # Link related
    #

    def CreateObjectLink(self, objectpk, linkdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('POST', u'object/%s/link/' % objectpk, data=linkdata, fields=fields, timeout=timeout)

    def SetObjectLink(self, objectpk, linkpk, linkdata, fields=None, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'object/%s/link/%s/' % (objectpk, linkpk), data=linkdata, fields=fields, timeout=timeout)

    def GetObjectLinks(self, objectpk, fields=None, usewebapi=True, timeout=5):
        """ returns the instance objects of the scene
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'object/%s/link/' % (objectpk), fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def GetObjectLink(self, objectpk, linkpk, fields=None, usewebapi=True, timeout=5):
        """ returns the instance objects of the scene
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'object/%s/link/%s/' % (objectpk, linkpk), fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def DeleteObjectLink(self, objectpk, linkpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('DELETE', u'object/%s/link/%s/' % (objectpk, linkpk), timeout=timeout)

    #
    # Attachment related
    #

    def CreateObjectAttachment(self, objectpk, attachmentdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('POST', u'object/%s/attachment/' % objectpk, data=attachmentdata, fields=fields, timeout=timeout)

    def SetObjectAttachment(self, objectpk, attachmentpk, attachmentdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'object/%s/attachment/%s/' % (objectpk, attachmentpk), data=attachmentdata, fields=fields, timeout=timeout)

    def DeleteObjectAttachment(self, objectpk, attachmentpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('DELETE', u'object/%s/attachment/%s/' % (objectpk, attachmentpk), timeout=timeout)

    #
    # Geometry related
    #

    def CreateObjectGeometry(self, objectpk, geometrydata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('POST', u'object/%s/geometry/' % objectpk, data=geometrydata, fields=fields, timeout=timeout)

    def SetObjectGeometry(self, objectpk, geometrypk, geometrydata, fields=None, usewebapi=True, timeout=5):
        """sets the instobject values via a WebAPI PUT call
        :param instobjectdata: key-value pairs of the data to modify on the instobject
        """
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'object/%s/geometry/%s/' % (objectpk, geometrypk), data=geometrydata, fields=fields, timeout=timeout)

    def GetObjectGeometryData(self, objectpk, geometrypk, fields=None, usewebapi=True, timeout=5):
        """ returns the instance objects of the scene
        """
        assert(usewebapi)
        status, response = self._webclient.APICall('GET', u'object/%s/geometry/%s/' % (objectpk, geometrypk), fields=fields, timeout=timeout)
        assert(status == 200)
        return response

    def SetObjectGeometryMesh(self, objectpk, geometrypk, data, formathint='stl', unit='mm', usewebapi=True, timeout=5):
        """upload binary file content of a cad file to be set as the mesh for the geometry
        """
        assert(usewebapi)
        assert(formathint == 'stl')  # for now, only support stl

        headers = {
            'Content-Type': 'application/sla',
        }
        params = {'unit': unit}
        return self._webclient.APICall('PUT', u'object/%s/geometry/%s/' % (objectpk, geometrypk), params=params, data=data, headers=headers, timeout=timeout)

    def DeleteObjectGeometry(self, objectpk, geometrypk, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('DELETE', u'object/%s/geometry/%s/' % (objectpk, geometrypk), timeout=timeout)

    def GetObjectGeometries(self, objectpk, mesh=False, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        params = {}
        if mesh:
            params['mesh'] = '1'
        return self._webclient.APICall('GET', u'object/%s/geometry/' % objectpk, params=params, fields=fields, timeout=timeout)['geometries']

    #
    # Object Tools related
    #

    def GetRobotTools(self, robotpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('GET', u'robot/%s/tool/' % robotpk, fields=fields, timeout=timeout)['tools']

    def GetRobotTool(self, robotpk, toolpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('GET', u'robot/%s/tool/%s/' % (robotpk, toolpk), fields=fields, timeout=timeout)

    def CreateRobotTool(self, robotpk, tooldata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('POST', u'robot/%s/tool/' % robotpk, data=tooldata, fields=fields, timeout=timeout)

    def SetRobotTool(self, robotpk, toolpk, tooldata, fields=None, usewebapi=True, timeout=5):
        """sets the tool values via a WebAPI PUT call
        :param tooldata: key-value pairs of the data to modify on the tool
        """
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'robot/%s/tool/%s/' % (robotpk, toolpk), data=tooldata, fields=fields, timeout=timeout)

    def DeleteRobotTool(self, robotpk, toolpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('DELETE', u'robot/%s/tool/%s/' % (robotpk, toolpk), timeout=timeout)

    #
    # InstObject Tools related
    #

    def GetInstRobotTools(self, scenepk, instobjectpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('GET', u'scene/%s/instobject/%s/tool/' % (scenepk, instobjectpk), fields=fields, timeout=timeout)['tools']

    def GetInstRobotTool(self, scenepk, instobjectpk, toolpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('GET', u'scene/%s/instobject/%s/tool/%s' % (scenepk, instobjectpk, toolpk), fields=fields, timeout=timeout)

    def CreateInstRobotTool(self, scenepk, instobjectpk, tooldata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('POST', u'scene/%s/instobject/%s/tool/' % (scenepk, instobjectpk), data=tooldata, fields=fields, timeout=timeout)

    def SetInstRobotTool(self, scenepk, instobjectpk, toolpk, tooldata, fields=None, usewebapi=True, timeout=5):
        """sets the tool values via a WebAPI PUT call
        :param tooldata: key-value pairs of the data to modify on the tool
        """
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'scene/%s/instobject/%s/tool/%s/' % (scenepk, instobjectpk, toolpk), data=tooldata, fields=fields, timeout=timeout)

    def DeleteInstRobotTool(self, scenepk, instobjectpk, toolpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('DELETE', u'scene/%s/instobject/%s/tool/%s/' % (scenepk, instobjectpk, toolpk), timeout=timeout)

    #
    # Attached sensors related
    #

    def CreateRobotAttachedSensor(self, robotpk, attachedsensordata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('POST', u'robot/%s/attachedsensor/' % robotpk, data=attachedsensordata, fields=fields, timeout=timeout)

    def SetRobotAttachedSensor(self, robotpk, attachedsensorpk, attachedsensordata, fields=None, usewebapi=True, timeout=5):
        """sets the attachedsensor values via a WebAPI PUT call
        :param attachedsensordata: key-value pairs of the data to modify on the attachedsensor
        """
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'robot/%s/attachedsensor/%s/' % (robotpk, attachedsensorpk), data=attachedsensordata, fields=fields, timeout=timeout)

    def SetRobotAttachedActuator(self, robotpk, attachedactuatorpk, attachedacturtordata, fields=None, usewebapi=True, timeout=5):
        """sets the attachedactuatorpk values via a WebAPI PUT call
        :param attachedacturtordata: key-value pairs of the data to modify on the attachedactuator
        """
        assert(usewebapi)
        return self._webclient.APICall('PUT', u'robot/%s/attachedactuator/%s/' % (robotpk, attachedactuatorpk), data=attachedacturtordata, fields=fields, timeout=timeout)

    def DeleteRobotAttachedSensor(self, robotpk, attachedsensorpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('DELETE', u'robot/%s/attachedsensor/%s/' % (robotpk, attachedsensorpk), timeout=timeout)

    #
    # Task related
    #

    def GetSceneTasks(self, scenepk, fields=None, offset=0, limit=0, tasktype=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        params = {
            'offset': offset,
            'limit': limit,
        }
        if tasktype:
            params['tasktype'] = tasktype
        return self.ObjectsWrapper(self._webclient.APICall('GET', u'scene/%s/task/' % scenepk, fields=fields, timeout=timeout, params=params))

    def GetSceneTask(self, scenepk, taskpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('GET', u'scene/%s/task/%s/' % (scenepk, taskpk), fields=fields, timeout=timeout)

    def CreateSceneTask(self, scenepk, taskdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('POST', u'scene/%s/task/' % scenepk, data=taskdata, fields=fields, timeout=timeout)

    def SetSceneTask(self, scenepk, taskpk, taskdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        self._webclient.APICall('PUT', u'scene/%s/task/%s/' % (scenepk, taskpk), data=taskdata, fields=fields, timeout=timeout)

    def DeleteSceneTask(self, scenepk, taskpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        self._webclient.APICall('DELETE', u'scene/%s/task/%s/' % (scenepk, taskpk), timeout=timeout)

    #
    # Result related
    #

    def GetResult(self, resultpk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self._webclient.APICall('GET', u'planningresult/%s/' % resultpk, fields=fields, timeout=timeout)

    def GetBinpickingResult(self, resultpk, fields=None, usewebapi=True, timeout=5):
        assert(UserWarning)
        return self._webclient.APICall('GET', u'binpickingresult/%s' % resultpk, fields=fields, timeout=timeout)

    def GetResultProgram(self, resultpk, programtype=None, format='dat', usewebapi=True, timeout=5):
        assert(usewebapi)
        params = {'format': format}
        if programtype is not None and len(programtype) > 0:
            params['type'] = programtype
        # custom http call because APICall currently only supports json
        response = self._webclient.Request('GET', u'/api/v1/planningresult/%s/program/' % resultpk, params=params, timeout=timeout)
        assert(response.status_code == 200)
        return response.content

    def SetResult(self, resultpk, resultdata, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        self._webclient.APICall('PUT', u'planningresult/%s/' % resultpk, data=resultdata, fields=fields, timeout=timeout)

    def DeleteResult(self, resultpk, usewebapi=True, timeout=5):
        assert(usewebapi)
        self._webclient.APICall('DELETE', u'planningresult/%s/' % resultpk, timeout=timeout)

    #
    # Job related
    #

    def GetJobs(self, fields=None, offset=0, limit=0, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self.ObjectsWrapper(self._webclient.APICall('GET', u'job/', fields=fields, timeout=timeout, params={
            'offset': offset,
            'limit': limit,
        }))

    def DeleteJob(self, jobpk, usewebapi=True, timeout=5):
        """ cancels the job with the corresponding jobk
        """
        assert(usewebapi)
        self._webclient.APICall('DELETE', u'job/%s/' % jobpk, timeout=timeout)

    def DeleteJobs(self, usewebapi=True, timeout=5):
        """ cancels all jobs
        """
        # cancel on the zmq configure socket first

        if usewebapi:
            self._webclient.APICall('DELETE', u'job/', timeout=timeout)

    #
    # Geometry related
    #

    def GetObjectGeometry(self, objectpk, usewebapi=True, timeout=5):
        """ return a list of geometries (a dictionary with key: positions, indices)) of given object
        """
        import numpy
        assert(usewebapi)
        response = self._webclient.APICall('GET', u'object/%s/scenejs/' % objectpk, timeout=timeout)
        geometries = []
        for encodedGeometry in response['geometries']:
            geometry = {}
            positions = numpy.fromstring(base64.b64decode(encodedGeometry['positions_base64']), dtype=float)
            positions.resize(len(positions) / 3, 3)
            geometry['positions'] = positions
            indices = numpy.fromstring(base64.b64decode(encodedGeometry['indices_base64']), dtype=numpy.uint32)
            indices.resize(len(indices) / 3, 3)
            geometry['indices'] = indices
            geometries.append(geometry)
        return geometries

    #
    # Instobject related
    #

    def GetSceneInstanceObjectsViaWebapi(self, scenepk, fields=None, usewebapi=True, timeout=5):
        assert(usewebapi)
        return self.ObjectsWrapper(self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, fields=fields, timeout=timeout))

    #
    # Sensor mappings related
    #

    def GetSceneSensorMapping(self, scenepk=None, usewebapi=True, timeout=5):
        """ return the camerafullname to cameraid mapping. e.g. {'sourcecamera/ensenso_l_rectified': '150353', 'sourcecamera/ensenso_r_rectified':'150353_Right' ...}
        """
        assert(usewebapi)
        if scenepk is None:
            scenepk = self.scenepk
        instobjects = self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, timeout=timeout)['objects']
        sensormapping = {}
        for instobject in instobjects:
            if len(instobject['attachedsensors']) > 0:
                attachedsensors = self._webclient.APICall('GET', u'robot/%s/attachedsensor/' % instobject['object_pk'])['attachedsensors']
                for attachedsensor in attachedsensors:
                    camerafullname = instobject['name'] + '/' + attachedsensor['name']
                    if 'hardware_id' in attachedsensor['sensordata']:
                        sensormapping[camerafullname] = attachedsensor['sensordata']['hardware_id']
                    else:
                        sensormapping[camerafullname] = None
                        log.warn(u'attached sensor %s/%s does not have hardware_id', instobject['name'], attachedsensor.get('name', None))
        return sensormapping

    def SetSceneSensorMapping(self, sensormapping, scenepk=None, usewebapi=True, timeout=5):
        """
        :param sensormapping: the camerafullname to cameraid mapping. e.g. {'sourcecamera/ensenso_l_rectified': '150353', 'sourcecamera/ensenso_r_rectified':'150353_Right' ...}
        """
        assert(usewebapi)
        if scenepk is None:
            scenepk = self.scenepk
        instobjects = self._webclient.APICall('GET', u'scene/%s/instobject/' % scenepk, params={'limit': 0}, fields='attachedsensors,object_pk,name', timeout=timeout)['objects']
        cameracontainernames = set([camerafullname.split('/')[0] for camerafullname in sensormapping.keys()])
        sensormapping = dict(sensormapping)
        for instobject in instobjects:
            if len(instobject['attachedsensors']) > 0 and instobject['name'] in cameracontainernames:
                cameracontainerpk = instobject['object_pk']
                attachedsensors = self._webclient.APICall('GET', u'robot/%s/attachedsensor/' % cameracontainerpk)['attachedsensors']
                for attachedsensor in attachedsensors:
                    camerafullname = instobject['name'] + '/' + attachedsensor['name']
                    cameraid = attachedsensor['sensordata'].get('hardware_id', None)
                    sensorpk = attachedsensor['pk']
                    if camerafullname in sensormapping.keys():
                        if cameraid != sensormapping[camerafullname]:
                            self._webclient.APICall('PUT', u'robot/%s/attachedsensor/%s' % (cameracontainerpk, sensorpk), data={'sensordata': {'hardware_id': str(sensormapping[camerafullname])}})
                        del sensormapping[camerafullname]
        if sensormapping:
            raise ControllerClientError(_('some sensors are not found in scene: %r') % sensormapping.keys())

    #
    # File related
    #

    def UploadFile(self, f, filename=None, timeout=10):
        """uploads a file managed by file handle f

        Returns:
            (dict) json response
        """
        data = {}
        if filename:
            data['filename'] = filename
        response = self._webclient.Request('POST', '/fileupload', files={'file': f}, data=data, timeout=timeout)
        if response.status_code in (200,):
            try:
                return response.json()
            except Exception as e:
                log.exception('failed to upload file: %s', e)
        raise ControllerClientError(response.content.decode('utf-8'))

    def DeleteFile(self, filename, timeout=10):
        response = self._webclient.Request('POST', '/file/delete/', data={'filename': filename}, timeout=timeout)
        if response.status_code in (200,):
            try:
                return response.json()['filename']
            except Exception as e:
                log.exception('failed to delete file: %s', e)
        raise ControllerClientError(response.content.decode('utf-8'))

    def ListFiles(self, dirname='', timeout=2):
        response = self._webclient.Request('GET', '/file/list/', params={'dirname': dirname}, timeout=timeout)
        if response.status_code in (200, 404):
            try:
                return response.json()
            except Exception as e:
                log.exception('failed to delete file: %s', e)
        raise ControllerClientError(response.content.decode('utf-8'))

    def FileExists(self, path, timeout=5):
        """check if a file exists on server
        """
        response = self._webclient.Request('HEAD', u'/u/%s/%s' % (self.controllerusername, path.rstrip('/')), timeout=timeout)
        if response.status_code not in [200, 301, 404]:
            raise ControllerClientError(response.content.decode('utf-8'))
        return response.status_code != 404

    def DownloadFile(self, filename, ifmodifiedsince=None, timeout=5):
        """downloads a file given filename

        :return: a streaming response
        """
        headers = {}
        if ifmodifiedsince:
            headers['If-Modified-Since'] = _FormatHTTPDate(ifmodifiedsince)
        response = self._webclient.Request('GET', u'/u/%s/%s' % (self.controllerusername, filename), headers=headers, stream=True, timeout=timeout)
        if ifmodifiedsince and response.status_code == 304:
            return response
        if response.status_code != 200:
            raise ControllerClientError(response.content.decode('utf-8'))
        return response

    def FlushAndDownloadFile(self, filename, timeout=5):
        """Flush and perform a HEAD operation on given filename to retrieve metadata.

        :return: a streaming response
        """
        response = self._webclient.Request('GET', '/file/download/', params={'filename': filename}, stream=True, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(response.content.decode('utf-8'))
        return response

    def FlushAndHeadFile(self, filename, timeout=5):
        """Flush and perform a HEAD operation on given filename to retrieve metadata.

        :return: a dict containing "modified (datetime.datetime)" and "size (int)"
        """
        response = self._webclient.Request('HEAD', '/file/download/', params={'filename': filename}, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(response.content.decode('utf-8'))
        return {
            'modified': datetime.datetime(*email.utils.parsedate(response.headers['Last-Modified'])[:6]),
            'size': int(response.headers['Content-Length']),
        }

    def HeadFile(self, filename, timeout=5):
        """Perform a HEAD operation on given filename to retrieve metadata.

        :return: a dict containing "modified (datetime.datetime)" and "size (int)"
        """
        path = u'/u/%s/%s' % (self.controllerusername, filename.rstrip('/'))
        response = self._webclient.Request('HEAD', path, timeout=timeout)
        if response.status_code not in [200]:
            raise ControllerClientError(response.content.decode('utf-8'))
        return {
            'modified': datetime.datetime(*email.utils.parsedate(response.headers['Last-Modified'])[:6]),
            'size': int(response.headers['Content-Length']),
        }

    def FlushCache(self, timeout=5):
        """flush pending changes in cache to disk
        """
        response = self._webclient.Request('POST', '/flushcache/', timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(response.content.decode('utf-8'))

    #
    # Log related
    #

    def GetUserLog(self, category, level='DEBUG', keyword=None, limit=None, cursor=None, includecursor=False, forward=False, timeout=2):
        """ restarts controller
        """
        params = {
            'keyword': (keyword or '').strip(),
            'cursor': (cursor or '').strip(),
            'includecursor': 'true' if includecursor else 'false',
            'forward': 'true' if forward else 'false',
            'limit': str(limit or 0),
            'level': level,
        }

        response = self._webclient.Request('GET', '/log/user/%s/' % category, params=params, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(_('Failed to retrieve user log, status code is %d') % response.status_code)
        return response.json()

    #
    # Query list of scenepks based on barcdoe field
    #

    def QueryScenePKsByBarcodes(self, barcodes, timeout=2):
        response = self._webclient.Request('GET', '/query/barcodes/', params={'barcodes': ','.join(barcodes)})
        if response.status_code != 200:
            raise ControllerClientError(_('Failed to query scenes based on barcode, status code is %d') % response.status_code)
        return response.json()

    #
    # Report stats to registration controller
    #

    def ReportStats(self, data, timeout=5):
        response = self._webclient.Request('POST', '/stats/', data=json.dumps(data), headers={'Content-Type': 'application/json'}, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(_('Failed to upload stats, status code is %d') % response.status_code)

    #
    # Config.
    #

    def GetConfig(self, timeout=5):
        response = self._webclient.Request('GET', '/config/', timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(_('Failed to retrieve configuration fron controller, status code is %d') % response.status_code)
        return response.json()

    def SetConfig(self, data, timeout=5):
        response = self._webclient.Request('PUT', '/config/', data=json.dumps(data), headers={'Content-Type': 'application/json'}, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(_('Failed to set configuration fron controller, status code is %d') % response.status_code)

    #
    # Reference Object PKs.
    #

    def ModifySceneAddReferenceObjectPK(self, scenepk, referenceobjectpk, timeout=5):
        """
        Add a referenceobjectpk to the scene.
        """
        response = self._webclient.Request('POST', '/referenceobjectpks/add/', data=json.dumps({
            'scenepk': scenepk,
            'referenceobjectpk': referenceobjectpk,
        }), headers={'Content-Type': 'application/json'}, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(_('Failed to add referenceobjectpk %r to scene %r, status code is %d') % (referenceobjectpk, scenepk, response.status_code))

    def ModifySceneRemoveReferenceObjectPK(self, scenepk, referenceobjectpk, timeout=5):
        """
        Remove a referenceobjectpk from the scene.
        """
        response = self._webclient.Request('POST', '/referenceobjectpks/remove/', data=json.dumps({
            'scenepk': scenepk,
            'referenceobjectpk': referenceobjectpk,
        }), headers={'Content-Type': 'application/json'}, timeout=timeout)
        if response.status_code != 200:
            raise ControllerClientError(_('Failed to remove referenceobjectpk %r from scene %r, status code is %d') % (referenceobjectpk, scenepk, response.status_code))
