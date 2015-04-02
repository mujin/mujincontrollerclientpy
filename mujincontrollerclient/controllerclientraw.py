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
import requests
import requests.auth
import time
import logging
import socket
log = logging.getLogger(__name__)

try:
    import simplejson as json
except ImportError:
    import json

from . import APIServerError, FluidPlanningError, BinPickingError, HandEyeCalibrationError, TimeoutError, AuthenticationError

class ControllerWebClient(object):
    _baseurl = None
    _username = None
    _password = None
    _isloggedin = False
    _session = None
    _csrftoken = None

    def __init__(self, baseurl, username, password):
        self._baseurl = baseurl
        self._username = username
        self._password = password
        self._isloggedin = False
        self._session = requests.Session()
        self._csrftoken = None

    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self._csrftoken = None
        self._isloggedin = False
        if self._session is not None:
            self._session.close()
            self._session = None
            
    def RestartPlanningServer(self):
        response = self._session.post(self._baseurl + '/restartserver/')
        assert response.status_code == requests.codes.ok
        return response.json()
 
    def Login(self, timeout=5):
        if self._isloggedin:
            return

        self._session.auth = requests.auth.HTTPBasicAuth(self._username, self._password)

        response = self._session.get('%s/login/' % self._baseurl, timeout=timeout)
        if response.status_code != requests.codes.ok:
            raise AuthenticationError(u'Failed to authenticate: %r' % response.content)

        csrftoken = response.cookies.get('csrftoken', None)

        data = {
            'username': self._username,
            'password': self._password,
            'this_is_the_login_form': '1',
            'next': '/',
        }

        headers = {
            'X-CSRFToken': csrftoken,
        }

        response = self._session.post('%s/login/' % self._baseurl, data=data, headers=headers, timeout=timeout)

        if response.status_code != requests.codes.ok:
            raise AuthenticationError(u'Failed to authenticate: %r' % response.content)

        self._csrftoken = csrftoken
        self._isloggedin = True

    def IsLoggedIn(self):
        return self._isloggedin
        
    # python port of the javascript API Call function
    def APICall(self, request_type, api_url, url_params=None, fields=None, data=None, timeout=5):
        if not self.IsLoggedIn():
            self.Login()

        if not api_url.endswith('/'):
            api_url += '/'

        url = self._baseurl + '/api/v1/' + api_url + '?format=json'
        
        if url_params is None:
            url_params = {}
            
        if fields is not None:
            url_params['fields'] = fields
            
        # implicit order by pk
        if 'order_by' not in url_params:
            url_params['order_by'] = 'pk'
            
        for param, value in url_params.iteritems():
            url += '&' + str(param) + '=' + str(value)
        
        if data is None:
            data = {}

        headers = {}
        if self._csrftoken:
            headers['X-CSRFToken'] = self._csrftoken
            
        request_type = request_type.upper()
        
        log.debug('%s %s', request_type, url)
        response = self._session.request(method=request_type, url=url, data=json.dumps(data), timeout=timeout, headers=headers)
        
        if request_type == 'DELETE' and response.status_code == 204:
            # just return without doing anything for deletes
            return response.status_code, response.content

        # try to convert everything else
        error_base = u'\n\nError with %s to %s\n\nThe API call failed (status: %s)' % (request_type, url, response.status_code)
        content = None
        try:
            content = json.loads(response.content)
        except ValueError:
            # either response was empty or not JSON
            raise APIServerError(u'%s, here is what came back in the request:\n%s' % (error_base, response.content.encode('utf-8')))
        
        if 'traceback' in content:
            raise APIServerError('%s, here is the stack trace that came back in the request:\n%s' % (error_base, content['traceback'].encode('utf-8')))
        
        return response.status_code, content
            
    def GetOrCreateTask(self, scenepk, taskname, tasktype=None, timeout=5):
        """gets or creates a task, returns its pk
        """
        status, response = self.APICall(u'GET', u'scene/%s/task' % scenepk, url_params={'limit': 1, 'name': taskname, 'fields': 'pk,tasktype'}, timeout=timeout)
        assert(status == 200)
        if len(response['objects']) > 0:
            if tasktype is not None:
                assert(response['objects'][0]['tasktype'] == tasktype)
            return response['objects'][0]['pk']
        else:
            status, response = self.APICall(u'POST', u'scene/%s/task' % scenepk, url_params={'fields': 'pk'}, data={"name": taskname, "tasktype": tasktype, "scenepk": scenepk}, timeout=timeout)
            assert(status == 201)
            return response['pk']
        
    def ExecuteFluidTask(self, scenepk, taskparameters, timeout=1000):
        """
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        """
        taskpk = self.GetOrCreateTask(scenepk, 'test0', 'fluidplanning')
        # set the task parameters
        self.APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'fluidplanning', 'taskparameters': taskparameters}, timeout=5)
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
            while True:
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
                                raise FluidPlanningError(result['errormessage'])
                            return result['output']
                except socket.error, e:
                    log.error(e)
                    
                # tasks can be long, so sleep
                time.sleep(1)
        finally:
            if jobpk is not None:
                log.info('deleting previous job')
                self.APICall('DELETE', 'job/%s' % jobpk, timeout=timeout)
                    
    def ExecuteBinPickingTaskSync(self, scenepk, taskparameters, forcecancel=False, timeout=1000):
        '''
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        :param forcecancel: if True, then cancel all previously running jobs before running this one
        '''
        taskpk = self.GetOrCreateTask(scenepk, 'binpickingtask1', 'binpicking')
        # set the task parameters
        self.APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'binpicking', 'taskparameters': taskparameters}, timeout=5)
        if forcecancel:
            # # just in case, delete all previous tasks
            self.APICall('DELETE', 'job', timeout=5)
        # execute the task
        status, response = self.APICall('POST', u'scene/%s/task/%s/result' % (scenepk, taskpk), timeout=timeout)
        assert(status == 200)
        return response
        
    def ExecuteBinPickingTask(self, scenepk, taskparameters, timeout=1000):
        """
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        """
        taskpk = self.GetOrCreateTask(scenepk, 'binpickingtask1', 'binpicking')
        # set the task parameters
        self.APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'binpicking', 'taskparameters': taskparameters}, timeout=5)
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
            while True:
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
                time.sleep(.1)
                
        finally:
            if jobpk is not None:
                log.info('deleting previous job')
                self.APICall('DELETE', 'job/%s' % jobpk, timeout=timeout)
                    
    def ExecuteHandEyeCalibrationTaskSync(self, scenepk, taskparameters):
        '''
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        '''
        taskpk = self.GetOrCreateTask(scenepk, 'handeyecalibrationtask1', 'handeyecalibration')
        # set the task parameters
        self.APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'handeyecalibration', 'taskparameters': taskparameters}, timeout=5)
        # # just in case, delete all previous tasks
        self.APICall('DELETE', 'job', timeout=5)
        # execute the task
        status, response = self.APICall('POST', u'scene/%s/task/%s/result' % (scenepk, taskpk), timeout=timeout)
        assert(status == 200)
        return response
        
    def ExecuteHandEyeCalibrationTaskAsync(self, scenepk, taskparameters, timeout=1000):
        """
        :param taskparameters: a dictionary with the following values: targetname, destinationname, robot, command, manipname, returntostart, samplingtime
        """
        taskpk = self.GetOrCreateTask(scenepk, 'handeyecalibrationtask1', 'handeyecalibration')
        # set the task parameters
        self.APICall('PUT', u'scene/%s/task/%s' % (scenepk, taskpk), data={'tasktype': 'handeyecalibration', 'taskparameters': taskparameters}, timeout=5)
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
            while True:
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
                time.sleep(.1)
                
        finally:
            if jobpk is not None:
                log.info('deleting previous job')
                self.APICall('DELETE', 'job/%s' % jobpk, timeout=timeout)

    def GetObjects(self, scenepk, timeout=5):
        """returns all the objects and their translations/rotations
        """
        status, response = self.APICall('GET', u'scene/%s/instobject' % (scenepk), data={}, timeout=timeout)
        instobjects = {}
        for objvalues in response['instobjects']:
            instobjects[objvalues['name']] = objvalues
        return instobjects
        
    def UpdateObjects(self, scenepk, objectdata, timeout=5):
        """updates the objects. objectdata is in the same format as returned by GetObjects
        """
        objects = []
        for name, values in objectdata.iteritems():
            objects.append({'pk': values['pk'], 'quaternion': list(values['quaternion']), 'translate': list(values['translate'])})
        status, response = self.APICall('PUT', u'scene/%s/instobject' % (scenepk), data={'objects': objects}, timeout=timeout)
        return response
