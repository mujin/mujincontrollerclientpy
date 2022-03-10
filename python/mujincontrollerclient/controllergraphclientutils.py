# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)


def _StringifyQueryFields(queryFields, fields=None):
    selectedFields = []
    for fieldName, subQueryFields in queryFields.items():
        if fields and fieldName not in fields:
            continue
        if subQueryFields:
            selectedFields.append('%s %s' % (fieldName, _StringifyQueryFields(subQueryFields)))
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
        query = '%s %s%s\n' % (queryOrMutation, operationName, queryParameters)
        query += '{'
        queryArguments = ', '.join([
            '%s: $%s' % (parameterName, parameterName)
            for parameterName, parameterType, parameterValue in parameterNameTypeValues
        ])
        if queryArguments:
            queryArguments = '(%s)' % queryArguments
        query += '    %s%s %s\n' % (operationName, queryArguments, _StringifyQueryFields(queryFields, fields) if queryFields else '')
        query += '}'
        variables = {}
        for parameterName, parameterType, parameterValue in parameterNameTypeValues:
            variables[parameterName] = parameterValue
        data = self._webclient.CallGraphAPI(query, variables, timeout=timeout)
        return data.get(operationName)
