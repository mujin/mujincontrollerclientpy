# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import requests
import requests.auth
import time

import logging
log = logging.getLogger(__name__)

try:
    import ujson as json
except ImportError:
    import json

from . import ControllerClientError
from . import APIServerError, AuthenticationError, GetAPIServerErrorFromWeb
from . import ugettext as _

class ControllerWebClient(object):
    _baseurl = None
    _username = None
    _password = None
    _session = None
    _csrftoken = None
    _locale = None
    _language = None
    _isok = False

    def __init__(self, baseurl, username, password, locale=None):
        self._baseurl = baseurl
        self._username = username
        self._password = password
        self._session = None
        self._csrftoken = None
        self._locale = None
        self._language = None

        self._isok = True
        self.SetLocale(locale)

    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self.SetDestroy()
        self.Logout()

    def SetDestroy(self):
        self._isok = False

    def SetLocale(self, locale=None):
        self._locale = locale or os.environ.get('LANG', None)

        # convert locale to language code for http requests
        # en_US.UTF-8 => en-us
        # en_US => en-us
        # en => en
        self._language = 'en' # default to en
        if self._locale is not None and len(self._locale) > 0:
            self._language = self._locale.split('.', 1)[0].replace('_', '-').lower()

    def Login(self, timeout=5):
        session = requests.Session()
        session.auth = requests.auth.HTTPBasicAuth(self._username, self._password)

        headers = {
            'Accept-Language': self._language,
        }
        response = session.get('%s/login/' % self._baseurl, headers=headers, timeout=timeout)
        if response.status_code != requests.codes.ok:
            raise AuthenticationError(_('Failed to authenticate: %r') % response.content.decode('utf-8'))

        csrftoken = response.cookies.get('csrftoken', None)

        data = {
            'username': self._username,
            'password': self._password,
            'this_is_the_login_form': '1',
            'next': '/',
        }

        headers = {
            'X-CSRFToken': csrftoken,
            'Accept-Language': self._language,
        }
        response = session.post('%s/login/' % self._baseurl, data=data, headers=headers, timeout=timeout)

        if response.status_code != requests.codes.ok:
            raise AuthenticationError(_('Failed to authenticate: %r') % response.content.decode('utf-8'))

        self._session = session
        self._csrftoken = csrftoken

    def Logout(self):
        self._csrftoken = None
        if self._session is not None:
            self._session.close()
            self._session = None

    def IsLoggedIn(self):
        if self._session is None:
            return False
        sessionidexpires = 0
        csrftokenexpires = 0
        for cookie in self._session.cookies:
            if cookie.name == 'sessionid':
                sessionidexpires = cookie.expires
            elif cookie.name == 'csrftoken':
                csrftokenexpires = cookie.expires
        if sessionidexpires < int(time.time()) + 60:
            log.warn('sessionid cookie has expired or will expire in less than a minute.')
            return False
        if csrftokenexpires < int(time.time()) + 60:
            log.warn('csrftoken cookie has expired or will expire in less than a minute.')
            return False
        return True

    def Request(self, method, path, timeout=5, headers=None, **kwargs):
        if not self.IsLoggedIn():
            self.Login(timeout=timeout)

        url = self._baseurl + path

        if headers is None:
            headers = {}

        headers['Accept-Language'] = self._language
        if self._csrftoken:
            headers['X-CSRFToken'] = self._csrftoken

        return self._session.request(method=method, url=url, timeout=timeout, headers=headers, **kwargs)
	
    # python port of the javascript API Call function
    def APICall(self, request_type, api_url='', url_params=None, fields=None, data=None, headers=None, timeout=5):
        if timeout < 1e-6:
            raise ControllerClientError('timeout value (%s sec) is too small' % timeout)

        path = '/api/v1/' + api_url.lstrip('/')
        if not path.endswith('/'):
            path += '/'

        if url_params is None:
            url_params = {}

        url_params['format'] = 'json'

        if fields is not None:
            url_params['fields'] = fields

        # implicit order by pk
        if 'order_by' not in url_params:
            url_params['order_by'] = 'pk'

        if data is None:
            data = {}

        if headers is None:
            headers = {}

        # default to json content type
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(data)

        request_type = request_type.upper()

        log.verbose('%s %s', request_type, self._baseurl + path)
        response = self.Request(request_type, path, params=url_params, data=data, headers=headers, timeout=timeout)

        if request_type == 'HEAD' and response.status_code == 200:
            # just return without doing anything for head
            return response.status_code, response.content

        if request_type == 'DELETE' and response.status_code == 204:
            # just return without doing anything for deletes
            return response.status_code, response.content

        # try to convert everything else
        try:
            content = json.loads(response.content)
        except ValueError, e:
            log.warn(u'caught exception during json decode for content (%r): %s', response.content.decode('utf-8'), e)
            self.Logout() # always logout the session when we hit an error
            raise GetAPIServerErrorFromWeb(request_type, self._baseurl + path, response.status_code, response.content)
        
        if 'stacktrace' in content or response.status_code >= 400:
            self.Logout() # always logout the session when we hit an error
            raise GetAPIServerErrorFromWeb(request_type, self._baseurl + path, response.status_code, response.content)
        
        return response.status_code, content


    def GetOrCreateTask(self, scenepk, taskname, tasktype=None, slaverequestid='', timeout=5):
        """gets or creates a task, returns its pk
        """
        status, response = self.APICall(u'GET', u'scene/%s/task' % scenepk, url_params={'limit': 1, 'name': taskname, 'fields': 'pk,tasktype'}, timeout=timeout)
        assert(status == 200)
        if len(response['objects']) > 0:
            if tasktype is not None:
                assert(response['objects'][0]['tasktype'] == tasktype)
            return response['objects'][0]['pk']
        else:
            status, response = self.APICall(u'POST', u'scene/%s/task' % scenepk, url_params={'fields': 'pk'}, data={"name": taskname, "tasktype": tasktype, "scenepk": scenepk, 'slaverequestid': slaverequestid}, timeout=timeout)
            assert(status == 201)
            return response['pk']
    
    def ExecuteBinPickingTaskSync(self, scenepk, taskparameters, forcecancel=False, slaverequestid='', timeout=1000):
        '''
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        :param forcecancel: if True, then cancel all previously running jobs before running this one
        '''
        taskpk = self.GetOrCreateTask(scenepk, 'binpickingtask1', 'binpicking')
        # set the task parameters
        self.APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'binpicking', 'taskparameters': taskparameters, 'slaverequestid': slaverequestid}, timeout=5)
        if forcecancel:
            # # just in case, delete all previous tasks
            self.APICall('DELETE', 'job', timeout=5)
        # execute the task
        status, response = self.APICall('POST', u'scene/%s/task/%s/result' % (scenepk, taskpk), timeout=timeout)
        assert(status == 200)
        return response

    def ExecuteTaskSync(self, scenepk, tasktype, taskparameters, forcecancel=False, slaverequestid='', timeout=1000):
        '''executes task with a particular task type without creating a new task
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        :param forcecancel: if True, then cancel all previously running jobs before running this one
        '''
        if forcecancel:
            # # just in case, delete all previous tasks
            self.APICall('DELETE', 'job', timeout=5)
        # execute task
        status, response = self.APICall('GET', u'scene/%s/resultget' % (scenepk), data={'tasktype': tasktype, 'taskparameters': taskparameters, 'slaverequestid': slaverequestid}, timeout=timeout)
        assert(status==200)
        return response

    def ExecuteBinPickingTask(self, scenepk, taskparameters, slaverequestid='', timeout=1000):
        """
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        """
        taskpk = self.GetOrCreateTask(scenepk, 'binpickingtask1', 'binpicking')
        # set the task parameters
        self.APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'binpicking', 'taskparameters': taskparameters, 'slaverequestid': slaverequestid}, timeout=5)
        # just in case, delete all previous tasks
        self.APICall('DELETE', 'job', timeout=5)
        # execute the task
        #status, response = _APICall('POST', u'scene/%s/task/%s'%(scenepk, taskpk))
        status, response = self.APICall('POST', u'job', data={'resource_type': 'task', 'target_pk': taskpk}, timeout=timeout)
        assert(status == 200)
        # the jobpk allows us to track the job
        jobpk = response['jobpk']
        # query the task results
        status_text_prev = None
        starttime = time.time()
        try:
            while self._isok:
                try:
                    if timeout is not None and time.time() - starttime > timeout:
                        raise TimeoutError('failed to get result in time, quitting')
                    try:
                        status, response = self.APICall('GET', u'job/%s' % jobpk, timeout=5)
                        if status == 200:
                            if status_text_prev is not None and status_text_prev != response['status_text']:
                                log.info(response['status_text'])
                            status_text_prev = response['status_text']

                        jobstatus = response['status']
                    except APIServerError, e:
                        # most likely job finished
                        log.warn(u'problem with requesting job: %s', e)
                        jobstatus = '2'
                    if jobstatus == '2' or jobstatus == '3' or jobstatus == '4' or jobstatus == '5' or jobstatus == '8':
                        # job finished, so check for results:
                        status, response = self.APICall('GET', u'task/%s/result' % taskpk, url_params={'limit': 1, 'optimization': 'None'}, timeout=5)
                        assert(status == 200)
                        if len(response['objects']) > 0:
                            # have a response, so return!
                            jobpk = None
                            result = response['objects'][0]
                            if 'errormessage' in result and len(result['errormessage']) > 0:
                                raise BinPickingError(result['errormessage'])
                            return result['output']
                except socket.error, e:
                    log.error(e)

                # tasks can be long, so sleep
                time.sleep(0.1)

        finally:
            if jobpk is not None:
                log.info('deleting previous job')
                self.APICall('DELETE', 'job/%s' % jobpk, timeout=timeout)

    def ExecuteHandEyeCalibrationTaskSync(self, scenepk, taskparameters, slaverequestid=''):
        '''
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        '''
        taskpk = self.GetOrCreateTask(scenepk, 'handeyecalibrationtask1', 'handeyecalibration')
        # set the task parameters
        self.APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'handeyecalibration', 'taskparameters': taskparameters, 'slaverequestid': slaverequestid}, timeout=5)
        # # just in case, delete all previous tasks
        self.APICall('DELETE', 'job', timeout=5)
        # execute the task
        status, response = self.APICall('POST', u'scene/%s/task/%s/result' % (scenepk, taskpk), timeout=timeout)
        assert(status == 200)
        return response

    def ExecuteHandEyeCalibrationTaskAsync(self, scenepk, taskparameters, slaverequestid='', timeout=1000):
        """
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        """
        taskpk = self.GetOrCreateTask(scenepk, 'handeyecalibrationtask1', 'handeyecalibration')
        # set the task parameters
        self.APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'handeyecalibration', 'taskparameters': taskparameters, 'slaverequestid': slaverequestid}, timeout=5)
        # just in case, delete all previous tasks
        self.APICall('DELETE', 'job', timeout=5)
        # execute the task
        status, response = self.APICall('POST', u'scene/%s/task/%s' % (scenepk, taskpk), timeout=timeout)
        assert(status == 200)
        # the jobpk allows us to track the job
        jobpk = response['jobpk']
        # query the task results
        status_text_prev = None
        starttime = time.time()
        try:
            while self._isok:
                try:
                    if timeout is not None and time.time() - starttime > timeout:
                        raise TimeoutError('failed to get result in time, quitting')
                    try:
                        status, response = self.APICall('GET', u'job/%s' % jobpk, timeout=5)
                        if status == 200:
                            if status_text_prev is not None and status_text_prev != response['status_text']:
                                log.info(response['status_text'])
                            status_text_prev = response['status_text']

                        jobstatus = response['status']
                    except APIServerError, e:
                        # most likely job finished
                        log.warn(u'problem with requesting job: %s', e)
                        jobstatus = '2'
                    if jobstatus == '2' or jobstatus == '3' or jobstatus == '4' or jobstatus == '5' or jobstatus == '8':
                        # job finished, so check for results:
                        status, response = self.APICall('GET', u'task/%s/result' % taskpk, url_params={'limit': 1, 'optimization': 'None'}, timeout=5)
                        assert(status == 200)
                        if len(response['objects']) > 0:
                            # have a response, so return!
                            jobpk = None
                            result = response['objects'][0]
                            if 'errormessage' in result and len(result['errormessage']) > 0:
                                raise HandEyeCalibrationError(result['errormessage'])
                            return result['output']

                except socket.error, e:
                    log.error(e)

                # tasks can be long, so sleep
                time.sleep(0.1)

        finally:
            if jobpk is not None:
                log.info('deleting previous job')
                self.APICall('DELETE', 'job/%s' % jobpk, timeout=timeout)
