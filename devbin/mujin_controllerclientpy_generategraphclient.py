#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
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


def _FetchServerVersionAndSchema(url, username, password):
    from mujincontrollerclient.controllerclientraw import ControllerWebClient
    webClient = ControllerWebClient(url, username, password)
    response = webClient.Request('HEAD', '/api/v2')
    assert response.status_code == 200, 'Unable to fetch server version: %s' % response
    serverVersion = response.headers['Server'].split()[0]
    log.info('server version determined to be: %s', serverVersion)
    schema = graphql.build_client_schema(webClient.CallGraphAPI(graphql.get_introspection_query(descriptions=True), {}))
    return serverVersion, schema

def _DereferenceType(graphType):
    while hasattr(graphType, 'of_type'):
        graphType = graphType.of_type
    return graphType

def _IndentNewlines(string, indent="    "*5):
    """Indent new lines in a string. Used for multi-line descriptions.
    """
    return string.replace("\n", "\n"+indent)

def _FormatTypeForDocstring(typeName):
    """Removes the exclamation mark and converts basic Golang types to Python types.
    """
    _typeName = str(typeName).replace("!", "")
    if _typeName == 'String':
        return 'str'
    elif _typeName == 'Int':
        return 'int'
    elif _typeName == 'Boolean':
        return 'bool'
    else:
        return _typeName

def _DiscoverType(graphType, typeDatabase):
    baseFieldType = _DereferenceType(graphType)
    baseFieldTypeName = '%s' % baseFieldType
    baseDescription = ''
    if hasattr(baseFieldType, 'fields'):
        baseDescription = baseFieldType.description.strip()
        if baseFieldTypeName not in typeDatabase:
            baseFields = {}
            for fieldName, field in baseFieldType.fields.items():
                baseFields[fieldName] = _DiscoverType(field.type, typeDatabase)
                if field.description:
                    baseFields[fieldName]['description'] = field.description.strip()
            typeDatabase[baseFieldTypeName] = {
                'description': baseDescription,
                'fields': baseFields,
            }
    return {
        'typeName': '%s' % graphType,
        'baseTypeName': '%s' % baseFieldType,
        'description': baseDescription,
    }

def _DiscoverMethods(queryOrMutationType, typeDatabase):
    methods = []
    for operationName, field in queryOrMutationType.fields.items():
        methods.append({
            'operationName': operationName,
            'parameters': sorted([
                {
                    'parameterName': argumentName,
                    'parameterType': _DiscoverType(argument.type, typeDatabase)['typeName'],
                    'parameterDescription': argument.description,
                    'parameterNullable': not isinstance(argument.type, graphql.GraphQLNonNull),
                }
                for argumentName, argument in field.args.items()
            ], key=lambda x: (x['parameterNullable'], x['parameterName'])),
            'description': field.description,
            'returnType': _DiscoverType(field.type, typeDatabase),
        })
    return methods    

def _PrintMethod(queryOrMutation, operationName, parameters, description, returnType):
    print('    def %s(self, %s):' % (operationName, ', '.join([
        '%s=None' % parameter['parameterName'] if parameter['parameterNullable'] else parameter['parameterName']
        for parameter in parameters
    ] + ['fields=None', 'timeout=None'])))
    if description:
        print('        """%s' % description)
        print('')
        print('        Args:')
        for parameter in parameters:
            isOptionalString = ", optional" if parameter['parameterNullable'] else ""
            print('            %s (%s%s): %s' % (parameter['parameterName'], _FormatTypeForDocstring(parameter['parameterType']), isOptionalString, _IndentNewlines(parameter['parameterDescription'])))
        print('            fields (list or dict, optional): Specifies a subset of fields to return.')
        print('            timeout (float, optional): Number of seconds to wait for response.')
        print('')
        print('        Returns:')
        print('            %s: %s' % (_FormatTypeForDocstring(returnType['typeName']), _IndentNewlines(returnType['description'])))
        print('        """')
    print('        parameterNameTypeValues = [')
    for parameter in parameters:
        print('            (\'%s\', \'%s\', %s),' % (parameter['parameterName'], parameter['parameterType'], parameter['parameterName']))
    print('        ]')
    print('        return self._CallSimpleGraphAPI(\'%s\', operationName=\'%s\', parameterNameTypeValues=parameterNameTypeValues, returnType=\'%s\', fields=fields, timeout=timeout)' % (queryOrMutation, operationName, returnType['baseTypeName']))

def _PrintTypeDatabase(typeDatabase):
    print('    typeDatabase = {')
    for typeName, typeDefinition in sorted(typeDatabase.items()):
        print('')
        if typeDefinition['description']:
            for line in typeDefinition['description'].split('\n'):
                print('        # %s' % line)
        print('        \'%s\': {' % typeName)
        for fieldName, fieldDefinition in sorted(typeDefinition['fields'].items()):
            if fieldDefinition['description']:
                for line in fieldDefinition['description'].split('\n'):
                    print('            # %s' % line)
            print('            \'%s\': \'%s\', # %s' % (fieldName, fieldDefinition['baseTypeName'], fieldDefinition['typeName']))
        print('        },')
    print('    }')

def _PrintClient(serverVersion, queryMethods, mutationMethods, typeDatabase):
    print('# -*- coding: utf-8 -*-')
    print('#')
    print('# DO NOT EDIT, THIS FILE WAS AUTO-GENERATED')
    print('# GENERATED BY: %s' % os.path.basename(__file__))
    print('# GENERATED AGAINST: %s' % serverVersion)
    print('#')
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
    print('')
    _PrintTypeDatabase(typeDatabase)
    print('')
    print('#')
    print('# DO NOT EDIT, THIS FILE WAS AUTO-GENERATED, SEE HEADER')
    print('#')
    print('')


def _Main():
    options = _ParseArguments()
    _ConfigureLogging(options.loglevel)

    serverVersion, schema = _FetchServerVersionAndSchema(options.url, options.username, options.password)
    typeDatabase = {}
    queryMethods = _DiscoverMethods(schema.query_type, typeDatabase)
    mutationMethods = _DiscoverMethods(schema.mutation_type, typeDatabase)

    _PrintClient(serverVersion, queryMethods, mutationMethods, typeDatabase)


if __name__ == "__main__":
    _Main()
