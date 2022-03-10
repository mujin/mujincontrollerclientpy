# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)


def _StringifyQueryFields(queryFields, fields=None):
    selectedFields = []
    for fieldName, subQueryFields in queryFields.items():
        if isinstance(fields, (list, set, dict)) and fieldName not in fields:
            continue
        if subQueryFields:
            subFields = None
            if isinstance(fields, dict):
                subFields = fields.get(fieldName)
            selectedFields.append('%s %s' % (fieldName, _StringifyQueryFields(subQueryFields, subFields)))
        else:
            selectedFields.append(fieldName)
    return '{%s}' % ', '.join(selectedFields)


class ControllerGraphClientBase(object):

    _webclient = None # an instance of ControllerWebClient

    def __init__(self, webclient):
        self._webclient = webclient

    def _CallSimpleGraphAPI(self, queryOrMutation, operationName, parameterNameTypeValues, queryFields=None, fields=None, timeout=None):
        """
        :param queryOrMutation: either "query" or "mutation"
        :param operationName: name of the operation
        :param parameterNameTypeValues: list of tuple (parameterName, parameterType, parameterValue)
        :param queryFields: dict mapping fieldName to subFields, used to construct query fields
        :param fields: list of fieldName to filter for
        :param timeout: timeout in seconds
        """
        if timeout is None:
            timeout = 5.0

        queryParameters = ', '.join([
            '$%s: %s' % (parameterName, parameterType)
            for parameterName, parameterType, parameterValue in parameterNameTypeValues
        ])
        if queryParameters:
            queryParameters = '(%s)' % queryParameters
        queryArguments = ', '.join([
            '%s: $%s' % (parameterName, parameterName)
            for parameterName, parameterType, parameterValue in parameterNameTypeValues
        ])
        if queryArguments:
            queryArguments = '(%s)' % queryArguments
        query = '%(queryOrMutation)s %(operationName)s%(queryParameters)s {\n    %(operationName)s%(queryArguments)s%(queryFields)s\n}' % {
            'queryOrMutation': queryOrMutation,
            'operationName': operationName,
            'queryParameters': queryParameters,
            'queryArguments': queryArguments,
            'queryFields': ' %s' % _StringifyQueryFields(queryFields, fields) if queryFields else ''
        }
        variables = {}
        for parameterName, parameterType, parameterValue in parameterNameTypeValues:
            variables[parameterName] = parameterValue
        if log.isEnabledFor(5): # logging.VERBOSE might not be available in the system
            log.verbose('executing graph query with variables %r:\n\n%s\n', variables, query)
        data = self._webclient.CallGraphAPI(query, variables, timeout=timeout)
        if log.isEnabledFor(5): # logging.VERBOSE might not be available in the system
            log.verbose('got response from graph query: %r', data)
        return data.get(operationName)
