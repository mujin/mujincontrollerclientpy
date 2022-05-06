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
    response = webClient.Request('HEAD', '/')
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
    elif _typeName == 'Float':
        return 'float'
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

def isBasicType(t):
    if t in ['String', 'Float', 'Boolean', 'Int']:
        return True
    elif t in ['Any']:  # Exception for objectDescription parameter, which does not have a type
        return True
    else:
        return False

def _MakeConstructor(fields, indent='    '):
    """
    """
    s = indent + 'def __init__(self'
    for fieldName, _ in fields:
        s += ', ' + fieldName + '=None'
    s += '):'
    return s


def _PrintTypesAsClasses(typeDatabase):
    """Create Python classes inspired by systemmanager/models.py, based on the graphAPI types.
    """
    indent = '    '
    indent2 = indent*2
    indent3 = indent*3
    for typeName, typeDefinition in sorted(typeDatabase.items()):
        modelName = '' + typeName
        print('class ' + modelName + '(dict):')
        print('    """')
        if typeDefinition['description']:
            for line in typeDefinition['description'].split('\n'):
                print('    %s' % line)
        print('')

        s = '    '
        if 'Input' in modelName:
            s += 'This class is an input type, meant to be passed to a function of controllergraphclient.'
        if not 'Input' in modelName:
            s += "This class is a return type, returned by a function of controllergraphclient. Not all fields may be intended for editing."
            if modelName + 'Input' in typeDatabase:
                s += " Also see the 'Input' version of this class."

        s += '\n\n    This class exposes its fields as properties for convenience, so they can be accessed more easily and auto-completed in most editors.'
        if 'Input' in modelName:
            s += ' This class behaves like a regular Python dictionary, which means that methods which take an instance of this class as an input also accept a dictionary, and the input does not first need to be converted to this class.'
        print(s)
        print('    """')
        
        fields = sorted(typeDefinition['fields'].items())  # Sorted for repeatability

        # Constructor (declaration and docstring)
        print()
        print(_MakeConstructor(fields))
        print(indent2 + '"""')
        if typeDefinition['description']:
            for line in typeDefinition['description'].split('\n'):
                print(indent2 + '%s' % line)
        print('')
        # TODO(felixvd): Enforce the keyword-only behavior when Python 3 transition is finished (as in https://stackoverflow.com/questions/31939890/function-which-allows-only-name-arguments )
        print(indent2 + 'The argument order may change in future releases. Only instantiate this object with named arguments (do not use positional args).')
        print('')
        print(indent2 + 'Args:')
        for fieldName, fieldDefinition in fields:
            isOptionalString = ""  # ", optional"
            print(indent3 + '%s (%s%s): %s' % (fieldName, _FormatTypeForDocstring(fieldDefinition['baseTypeName']), isOptionalString, fieldDefinition['description']))
        print(indent2 + '"""')

        # Constructor (content)
        for fieldName, fieldDefinition in fields:
            # TODO(felixvd): Can this be made into one line with self['%s'] = %s if %s is not None , or does this perform worse?
            print(indent2 + "if %s is not None:" % fieldName)
            print(indent2 + "    self['%s'] = %s" % (fieldName, fieldName))
            if not isBasicType(fieldDefinition['baseTypeName']) and fieldDefinition['baseTypeName'] != 'DateTime': # It is one of our types, so we instantiate an empty one (this allows descending into the tree)
                print(indent2 + "else:")
                print(indent2 + "    self['%s'] = %s()" % (fieldName, fieldDefinition['baseTypeName']))

        print('')

        # Property/Setter pairs
        for fieldName, fieldDefinition in fields:
            print('    @property')
            print('    def %s(self):' % fieldName)
            if fieldDefinition.get('description', None):
                print('        """' + fieldDefinition['description'])
                print('        """')
            print("        return self.get('%s', None)" % fieldName)
            print('')
            print('    @%s.setter' % fieldName)
            print('    def %s(self, value):' % fieldName)
            print("        self['%s'] = value" % fieldName)
            print('')
        
        
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
    print('# ===== Types are defined below')
    print('')
    _PrintTypesAsClasses(typeDatabase)
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
