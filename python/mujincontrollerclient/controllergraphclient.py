# -*- coding: utf-8 -*-
# DO NOT EDIT: THIS FILE IS AUTO-GENERATED

from .controllergraphclientutils import ControllerGraphClientBase

class ControllerGraphQueries:

    def GetAttachedSensor(self, attachedSensorId, bodyId, environmentId, fields=None, timeout=None):
        """Get a particular attached sensor on a robot.

        Args:
            attachedSensorId (String!): ID of the existing attached sensor.
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            AttachedSensor: Attached sensor on a robot.
        """
        parameterNameTypeValues = [
            ('attachedSensorId', 'String!', attachedSensorId),
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}
        return self._CallSimpleGraphAPI('query', operationName='GetAttachedSensor', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetBody(self, bodyId, environmentId, fields=None, timeout=None):
        """Get a particular body in an environment.

        Args:
            bodyId (String!): ID of the existing body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Body: Body or a robot in an environment.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}
        return self._CallSimpleGraphAPI('query', operationName='GetBody', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetConnectedBody(self, bodyId, connectedBodyId, environmentId, fields=None, timeout=None):
        """Get a particular connected body on a robot.

        Args:
            bodyId (String!): ID of the body.
            connectedBodyId (String!): ID of the existing connected body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            ConnectedBody: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('connectedBodyId', 'String!', connectedBodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}
        return self._CallSimpleGraphAPI('query', operationName='GetConnectedBody', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetEnvironment(self, environmentId, fields=None, timeout=None):
        """Get a specific environment.

        Args:
            environmentId (String!): ID of an existing environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Environment: Environment represents an OpenRAVE environment.
        """
        parameterNameTypeValues = [
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'attributes': {'aabbHalfExtents': None, 'barcodeScanningGain': None, 'barcodes': None, 'disabledReferenceObjectPKs': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'mass': None, 'materialType': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'referenceObjectPKs': None, 'transferSpeedMult': None, 'vendorName': None}, 'author': None, 'blobs': {'contentType': None, 'created': None, 'environmentId': None, 'id': None, 'modified': None, 'size': None}, 'bodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}, 'bodyCount': None, 'created': None, 'description': None, 'disabledReferenceEnvironmentIds': None, 'gravity': None, 'id': None, 'keywords': None, 'modified': None, 'name': None, 'referenceEnvironmentIds': None, 'referenceFilename': None, 'revision': None, 'stats': {'dateLastDetected': None, 'dateLastPicked': None}, 'unit': {'unitName': None, 'unitScale': None}}
        return self._CallSimpleGraphAPI('query', operationName='GetEnvironment', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetGeometry(self, bodyId, environmentId, geometryId, linkId, fields=None, timeout=None):
        """Get a particular geometry in a link.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            geometryId (String!): ID of the existing geometry.
            linkId (String!): ID of the link.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Geometry: Geometry belonging to a link.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('geometryId', 'String!', geometryId),
            ('linkId', 'String!', linkId),
        ]
        queryFields = {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}
        return self._CallSimpleGraphAPI('query', operationName='GetGeometry', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetGrabbed(self, bodyId, environmentId, grabbedId, fields=None, timeout=None):
        """Get a particular grabbed object in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            grabbedId (String!): ID of the existing grabbed object.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Grabbed: Grabbed object describes a grabbing relationship.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('grabbedId', 'String!', grabbedId),
        ]
        queryFields = {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}
        return self._CallSimpleGraphAPI('query', operationName='GetGrabbed', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetGraspSet(self, bodyId, environmentId, graspSetId, fields=None, timeout=None):
        """Get a particular grasp set in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            graspSetId (String!): ID of the existing grasp set.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            GraspSet: Grasp set describes a set of ikparams.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('graspSetId', 'String!', graspSetId),
        ]
        queryFields = {'deleted': None, 'id': None, 'ikParams': None, 'name': None}
        return self._CallSimpleGraphAPI('query', operationName='GetGraspSet', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetGripperInfo(self, bodyId, environmentId, gripperInfoId, fields=None, timeout=None):
        """Get a particular gripper info on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            gripperInfoId (String!): ID of the existing gripper info.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            GripperInfo: Gripper info describing the gripper properties, used for planning gripper operations.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('gripperInfoId', 'String!', gripperInfoId),
        ]
        queryFields = {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}
        return self._CallSimpleGraphAPI('query', operationName='GetGripperInfo', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetIKParameterization(self, bodyId, environmentId, ikParamId, fields=None, timeout=None):
        """Get a particular ikparam in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            ikParamId (String!): ID of the existing ikparam.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            IKParameterization: Inverse Kinematics Parameter describe a pose in space with additional parameters that can affect grasping.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('ikParamId', 'String!', ikParamId),
        ]
        queryFields = {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}
        return self._CallSimpleGraphAPI('query', operationName='GetIKParameterization', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetJoint(self, bodyId, environmentId, jointId, fields=None, timeout=None):
        """Get a particular joint in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            jointId (String!): ID of the existing joint.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Joint: Joint in a body describing the linkage between a parent link and a child link.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('jointId', 'String!', jointId),
        ]
        queryFields = {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}
        return self._CallSimpleGraphAPI('query', operationName='GetJoint', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetLink(self, bodyId, environmentId, linkId, fields=None, timeout=None):
        """Get a particular link in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            linkId (String!): ID of the existing link.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Link: Link of a body, containing geometries.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('linkId', 'String!', linkId),
        ]
        queryFields = {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}
        return self._CallSimpleGraphAPI('query', operationName='GetLink', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetRevision(self, environmentId, revisionId, fields=None, timeout=None):
        """Get a particular revision of an environment.

        Args:
            environmentId (String!): ID of the environment.
            revisionId (Int!): ID of the revision.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Revision: Revision of an environment, contains backward and forward differences.
        """
        parameterNameTypeValues = [
            ('environmentId', 'String!', environmentId),
            ('revisionId', 'Int!', revisionId),
        ]
        queryFields = {'author': None, 'backward': {'attributes': {'aabbHalfExtents': None, 'barcodeScanningGain': None, 'barcodes': None, 'disabledReferenceObjectPKs': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'mass': None, 'materialType': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'referenceObjectPKs': None, 'transferSpeedMult': None, 'vendorName': None}, 'author': None, 'blobs': {'contentType': None, 'created': None, 'environmentId': None, 'id': None, 'modified': None, 'size': None}, 'bodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}, 'bodyCount': None, 'created': None, 'description': None, 'disabledReferenceEnvironmentIds': None, 'gravity': None, 'id': None, 'keywords': None, 'modified': None, 'name': None, 'referenceEnvironmentIds': None, 'referenceFilename': None, 'revision': None, 'stats': {'dateLastDetected': None, 'dateLastPicked': None}, 'unit': {'unitName': None, 'unitScale': None}}, 'created': None, 'forward': {'attributes': {'aabbHalfExtents': None, 'barcodeScanningGain': None, 'barcodes': None, 'disabledReferenceObjectPKs': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'mass': None, 'materialType': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'referenceObjectPKs': None, 'transferSpeedMult': None, 'vendorName': None}, 'author': None, 'blobs': {'contentType': None, 'created': None, 'environmentId': None, 'id': None, 'modified': None, 'size': None}, 'bodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}, 'bodyCount': None, 'created': None, 'description': None, 'disabledReferenceEnvironmentIds': None, 'gravity': None, 'id': None, 'keywords': None, 'modified': None, 'name': None, 'referenceEnvironmentIds': None, 'referenceFilename': None, 'revision': None, 'stats': {'dateLastDetected': None, 'dateLastPicked': None}, 'unit': {'unitName': None, 'unitScale': None}}, 'id': None, 'message': None, 'modified': None}
        return self._CallSimpleGraphAPI('query', operationName='GetRevision', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def GetTool(self, bodyId, environmentId, toolId, fields=None, timeout=None):
        """Get a particular tool on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            toolId (String!): ID of the existing tool.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Tool: Tool describes a manipulator coordinate system of a robot.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('toolId', 'String!', toolId),
        ]
        queryFields = {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}
        return self._CallSimpleGraphAPI('query', operationName='GetTool', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def IsAttachedSensorMoveable(self, attachedSensorName, bodyName, environmentId, fields=None, timeout=None):
        """Check and see if attached sensor is moveable on a robot

        Args:
            attachedSensorName (String!): Name of the attached sensor, could be in the format of "connectedBodyName_attachedSensorName"
            bodyName (String!): Name of the body to check
            environmentId (String!): ID of the environment to check
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Boolean!: The `Boolean` scalar type represents `true` or `false`.
        """
        parameterNameTypeValues = [
            ('attachedSensorName', 'String!', attachedSensorName),
            ('bodyName', 'String!', bodyName),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('query', operationName='IsAttachedSensorMoveable', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListAttachedSensors(self, bodyId, environmentId, fields=None, timeout=None):
        """List attached sensors defined on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [AttachedSensor]!: Attached sensor on a robot.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}
        return self._CallSimpleGraphAPI('query', operationName='ListAttachedSensors', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListBodies(self, environmentId, fields=None, timeout=None):
        """List bodies in an environment.

        Args:
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [Body]!: Body or a robot in an environment.
        """
        parameterNameTypeValues = [
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}
        return self._CallSimpleGraphAPI('query', operationName='ListBodies', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListConnectedBodies(self, bodyId, environmentId, fields=None, timeout=None):
        """List connected bodies defined on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [ConnectedBody]!: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}
        return self._CallSimpleGraphAPI('query', operationName='ListConnectedBodies', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListEnvironments(self, pagination=None, fields=None, timeout=None):
        """List all environments.

        Args:
            pagination (PaginationInput): Optional pagination parameters, used to filter returned results.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [Environment]!: Environment represents an OpenRAVE environment.
        """
        parameterNameTypeValues = [
            ('pagination', 'PaginationInput', pagination),
        ]
        queryFields = {'attributes': {'aabbHalfExtents': None, 'barcodeScanningGain': None, 'barcodes': None, 'disabledReferenceObjectPKs': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'mass': None, 'materialType': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'referenceObjectPKs': None, 'transferSpeedMult': None, 'vendorName': None}, 'author': None, 'blobs': {'contentType': None, 'created': None, 'environmentId': None, 'id': None, 'modified': None, 'size': None}, 'bodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}, 'bodyCount': None, 'created': None, 'description': None, 'disabledReferenceEnvironmentIds': None, 'gravity': None, 'id': None, 'keywords': None, 'modified': None, 'name': None, 'referenceEnvironmentIds': None, 'referenceFilename': None, 'revision': None, 'stats': {'dateLastDetected': None, 'dateLastPicked': None}, 'unit': {'unitName': None, 'unitScale': None}}
        return self._CallSimpleGraphAPI('query', operationName='ListEnvironments', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListGeometries(self, bodyId, environmentId, linkId, fields=None, timeout=None):
        """List geometries in a link.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            linkId (String!): ID of the link.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [Geometry]!: Geometry belonging to a link.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('linkId', 'String!', linkId),
        ]
        queryFields = {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}
        return self._CallSimpleGraphAPI('query', operationName='ListGeometries', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListGrabbeds(self, bodyId, environmentId, fields=None, timeout=None):
        """List grabbed objects in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [Grabbed]!: Grabbed object describes a grabbing relationship.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}
        return self._CallSimpleGraphAPI('query', operationName='ListGrabbeds', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListGraspSets(self, bodyId, environmentId, fields=None, timeout=None):
        """List grasp sets in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [GraspSet]!: Grasp set describes a set of ikparams.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'deleted': None, 'id': None, 'ikParams': None, 'name': None}
        return self._CallSimpleGraphAPI('query', operationName='ListGraspSets', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListGripperInfos(self, bodyId, environmentId, fields=None, timeout=None):
        """List gripper infos defined on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [GripperInfo]!: Gripper info describing the gripper properties, used for planning gripper operations.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}
        return self._CallSimpleGraphAPI('query', operationName='ListGripperInfos', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListIKParameterizations(self, bodyId, environmentId, fields=None, timeout=None):
        """List ikparams in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [IKParameterization]!: Inverse Kinematics Parameter describe a pose in space with additional parameters that can affect grasping.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}
        return self._CallSimpleGraphAPI('query', operationName='ListIKParameterizations', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListJoints(self, bodyId, environmentId, fields=None, timeout=None):
        """List joints in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [Joint]!: Joint in a body describing the linkage between a parent link and a child link.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}
        return self._CallSimpleGraphAPI('query', operationName='ListJoints', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListLinks(self, bodyId, environmentId, fields=None, timeout=None):
        """List links in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [Link]!: Link of a body, containing geometries.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}
        return self._CallSimpleGraphAPI('query', operationName='ListLinks', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListRevisions(self, environmentId, pagination=None, fields=None, timeout=None):
        """List revisions of an environment.

        Args:
            environmentId (String!): ID of the environment.
            pagination (PaginationInput): Optional pagination parameters, used to filter returned results.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [Revision]!: Revision of an environment, contains backward and forward differences.
        """
        parameterNameTypeValues = [
            ('environmentId', 'String!', environmentId),
            ('pagination', 'PaginationInput', pagination),
        ]
        queryFields = {'author': None, 'backward': {'attributes': {'aabbHalfExtents': None, 'barcodeScanningGain': None, 'barcodes': None, 'disabledReferenceObjectPKs': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'mass': None, 'materialType': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'referenceObjectPKs': None, 'transferSpeedMult': None, 'vendorName': None}, 'author': None, 'blobs': {'contentType': None, 'created': None, 'environmentId': None, 'id': None, 'modified': None, 'size': None}, 'bodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}, 'bodyCount': None, 'created': None, 'description': None, 'disabledReferenceEnvironmentIds': None, 'gravity': None, 'id': None, 'keywords': None, 'modified': None, 'name': None, 'referenceEnvironmentIds': None, 'referenceFilename': None, 'revision': None, 'stats': {'dateLastDetected': None, 'dateLastPicked': None}, 'unit': {'unitName': None, 'unitScale': None}}, 'created': None, 'forward': {'attributes': {'aabbHalfExtents': None, 'barcodeScanningGain': None, 'barcodes': None, 'disabledReferenceObjectPKs': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'mass': None, 'materialType': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'referenceObjectPKs': None, 'transferSpeedMult': None, 'vendorName': None}, 'author': None, 'blobs': {'contentType': None, 'created': None, 'environmentId': None, 'id': None, 'modified': None, 'size': None}, 'bodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}, 'bodyCount': None, 'created': None, 'description': None, 'disabledReferenceEnvironmentIds': None, 'gravity': None, 'id': None, 'keywords': None, 'modified': None, 'name': None, 'referenceEnvironmentIds': None, 'referenceFilename': None, 'revision': None, 'stats': {'dateLastDetected': None, 'dateLastPicked': None}, 'unit': {'unitName': None, 'unitScale': None}}, 'id': None, 'message': None, 'modified': None}
        return self._CallSimpleGraphAPI('query', operationName='ListRevisions', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ListTools(self, bodyId, environmentId, fields=None, timeout=None):
        """List tools defined on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            [Tool]!: Tool describes a manipulator coordinate system of a robot.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}
        return self._CallSimpleGraphAPI('query', operationName='ListTools', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)


class ControllerGraphMutations:

    def CopyAttachedSensor(self, attachedSensorId, bodyId, environmentId, attachedSensor=None, fields=None, timeout=None):
        """Copy an existing attached sensor on a robot to a new one.

        Args:
            attachedSensorId (String!): ID of the existing attached sensor.
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            attachedSensor (AttachedSensorInput): Optionally, properties to change on the copied the attached sensor.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            AttachedSensor: Attached sensor on a robot.
        """
        parameterNameTypeValues = [
            ('attachedSensorId', 'String!', attachedSensorId),
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('attachedSensor', 'AttachedSensorInput', attachedSensor),
        ]
        queryFields = {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyAttachedSensor', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CopyBody(self, bodyId, environmentId, body=None, fields=None, timeout=None):
        """Copy an existing body in an environment to a new one.

        Args:
            bodyId (String!): ID of the existing body.
            environmentId (String!): ID of the environment.
            body (BodyInput): Optional properties to be applied on the copied body.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Body: Body or a robot in an environment.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('body', 'BodyInput', body),
        ]
        queryFields = {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyBody', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CopyConnectedBody(self, bodyId, connectedBodyId, environmentId, connectedBody=None, fields=None, timeout=None):
        """Copy an existing connected body on a robot to a new one.

        Args:
            bodyId (String!): ID of the body.
            connectedBodyId (String!): ID of the existing connected body.
            environmentId (String!): ID of the environment.
            connectedBody (ConnectedBodyInput): Optionally, properties to change on the copied the connected body.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            ConnectedBody: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('connectedBodyId', 'String!', connectedBodyId),
            ('environmentId', 'String!', environmentId),
            ('connectedBody', 'ConnectedBodyInput', connectedBody),
        ]
        queryFields = {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyConnectedBody', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CopyEnvironment(self, environmentId, environment=None, fields=None, timeout=None):
        """Copy an existing environment to a new one.

        Args:
            environmentId (String!): ID of the existing environment.
            environment (EnvironmentInput): Optionall properties to be applied on the copied environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Environment: Environment represents an OpenRAVE environment.
        """
        parameterNameTypeValues = [
            ('environmentId', 'String!', environmentId),
            ('environment', 'EnvironmentInput', environment),
        ]
        queryFields = {'attributes': {'aabbHalfExtents': None, 'barcodeScanningGain': None, 'barcodes': None, 'disabledReferenceObjectPKs': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'mass': None, 'materialType': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'referenceObjectPKs': None, 'transferSpeedMult': None, 'vendorName': None}, 'author': None, 'blobs': {'contentType': None, 'created': None, 'environmentId': None, 'id': None, 'modified': None, 'size': None}, 'bodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}, 'bodyCount': None, 'created': None, 'description': None, 'disabledReferenceEnvironmentIds': None, 'gravity': None, 'id': None, 'keywords': None, 'modified': None, 'name': None, 'referenceEnvironmentIds': None, 'referenceFilename': None, 'revision': None, 'stats': {'dateLastDetected': None, 'dateLastPicked': None}, 'unit': {'unitName': None, 'unitScale': None}}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyEnvironment', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CopyGeometry(self, bodyId, environmentId, geometryId, linkId, geometry=None, fields=None, timeout=None):
        """Copy an existing geometry in a link to a new one.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            geometryId (String!): ID of the existing geometry.
            linkId (String!): ID of the link.
            geometry (GeometryInput): Optional properties to be applied on the copied geometry.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Geometry: Geometry belonging to a link.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('geometryId', 'String!', geometryId),
            ('linkId', 'String!', linkId),
            ('geometry', 'GeometryInput', geometry),
        ]
        queryFields = {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyGeometry', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CopyGrabbed(self, bodyId, environmentId, grabbedId, grabbed=None, fields=None, timeout=None):
        """Copy an existing grabbed object in a body to a new one.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            grabbedId (String!): ID of the existing grabbed object.
            grabbed (GrabbedInput): Optional properties to be applied on the copied grabbed object.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Grabbed: Grabbed object describes a grabbing relationship.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('grabbedId', 'String!', grabbedId),
            ('grabbed', 'GrabbedInput', grabbed),
        ]
        queryFields = {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyGrabbed', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CopyGraspSet(self, bodyId, environmentId, graspSetId, graspSet=None, fields=None, timeout=None):
        """Copy an existing grasp set in a body to a new one.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            graspSetId (String!): ID of the existing grasp set.
            graspSet (GraspSetInput): Optional properties to be applied on the copied grasp set.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            GraspSet: Grasp set describes a set of ikparams.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('graspSetId', 'String!', graspSetId),
            ('graspSet', 'GraspSetInput', graspSet),
        ]
        queryFields = {'deleted': None, 'id': None, 'ikParams': None, 'name': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyGraspSet', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CopyGripperInfo(self, bodyId, environmentId, gripperInfoId, gripperInfo=None, fields=None, timeout=None):
        """Copy an existing gripper info on a robot to a new one.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            gripperInfoId (String!): ID of the existing gripper info.
            gripperInfo (GripperInfoInput): Optionally, properties to change on the copied the gripper info.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            GripperInfo: Gripper info describing the gripper properties, used for planning gripper operations.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('gripperInfoId', 'String!', gripperInfoId),
            ('gripperInfo', 'GripperInfoInput', gripperInfo),
        ]
        queryFields = {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyGripperInfo', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CopyIKParameterization(self, bodyId, environmentId, ikParamId, ikParam=None, fields=None, timeout=None):
        """Copy an existing ikparam in a body to a new one.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            ikParamId (String!): ID of the existing ikparam.
            ikParam (IKParameterizationInput): Optional properties to be applied on the copied ikparam.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            IKParameterization: Inverse Kinematics Parameter describe a pose in space with additional parameters that can affect grasping.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('ikParamId', 'String!', ikParamId),
            ('ikParam', 'IKParameterizationInput', ikParam),
        ]
        queryFields = {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyIKParameterization', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CopyJoint(self, bodyId, environmentId, jointId, joint=None, fields=None, timeout=None):
        """Copy an existing joint in a body to a new one.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            jointId (String!): ID of the existing joint.
            joint (JointInput): Optional properties to be applied on the copied joint.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Joint: Joint in a body describing the linkage between a parent link and a child link.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('jointId', 'String!', jointId),
            ('joint', 'JointInput', joint),
        ]
        queryFields = {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyJoint', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CopyLink(self, bodyId, environmentId, linkId, link=None, fields=None, timeout=None):
        """Copy an existing link in a body to a new one.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            linkId (String!): ID of the existing link.
            link (LinkInput): Optional properties to be applied on the copied link.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Link: Link of a body, containing geometries.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('linkId', 'String!', linkId),
            ('link', 'LinkInput', link),
        ]
        queryFields = {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyLink', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CopyTool(self, bodyId, environmentId, toolId, tool=None, fields=None, timeout=None):
        """Copy an existing tool on a robot to a new one.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            toolId (String!): ID of the existing tool.
            tool (ToolInput): Optionally, properties to change on the copied the tool.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Tool: Tool describes a manipulator coordinate system of a robot.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('toolId', 'String!', toolId),
            ('tool', 'ToolInput', tool),
        ]
        queryFields = {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CopyTool', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateAttachedSensor(self, bodyId, environmentId, attachedSensor=None, fields=None, timeout=None):
        """Create a new attached sensor on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            attachedSensor (AttachedSensorInput): Properties for the new attached sensor.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            AttachedSensor: Attached sensor on a robot.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('attachedSensor', 'AttachedSensorInput', attachedSensor),
        ]
        queryFields = {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateAttachedSensor', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateBody(self, environmentId, body=None, fields=None, timeout=None):
        """Create a new body in an environment.

        Args:
            environmentId (String!): ID of the environment.
            body (BodyInput): Properties to be applied on the newly created body.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Body: Body or a robot in an environment.
        """
        parameterNameTypeValues = [
            ('environmentId', 'String!', environmentId),
            ('body', 'BodyInput', body),
        ]
        queryFields = {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateBody', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateConnectedBody(self, bodyId, environmentId, connectedBody=None, fields=None, timeout=None):
        """Create a new connected body on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            connectedBody (ConnectedBodyInput): Properties for the new connected body.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            ConnectedBody: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('connectedBody', 'ConnectedBodyInput', connectedBody),
        ]
        queryFields = {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateConnectedBody', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateEnvironment(self, environment=None, fields=None, timeout=None):
        """Create a new environment.

        Args:
            environment (EnvironmentInput): Properties to be applied on the newly created environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Environment: Environment represents an OpenRAVE environment.
        """
        parameterNameTypeValues = [
            ('environment', 'EnvironmentInput', environment),
        ]
        queryFields = {'attributes': {'aabbHalfExtents': None, 'barcodeScanningGain': None, 'barcodes': None, 'disabledReferenceObjectPKs': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'mass': None, 'materialType': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'referenceObjectPKs': None, 'transferSpeedMult': None, 'vendorName': None}, 'author': None, 'blobs': {'contentType': None, 'created': None, 'environmentId': None, 'id': None, 'modified': None, 'size': None}, 'bodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}, 'bodyCount': None, 'created': None, 'description': None, 'disabledReferenceEnvironmentIds': None, 'gravity': None, 'id': None, 'keywords': None, 'modified': None, 'name': None, 'referenceEnvironmentIds': None, 'referenceFilename': None, 'revision': None, 'stats': {'dateLastDetected': None, 'dateLastPicked': None}, 'unit': {'unitName': None, 'unitScale': None}}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateEnvironment', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateGeometry(self, bodyId, environmentId, linkId, geometry=None, fields=None, timeout=None):
        """Create a new geometry in a link.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            linkId (String!): ID of the existing geometry.
            geometry (GeometryInput): Properties to be applied on the newly created geometry.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Geometry: Geometry belonging to a link.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('linkId', 'String!', linkId),
            ('geometry', 'GeometryInput', geometry),
        ]
        queryFields = {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateGeometry', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateGrabbed(self, bodyId, environmentId, grabbed=None, fields=None, timeout=None):
        """Create a new grabbed object in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            grabbed (GrabbedInput): Properties to be applied on the newly created grabbed object.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Grabbed: Grabbed object describes a grabbing relationship.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('grabbed', 'GrabbedInput', grabbed),
        ]
        queryFields = {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateGrabbed', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateGraspSet(self, bodyId, environmentId, graspSet=None, fields=None, timeout=None):
        """Create a new grasp set in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            graspSet (GraspSetInput): Properties to be applied on the newly created grasp set.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            GraspSet: Grasp set describes a set of ikparams.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('graspSet', 'GraspSetInput', graspSet),
        ]
        queryFields = {'deleted': None, 'id': None, 'ikParams': None, 'name': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateGraspSet', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateGripperInfo(self, bodyId, environmentId, gripperInfo=None, fields=None, timeout=None):
        """Create a new gripper info on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            gripperInfo (GripperInfoInput): Properties for the new gripper info.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            GripperInfo: Gripper info describing the gripper properties, used for planning gripper operations.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('gripperInfo', 'GripperInfoInput', gripperInfo),
        ]
        queryFields = {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateGripperInfo', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateIKParameterization(self, bodyId, environmentId, ikParam=None, fields=None, timeout=None):
        """Create a new ikparam in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            ikParam (IKParameterizationInput): Properties to be applied on the newly created ikparam.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            IKParameterization: Inverse Kinematics Parameter describe a pose in space with additional parameters that can affect grasping.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('ikParam', 'IKParameterizationInput', ikParam),
        ]
        queryFields = {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateIKParameterization', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateJoint(self, bodyId, environmentId, joint=None, fields=None, timeout=None):
        """Create a new joint in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            joint (JointInput): Properties to be applied on the newly created joint.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Joint: Joint in a body describing the linkage between a parent link and a child link.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('joint', 'JointInput', joint),
        ]
        queryFields = {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateJoint', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateLink(self, bodyId, environmentId, link=None, fields=None, timeout=None):
        """Create a new link in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            link (LinkInput): Properties to be applied on the newly created link.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Link: Link of a body, containing geometries.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('link', 'LinkInput', link),
        ]
        queryFields = {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateLink', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def CreateTool(self, bodyId, environmentId, tool=None, fields=None, timeout=None):
        """Create a new tool on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            tool (ToolInput): Properties for the new tool.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Tool: Tool describes a manipulator coordinate system of a robot.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('tool', 'ToolInput', tool),
        ]
        queryFields = {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='CreateTool', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteAttachedSensor(self, attachedSensorId, bodyId, environmentId, fields=None, timeout=None):
        """Delete a attached sensor from a robot.

        Args:
            attachedSensorId (String!): ID of the attached sensor to delete.
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('attachedSensorId', 'String!', attachedSensorId),
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteAttachedSensor', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteBody(self, bodyId, environmentId, fields=None, timeout=None):
        """Delete a body in an environment.

        Args:
            bodyId (String!): ID of the body to delete.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteBody', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteConnectedBody(self, bodyId, connectedBodyId, environmentId, fields=None, timeout=None):
        """Delete a connected body from a robot.

        Args:
            bodyId (String!): ID of the body.
            connectedBodyId (String!): ID of the connected body to delete.
            environmentId (String!): ID of the environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('connectedBodyId', 'String!', connectedBodyId),
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteConnectedBody', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteEnvironment(self, environmentId, fields=None, timeout=None):
        """Delete an environment.

        Args:
            environmentId (String!): ID of the environment to delete.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('environmentId', 'String!', environmentId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteEnvironment', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteGeometry(self, bodyId, environmentId, geometryId, linkId, fields=None, timeout=None):
        """Delete a geometry in a link.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            geometryId (String!): ID of the geometry to delete.
            linkId (String!): ID of the link.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('geometryId', 'String!', geometryId),
            ('linkId', 'String!', linkId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteGeometry', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteGrabbed(self, bodyId, environmentId, grabbedId, fields=None, timeout=None):
        """Delete a grabbed object in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            grabbedId (String!): ID of the grabbed object to delete.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('grabbedId', 'String!', grabbedId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteGrabbed', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteGraspSet(self, bodyId, environmentId, graspSetId, fields=None, timeout=None):
        """Delete a grasp set in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            graspSetId (String!): ID of the grasp set to delete.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('graspSetId', 'String!', graspSetId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteGraspSet', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteGripperInfo(self, bodyId, environmentId, gripperInfoId, fields=None, timeout=None):
        """Delete a gripper info from a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            gripperInfoId (String!): ID of the gripper info to delete.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('gripperInfoId', 'String!', gripperInfoId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteGripperInfo', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteIKParameterization(self, bodyId, environmentId, ikParamId, fields=None, timeout=None):
        """Delete a ikparam in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            ikParamId (String!): ID of the ikparam to delete.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('ikParamId', 'String!', ikParamId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteIKParameterization', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteJoint(self, bodyId, environmentId, jointId, fields=None, timeout=None):
        """Delete a joint in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            jointId (String!): ID of the joint to delete.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('jointId', 'String!', jointId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteJoint', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteLink(self, bodyId, environmentId, linkId, fields=None, timeout=None):
        """Delete a link in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            linkId (String!): ID of the link to be deleted.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('linkId', 'String!', linkId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteLink', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def DeleteTool(self, bodyId, environmentId, toolId, fields=None, timeout=None):
        """Delete a tool from a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            toolId (String!): ID of the tool to delete.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Void: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('toolId', 'String!', toolId),
        ]
        queryFields = None
        return self._CallSimpleGraphAPI('mutation', operationName='DeleteTool', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyAttachedSensor(self, attachedSensorId, bodyId, environmentId, attachedSensor=None, fields=None, timeout=None):
        """Modify an existing attached sensor on a robot.

        Args:
            attachedSensorId (String!): ID of the attached sensor to modify.
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            attachedSensor (AttachedSensorInput): Proprties to modify on the attached sensor.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            AttachedSensor: Attached sensor on a robot.
        """
        parameterNameTypeValues = [
            ('attachedSensorId', 'String!', attachedSensorId),
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('attachedSensor', 'AttachedSensorInput', attachedSensor),
        ]
        queryFields = {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyAttachedSensor', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyBody(self, bodyId, environmentId, body=None, fields=None, timeout=None):
        """Modify an existing body in an environment.

        Args:
            bodyId (String!): ID of the body to modify.
            environmentId (String!): ID of the environment.
            body (BodyInput): Properties to be modified on the body.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Body: Body or a robot in an environment.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('body', 'BodyInput', body),
        ]
        queryFields = {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyBody', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyConnectedBody(self, bodyId, connectedBodyId, environmentId, connectedBody=None, fields=None, timeout=None):
        """Modify an existing connected body on a robot.

        Args:
            bodyId (String!): ID of the body.
            connectedBodyId (String!): ID of the connected body to modify.
            environmentId (String!): ID of the environment.
            connectedBody (ConnectedBodyInput): Proprties to modify on the connected body.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            ConnectedBody: 
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('connectedBodyId', 'String!', connectedBodyId),
            ('environmentId', 'String!', environmentId),
            ('connectedBody', 'ConnectedBodyInput', connectedBody),
        ]
        queryFields = {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyConnectedBody', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyEnvironment(self, environmentId, environment=None, fields=None, timeout=None):
        """Modify an existing environment.

        Args:
            environmentId (String!): ID of the environment to modify.
            environment (EnvironmentInput): Properties to be modified on the existing environment.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Environment: Environment represents an OpenRAVE environment.
        """
        parameterNameTypeValues = [
            ('environmentId', 'String!', environmentId),
            ('environment', 'EnvironmentInput', environment),
        ]
        queryFields = {'attributes': {'aabbHalfExtents': None, 'barcodeScanningGain': None, 'barcodes': None, 'disabledReferenceObjectPKs': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'mass': None, 'materialType': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'referenceObjectPKs': None, 'transferSpeedMult': None, 'vendorName': None}, 'author': None, 'blobs': {'contentType': None, 'created': None, 'environmentId': None, 'id': None, 'modified': None, 'size': None}, 'bodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'connectedBodies': {'attachedSensors': {'deleted': None, 'id': None, 'linkName': None, 'name': None, 'referenceAttachedSensorName': None, 'sensorGeometry': {'gain': None, 'hardwareId': None, 'height': None, 'intrinsics': {'cx': None, 'cy': None, 'distortionCoeffs': None, 'distortionModel': None, 'focalLength': None, 'fx': None, 'fy': None}, 'measurementTime': None, 'sensorReference': None, 'targetRegion': None, 'width': None}, 'sensorMaker': None, 'sensorModel': None, 'transform': None, 'type': None}, 'deleted': None, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'isActive': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'linkName': None, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'name': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None, 'uri': None}, 'created': None, 'deleted': None, 'dofValues': {'jointAxis': None, 'jointName': None, 'value': None}, 'grabbed': {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}, 'gripperInfos': {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}, 'id': None, 'interfaceType': None, 'isRobot': None, 'joints': {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}, 'links': {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}, 'modified': None, 'name': None, 'readableInterfaces': {'bodyparameters': {'allowedPlacementOrientations': None, 'barcodeScanningGain': None, 'barcodes': None, 'bottomBoxDistSensorThresh': None, 'disabledReferenceObjectPKs': None, 'distSensorMismatchReplanThresh': None, 'graspModelInfo': {'minNumSupportedFaces': None}, 'graspSets': {'deleted': None, 'id': None, 'ikParams': None, 'name': None}, 'gripperSuctionCupsPerformances': {'gripperName': None, 'suctionCupsPerformances': {'score': None, 'suctionCupPartTypes': None}}, 'ikParams': {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}, 'knownBarCodeFaces': None, 'materialType': None, 'minSuctionForce': None, 'minViableRegionSize2D': None, 'modelName': None, 'objectCategory': None, 'objectDescription': None, 'objectPackingId': None, 'objectType': None, 'packingOrderPriority': None, 'positionConfigurations': {'deleted': None, 'id': None, 'jointConfigurationStates': {'connectedBodyName': None, 'jointName': None, 'jointValue': None}, 'name': None}, 'referenceObjectPKs': None, 'regions': {'extents': None, 'name': None, 'transform': None}, 'totalNumBarCodes': None, 'transferSpeedMult': None, 'vendorName': None}, 'extendable': None, 'robotmotionparameters': {'controllerDOFMults': None, 'controllerDOFOrder': None, 'controllerTimestep': None, 'dynamicsConstraintsType': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'ikTypeName': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'maxToolAccelRotation': None, 'maxToolAccelTranslation': None, 'maxToolSpeedRotation': None, 'maxToolSpeedTranslation': None, 'robotController': None, 'robotLanguage': None, 'robotMaker': None, 'robotSimulationFile': None, 'robotType': None, 'safetySpeedConstraintsInfo': {'speedLimitForToolNames': {'maxToolSpeed': None, 'toolname': None}, 'use': None}, 'stringParameters': {'deleted': None, 'id': None, 'values': None}}}, 'referenceUri': None, 'referenceUriHint': None, 'tools': {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}, 'transform': None}, 'bodyCount': None, 'created': None, 'description': None, 'disabledReferenceEnvironmentIds': None, 'gravity': None, 'id': None, 'keywords': None, 'modified': None, 'name': None, 'referenceEnvironmentIds': None, 'referenceFilename': None, 'revision': None, 'stats': {'dateLastDetected': None, 'dateLastPicked': None}, 'unit': {'unitName': None, 'unitScale': None}}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyEnvironment', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyGeometry(self, bodyId, environmentId, geometryId, linkId, geometry=None, fields=None, timeout=None):
        """Modify an existing geometry in a link.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            geometryId (String!): ID of the geometry to modify.
            linkId (String!): ID of the link.
            geometry (GeometryInput): Properties to be modified on the geometry.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Geometry: Geometry belonging to a link.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('geometryId', 'String!', geometryId),
            ('linkId', 'String!', linkId),
            ('geometry', 'GeometryInput', geometry),
        ]
        queryFields = {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyGeometry', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyGrabbed(self, bodyId, environmentId, grabbedId, grabbed=None, fields=None, timeout=None):
        """Modify an existing grabbed object in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            grabbedId (String!): ID of the grabbed object to modify.
            grabbed (GrabbedInput): Properties to be modified on the grabbed object.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Grabbed: Grabbed object describes a grabbing relationship.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('grabbedId', 'String!', grabbedId),
            ('grabbed', 'GrabbedInput', grabbed),
        ]
        queryFields = {'deleted': None, 'grabbedName': None, 'id': None, 'ignoreRobotLinkNames': None, 'robotLinkName': None, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyGrabbed', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyGraspSet(self, bodyId, environmentId, graspSetId, graspSet=None, fields=None, timeout=None):
        """Modify an existing grasp set in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            graspSetId (String!): ID of the grasp set to modify.
            graspSet (GraspSetInput): Properties to be modified on the grasp set.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            GraspSet: Grasp set describes a set of ikparams.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('graspSetId', 'String!', graspSetId),
            ('graspSet', 'GraspSetInput', graspSet),
        ]
        queryFields = {'deleted': None, 'id': None, 'ikParams': None, 'name': None}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyGraspSet', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyGripperInfo(self, bodyId, environmentId, gripperInfoId, gripperInfo=None, fields=None, timeout=None):
        """Modify an existing gripper info on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            gripperInfoId (String!): ID of the gripper info to modify.
            gripperInfo (GripperInfoInput): Proprties to modify on the gripper info.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            GripperInfo: Gripper info describing the gripper properties, used for planning gripper operations.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('gripperInfoId', 'String!', gripperInfoId),
            ('gripperInfo', 'GripperInfoInput', gripperInfo),
        ]
        queryFields = {'deleted': None, 'extendable': None, 'gripperJointNames': None, 'grippertype': None, 'id': None, 'name': None}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyGripperInfo', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyIKParameterization(self, bodyId, environmentId, ikParamId, ikParam=None, fields=None, timeout=None):
        """Modify an existing ikparam in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            ikParamId (String!): ID of the ikparam to modify.
            ikParam (IKParameterizationInput): Properties to be modified on the ikparam.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            IKParameterization: Inverse Kinematics Parameter describe a pose in space with additional parameters that can affect grasping.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('ikParamId', 'String!', ikParamId),
            ('ikParam', 'IKParameterizationInput', ikParam),
        ]
        queryFields = {'angle': None, 'customData': {'deleted': None, 'id': None, 'values': None}, 'deleted': None, 'direction': None, 'id': None, 'localTranslate': None, 'name': None, 'quaternion': None, 'transform': None, 'translate': None, 'type': None}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyIKParameterization', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyJoint(self, bodyId, environmentId, jointId, joint=None, fields=None, timeout=None):
        """Modify an existing joint in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            jointId (String!): ID of the joint to modify.
            joint (JointInput): Properties to be modified on the joint.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Joint: Joint in a body describing the linkage between a parent link and a child link.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('jointId', 'String!', jointId),
            ('joint', 'JointInput', joint),
        ]
        queryFields = {'anchors': None, 'axes': None, 'childLinkName': None, 'currentValues': None, 'deleted': None, 'electricMotorActuator': {'assignedPowerRating': None, 'coloumbFriction': None, 'gearRatio': None, 'maxInstantaneousTorque': None, 'maxSpeed': None, 'maxSpeedTorquePoints': None, 'modelType': None, 'noLoadSpeed': None, 'nominalSpeedTorquePoints': None, 'nominalTorque': None, 'nominalVoltage': None, 'rotorInertia': None, 'speedConstant': None, 'stallTorque': None, 'startingCurrent': None, 'terminalResistance': None, 'torqueConstant': None, 'viscousFriction': None}, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'hardMaxAccel': None, 'hardMaxJerk': None, 'hardMaxVel': None, 'id': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isActive': None, 'isCircular': None, 'lowerLimit': None, 'maxAccel': None, 'maxInertia': None, 'maxJerk': None, 'maxTorque': None, 'maxVel': None, 'mimics': {'equations': None}, 'name': None, 'offsets': None, 'parentLinkName': None, 'resolutions': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'type': None, 'upperLimit': None, 'weights': None}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyJoint', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyLink(self, bodyId, environmentId, linkId, link=None, fields=None, timeout=None):
        """Modify an existing link in a body.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            linkId (String!): ID of the link to modify.
            link (LinkInput): Properties to be modified on the link.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Link: Link of a body, containing geometries.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('linkId', 'String!', linkId),
            ('link', 'LinkInput', link),
        ]
        queryFields = {'deleted': None, 'floatParameters': {'deleted': None, 'id': None, 'values': None}, 'forcedAdjacentLinks': None, 'geometries': {'ambientColor': None, 'baseExtents': None, 'bottom': None, 'bottomCross': None, 'calibrationBoardParameters': {'bigDotDiameterDistanceRatio': None, 'dotColor': None, 'dotDiameterDistanceRatio': None, 'dotsDistanceX': None, 'dotsDistanceY': None, 'numDotsX': None, 'numDotsY': None, 'patternName': None}, 'deleted': None, 'diffuseColor': None, 'halfExtents': None, 'height': None, 'id': None, 'innerExtents': None, 'innerSizeX': None, 'innerSizeY': None, 'innerSizeZ': None, 'mesh': {'indices': None, 'vertices': None}, 'modifiable': None, 'name': None, 'outerExtents': None, 'radius': None, 'sideWalls': {'halfExtents': None, 'transform': None, 'type': None}, 'transform': None, 'transparency': None, 'type': None, 'visible': None}, 'id': None, 'inertiaMoments': None, 'intParameters': {'deleted': None, 'id': None, 'values': None}, 'isEnabled': None, 'isStatic': None, 'mass': None, 'massTransform': None, 'name': None, 'stringParameters': {'deleted': None, 'id': None, 'value': None}, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyLink', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)

    def ModifyTool(self, bodyId, environmentId, toolId, tool=None, fields=None, timeout=None):
        """Modify an existing tool on a robot.

        Args:
            bodyId (String!): ID of the body.
            environmentId (String!): ID of the environment.
            toolId (String!): ID of the tool to modify.
            tool (ToolInput): Proprties to modify on the tool.
            fields (list or dict): Optionally specify a subset of fields to return.
            timeout (float): Number of seconds to wait for response.

        Returns:
            Tool: Tool describes a manipulator coordinate system of a robot.
        """
        parameterNameTypeValues = [
            ('bodyId', 'String!', bodyId),
            ('environmentId', 'String!', environmentId),
            ('toolId', 'String!', toolId),
            ('tool', 'ToolInput', tool),
        ]
        queryFields = {'baseLinkName': None, 'chuckingDirections': None, 'deleted': None, 'direction': None, 'effectorLinkName': None, 'gripperJointNames': None, 'grippername': None, 'id': None, 'ikChainEndLinkName': None, 'ikSolverType': None, 'name': None, 'restrictGraspSetNames': None, 'toolChangerConnectedBodyToolName': None, 'transform': None}
        return self._CallSimpleGraphAPI('mutation', operationName='ModifyTool', parameterNameTypeValues=parameterNameTypeValues, queryFields=queryFields, fields=fields, timeout=timeout)


class ControllerGraphClient(ControllerGraphClientBase, ControllerGraphQueries, ControllerGraphMutations):
    pass

