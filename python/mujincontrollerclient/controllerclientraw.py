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
import requests.adapters

from . import json
from . import APIServerError

import logging
log = logging.getLogger(__name__)


class ControllerWebClient(object):

    _baseurl = None  # base url of the controller
    _username = None  # username to login with
    _password = None  # password to login with
    _headers = None  # prepared headers for all requests
    _isok = False  # flag to stop
    _session = None  # requests session object

    def __init__(self, baseurl, username, password, locale=None):
        self._baseurl = baseurl
        self._username = username
        self._password = password
        self._headers = {}
        self._isok = True

        # create session
        self._session = requests.Session()

        # use basic auth
        self._session.auth = requests.auth.HTTPBasicAuth(self._username, self._password)

        # set csrftoken
        # any string can be the csrftoken
        self._headers['X-CSRFToken'] = 'csrftoken'
        self._session.cookies.set('csrftoken', self._headers['X-CSRFToken'], path='/')

        # add retry to deal with closed keep alive connections
        self._session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
        self._session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))

        # set locale headers
        self.SetLocale(locale)

    def __del__(self):
        self.Destroy()

    def Destroy(self):
        self.SetDestroy()

    def SetDestroy(self):
        self._isok = False

    def SetLocale(self, locale=None):
        locale = locale or os.environ.get('LANG', None)

        # convert locale to language code for http requests
        # en_US.UTF-8 => en-us
        # en_US => en-us
        # en => en
        language = 'en'  # default to en
        if locale is not None and len(locale) > 0:
            language = locale.split('.', 1)[0].replace('_', '-').lower()
        self._headers['Accept-Language'] = language

    def Request(self, method, path, timeout=5, headers=None, **kwargs):
        url = self._baseurl + path

        # set all the headers prepared for this client
        headers = dict(headers or {})
        headers.update(self._headers)

        return self._session.request(method=method, url=url, timeout=timeout, headers=headers, **kwargs)

    # python port of the javascript API Call function
    def APICall(self, method, path='', params=None, fields=None, data=None, headers=None, timeout=5):
        path = '/api/v1/' + path.lstrip('/')
        if not path.endswith('/'):
            path += '/'

        if params is None:
            params = {}

        params['format'] = 'json'

        if fields is not None:
            params['fields'] = fields

        # implicit order by pk, is this necessary?
        # if 'order_by' not in params:
        #     params['order_by'] = 'pk'

        if data is None:
            data = {}

        if headers is None:
            headers = {}

        # default to json content type
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
            data = json.dumps(data)

        if 'Accept' not in headers:
            headers['Accept'] = 'application/json'

        method = method.upper()

        # log.debug('%s %s', method, self._baseurl + path)
        response = self.Request(method, path, params=params, data=data, headers=headers, timeout=timeout)

        # try to parse response
        raw = response.content.decode('utf-8', 'replace').strip()
        content = None
        if len(raw) > 0:
            try:
                content = json.loads(raw)
            except ValueError as e:
                log.exception('caught exception parsing json response: %s: %s', e, raw)

        # first check error
        if content is not None and 'error_message' in content:
            raise APIServerError(content['error_message'], stacktrace=content.get('stacktrace', None), errorcode=content.get('error_code', None))
        if response.status_code >= 400:
            raise APIServerError(raw)

        # check expected status code
        expectedStatusCode = {
            'GET': 200,
            'HEAD': 200,
            'POST': 201,
            'DELETE': 204,
            'PUT': 202,
        }.get(method, 200)
        if response.status_code != expectedStatusCode:
            log.error('response status code is %d, expecting %d: %s', response.status_code, expectedStatusCode, raw)
            raise APIServerError(raw)

        return content
