#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graphql # require graphql-core pip package when generating python code

import logging
log = logging.getLogger(__name__)


def _ConfigureLogging(level=None):
    try:
        import mujincommon
        mujincommon.ConfigureRootLogger(level=level)
    except ImportError:
        logging.basicConfig(format='%(levelname)s %(name)s: %(funcName)s, %(message)s', level=logging.DEBUG)


def _ParseArguments():
    import argparse
    parser = argparse.ArgumentParser(description='Open a shell to use controllerclient')
    parser.add_argument('--loglevel', type=str, default=None, help='The python log level, e.g. DEBUG, VERBOSE, ERROR, INFO, WARNING, CRITICAL (default: %(default)s)')
    parser.add_argument('--url', type=str, default='http://localhost', help='URL of the controller (default: %(default)s)')
    parser.add_argument('--username', type=str, default='mujin', help='Username to login with (default: %(default)s)')
    parser.add_argument('--password', type=str, default='mujin', help='Password to login with (default: %(default)s)')
    return parser.parse_args()


def _FetchSchema(url, username, password):
    from mujincontrollerclient.controllerclientraw import ControllerWebClient
    webClient = ControllerWebClient(url, username, password)
    return graphql.build_client_schema(webClient.CallGraphAPI(graphql.get_introspection_query(descriptions=True), {}))

def _DereferenceType(fieldType):
    while hasattr(fieldType, 'of_type'):
        fieldType = fieldType.of_type
    return fieldType

def _DiscoverQueryFields(fieldType):
    fieldType = _DereferenceType(fieldType)
    if not hasattr(fieldType, 'fields'):
        return None
    queryFields = {}
    for fieldName, field in fieldType.fields.items():
        queryFields[fieldName] = _DiscoverQueryFields(field.type)
    return queryFields

def _DiscoverMethods(queryOrMutationType):
    methods = []
    for operationName, field in queryOrMutationType.fields.items():
        methods.append({
            'operationName': operationName,
            'parameters': sorted([
                {
                    'parameterName': argumentName,
                    'parameterType': argument.type,
                    'parameterDescription': argument.description,
                    'parameterNullable': not isinstance(argument.type, graphql.GraphQLNonNull),
                }
                for argumentName, argument in field.args.items()
            ], key=lambda x: (x['parameterNullable'], x['parameterName'])),
            'description': field.description,
            'returnType': field.type,
            'queryFields': _DiscoverQueryFields(field.type),
        })
    return methods    

def _PrintMethod(queryOrMutation, operationName, parameters, description, returnType, queryFields):
    print('    def %s(self, %s):' % (operationName, ', '.join([
        '%s=None' % parameter['parameterName'] if parameter['parameterNullable'] else parameter['parameterName']
        for parameter in parameters
    ] + ['fields=None', 'timeout=None'])))
    if description:
        print('        """%s' % description)
        print('')
        print('        Args:')
        for parameter in parameters:
            print('            %s (%s): %s' % (parameter['parameterName'], parameter['parameterType'], parameter['parameterDescription']))
        print('            fields (list or dict): Optionally specify a subset of fields to return.')
        print('            timeout (float): Number of seconds to wait for response.')
        print('')
        print('        Returns:')
        print('            %s: %s' % (returnType, _DereferenceType(returnType).description))
        print('        """')
    print('        parameterNameTypeValues = [')
    for parameter in parameters:
        print('            (\'%s\', \'%s\', %s),' % (parameter['parameterName'], parameter['parameterType'], parameter['parameterName']))
    print('        ]')
    print('        queryFields = %r' % queryFields)
    print('        return self._CallSimpleGraphAPI(\'%s\', operationName=\'%s\', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)' % (queryOrMutation, operationName))

def _PrintClient(queryMethods, mutationMethods):
    print('# -*- coding: utf-8 -*-')
    print('# DO NOT EDIT: THIS FILE IS AUTO-GENERATED')
    print('')
    print('from .controllergraphclientutils import ControllerGraphClientBase')
    print('')
    print('class ControllerGraphQueries:')
    print('')
    for queryMethod in queryMethods:
        _PrintMethod('query', **queryMethod)
        print('')
    print('')
    print('class ControllerGraphMutations:')
    print('')
    for mutationMethod in mutationMethods:
        _PrintMethod('mutation', **mutationMethod)
        print('')
    print('')
    print('class ControllerGraphClient(ControllerGraphClientBase, ControllerGraphQueries, ControllerGraphMutations):')
    print('    pass')
    print('')


def _Main():
    options = _ParseArguments()
    _ConfigureLogging(options.loglevel)

    schema = _FetchSchema(options.url, options.username, options.password)
    queryMethods = _DiscoverMethods(schema.query_type)
    mutationMethods = _DiscoverMethods(schema.mutation_type)
    _PrintClient(queryMethods, mutationMethods)


if __name__ == "__main__":
    _Main()
