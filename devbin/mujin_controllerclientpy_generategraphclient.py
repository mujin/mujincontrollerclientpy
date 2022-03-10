#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graphql # require graphql-core pip package when generating python code

from mujincontrollerclient.controllerclientraw import ControllerWebClient

def _GetSchema():
    webClient = ControllerWebClient('http://controller488', 'mujin', 'mujin')
    return graphql.build_client_schema(webClient.CallGraphAPI(graphql.get_introspection_query(descriptions=True), {}))

schema = _GetSchema()

def _DiscoverQueryFields(fieldType):
    while hasattr(fieldType, 'of_type'):
        fieldType = fieldType.of_type
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
                    'parameterNullable': not isinstance(argument.type, graphql.GraphQLNonNull),
                }
                for argumentName, argument in field.args.items()
            ], key=lambda x: (x['parameterNullable'], x['parameterName'])),
            'description': field.description,
            'queryFields': _DiscoverQueryFields(field.type),
        })
    return methods

queryMethods = _DiscoverMethods(schema.query_type)
mutationMethods = _DiscoverMethods(schema.mutation_type)

def _PrintMethod(queryOrMutation, operationName, parameters, description, queryFields):
    print('    def %s(self, %s):' % (operationName, ', '.join([
        '%s=None' % parameter['parameterName'] if parameter['parameterNullable'] else parameter['parameterName']
        for parameter in parameters
    ] + ['fields=None', 'timeout=None'])))
    if description:
        print('        """%s"""' % description)
    print('        parameterNameTypeValues = [')
    for parameter in parameters:
        print('            (\'%s\', \'%s\', %s),' % (parameter['parameterName'], parameter['parameterType'], parameter['parameterName']))
    print('        ]')
    print('        queryFields = %r' % queryFields)
    print('        return self._CallSimpleGraphAPI(\'%s\', operationName=\'%s\', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)' % (queryOrMutation, operationName))
    print('')

print("""# -*- coding: utf-8 -*-
# DO NOT EDIT: THIS FILE IS AUTO-GENERATED

from .controllergraphclientutils import ControllerGraphClientBase
""")


print("""class ControllerGraphQueries:
""")
for queryMethod in queryMethods:
    _PrintMethod('query', **queryMethod)



print("""class ControllerGraphMutations:
""")
for mutationMethod in mutationMethods:
    _PrintMethod('mutation', **mutationMethod)


print("""
class ControllerGraphClient(ControllerGraphClientBase, ControllerGraphQueries, ControllerGraphMutations):
    pass

""")
