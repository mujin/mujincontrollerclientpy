# -*- coding: utf-8 -*-

from functools import wraps

from . import _
from . import json
from . import ClientExceptionBase

import logging
log = logging.getLogger(__name__)

class ControllerGraphClientException(ClientExceptionBase):

    _statusCode = None
    _content = None

    def __init__(self, message='', statusCode=None, content=None):
        super(ControllerGraphClientException, self).__init__(message)
        self._statusCode = statusCode
        self._content = content

    @property
    def statusCode(self):
        return self._statusCode

    @property
    def content(self):
        return self._content


def _MakeSimpleGraphAPIDecorator(queryOrMutation, parameterTypes, queryFields='', timeout=5.0):
    def actual(func):
        @wraps(func)
        def wrapper(self, **kwargs):
            operationName = func.__name__
            queryParameters = ', '.join([
                '$%s: %s' % (parameterName, parameterType)
                for parameterName, parameterType in parameterTypes.items()
            ])
            if queryParameters:
                queryParameters = '(%s)' % queryParameters
            query = '%s %s%s\n' % (queryOrMutation, operationName, queryParameters)
            query += '{'
            queryArguments = ', '.join([
                '%s: $%s' % (parameterName, parameterName)
                for parameterName in parameterTypes.keys()
            ])
            if queryArguments:
                queryArguments = '(%s)' % queryArguments
            query += '    %s%s %s\n' % (operationName, queryArguments, queryFields)
            query += '}'
            variables = {}
            for parameterName in parameterTypes.keys():
                if parameterName not in kwargs:
                    raise ControllerGraphClientException(_('Missing parameter "%s" when calling "%s"') % (parameterName, operationName))
                variables[parameterName] = kwargs.pop(parameterName)
            data = self._ExecuteGraphAPI(operationName, query, variables, timeout=kwargs.pop('timeout', timeout))
            return data.get(operationName)
        return wrapper
    return actual


def SimpleGraphQueryDecorator(parameterTypes, queryFields='', timeout=5.0):
    return _MakeSimpleGraphAPIDecorator('query', parameterTypes, queryFields=queryFields, timeout=timeout)


def SimpleGraphMutationDecorator(parameterTypes, queryFields='', timeout=5.0):
    return _MakeSimpleGraphAPIDecorator('mutation', parameterTypes, queryFields=queryFields, timeout=timeout)


class ControllerGraphClient(object):

    _webclient = None # an instance of ControllerWebClient

    def __init__(self, webclient):
        self._webclient = webclient

    def _ExecuteGraphAPI(self, operationName, query, variables, timeout=5.0):
        response = self._webclient.Request('POST', '/api/v2/graphql', headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }, data=json.dumps({
            'operationName': operationName,
            'query': query,
            'variables': variables,
        }), timeout=timeout)

        # try to parse response
        raw = response.content.decode('utf-8', 'replace').strip()

        # repsonse must be 200 OK
        statusCode = response.status_code
        if statusCode != 200:
            raise ControllerGraphClientException(_('Unexpected server response %d: %s') % (statusCode, raw), statusCode=statusCode)

        # decode the response content
        content = None
        if len(raw) > 0:
            try:
                content = json.loads(raw)
            except ValueError as e:
                log.exception('caught exception parsing json response: %s: %s', e, raw)

        # raise any error returned
        if content is not None and 'errors' in content and len(content['errors']) > 0:
            message = content['errors'][0].get('message', raw)
            raise ControllerGraphClientException(message, statusCode=statusCode, content=content)

        if content is None or 'data' not in content:
            raise ControllerGraphClientException(_('Unexpected server response %d: %s') % (statusCode, raw), statusCode=statusCode)

        return content['data']

    @SimpleGraphQueryDecorator({
        'environmentId': 'String!',
        'bodyName': 'String!',
        'attachedSensorName': 'String!',
    }, timeout=5.0)
    def IsAttachedSensorMoveable(self):
        pass
