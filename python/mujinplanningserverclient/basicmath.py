# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)

import math
import numpy as np

# Taken from mujincommon.basicmath

def ConvertMatrixFromQuat(quat):
    """Returns a 4x4 homogenous matrix

    Args:
        quat (np.array): WXYZ-formatted quaternion
    """
    length2 = quat[0]**2 + quat[1]**2 + quat[2]**2 + quat[3]**2
    ilength2 = 2.0 / length2
    qq1 = ilength2 * quat[1] * quat[1]
    qq2 = ilength2 * quat[2] * quat[2]
    qq3 = ilength2 * quat[3] * quat[3]
    if hasattr(quat, 'dtype'): # if quat is a numpy element, then use its dtype
        T = np.eye(4, dtype=quat.dtype)
    else:
        T = np.eye(4)
    T[0, 0] = 1 - qq2 - qq3
    T[0, 1] = ilength2 * (quat[1] * quat[2] - quat[0] * quat[3])
    T[0, 2] = ilength2 * (quat[1] * quat[3] + quat[0] * quat[2])
    T[1, 0] = ilength2 * (quat[1] * quat[2] + quat[0] * quat[3])
    T[1, 1] = 1 - qq1 - qq3
    T[1, 2] = ilength2 * (quat[2] * quat[3] - quat[0] * quat[1])
    T[2, 0] = ilength2 * (quat[1] * quat[3] - quat[0] * quat[2])
    T[2, 1] = ilength2 * (quat[2] * quat[3] + quat[0] * quat[1])
    T[2, 2] = 1 - qq1 - qq2
    return T

def quatFromMatrix(T):
    """Converts the rotation of a matrix into a quaternion.

    Args:
        T (np.array): 3x3, 3x4, 4x4 transform
    """
    tr = T[0, 0] + T[1, 1] + T[2, 2]
    rot = np.array([0.0, 0.0, 0.0, 0.0])
    if tr >= 0:
        rot[0] = tr + 1
        rot[1] = (T[2, 1] - T[1, 2])
        rot[2] = (T[0, 2] - T[2, 0])
        rot[3] = (T[1, 0] - T[0, 1])
    else:
        # find the largest diagonal element and jump to the appropriate case
        if T[1, 1] > T[0, 0]:
            if T[2, 2] > T[1, 1]:
                rot[3] = (T[2, 2] - (T[0, 0] + T[1, 1])) + 1
                rot[1] = (T[2, 0] + T[0, 2])
                rot[2] = (T[1, 2] + T[2, 1])
                rot[0] = (T[1, 0] - T[0, 1])
            else:
                rot[2] = (T[1, 1] - (T[2, 2] + T[0, 0])) + 1
                rot[3] = (T[1, 2] + T[2, 1])
                rot[1] = (T[0, 1] + T[1, 0])
                rot[0] = (T[0, 2] - T[2, 0])
        elif T[2, 2] > T[0, 0]:
            rot[3] = (T[2, 2] - (T[0, 0] + T[1, 1])) + 1
            rot[1] = (T[2, 0] + T[0, 2])
            rot[2] = (T[1, 2] + T[2, 1])
            rot[0] = (T[1, 0] - T[0, 1])
        else:
            rot[1] = (T[0, 0] - (T[1, 1] + T[2, 2])) + 1
            rot[2] = (T[0, 1] + T[1, 0])
            rot[3] = (T[2, 0] + T[0, 2])
            rot[0] = (T[2, 1] - T[1, 2])
    return rot / np.sqrt(rot[0]**2 + rot[1]**2 + rot[2]**2 + rot[3]**2)

def zyxFromMatrix(T, epsilon=1e-10):
    """T -> Z*Y*X

    .. code-block:: python

      from sympy import *
      x,y,z = Symbol('x'), Symbol('y'), Symbol('z')
      Rx = Matrix(3,3,[1,0,0,0,cos(x),-sin(x),0,sin(x),cos(x)])
      Ry = Matrix(3,3,[cos(y),0,sin(y),0,1,0,-sin(y),0,cos(y)])
      Rz = Matrix(3,3,[cos(z),-sin(z),0,sin(z),cos(z),0,0,0,1])
      Rz*Ry*Rx

    [cos(y)*cos(z), -cos(x)*sin(z) + cos(z)*sin(x)*sin(y),  sin(x)*sin(z) + cos(x)*cos(z)*sin(y)]
    [cos(y)*sin(z),  cos(x)*cos(z) + sin(x)*sin(y)*sin(z), -cos(z)*sin(x) + cos(x)*sin(y)*sin(z)]
    [      -sin(y),                         cos(y)*sin(x),                         cos(x)*cos(y)]


    Multiplied by sign(cos(x)), but because there's two solutions, force choosing here.

    """
    if abs(T[2][1]) < epsilon and abs(T[2][2]) < epsilon:
        y = np.pi / 2 if T[2, 0] <= 0 else -np.pi / 2
        if y > 0:
            xminusz = math.atan2(T[0, 1], T[1, 1])
            x = xminusz
            z = 0
        else:
            xplusz = -math.atan2(T[0, 1], T[1, 1])
            x = xplusz
            z = 0
    else:
        x = math.atan2(T[2, 1], T[2, 2])
        sinx = math.sin(x)
        cosx = math.cos(x)
        Rzy20 = T[2, 0]
        Rzy22 = T[2, 1] * sinx + T[2, 2] * cosx
        Rzy01 = T[0, 1] * cosx - T[0, 2] * sinx
        Rzy11 = T[1, 1] * cosx - T[1, 2] * sinx

        y = math.atan2(-Rzy20, Rzy22)
        z = math.atan2(-Rzy01, Rzy11)

    return np.array([x, y, z], dtype=np.float64)

def ConvertQuatFromAxisAngle(axis, angle):
    """angle is in radians
    """
    axislength = np.sqrt(axis[0] * axis[0] + axis[1] * axis[1] + axis[2] * axis[2])
    if axislength == 0:
        return np.array([1.0, 0, 0, 0])
    sinangle = np.sin(angle * 0.5) / axislength
    return np.array([np.cos(angle * 0.5), axis[0] * sinangle, axis[1] * sinangle, axis[2] * sinangle])

def matrixFromAxisAngle(axis, angle):
    """angle is in radians
    """
    return ConvertMatrixFromQuat(ConvertQuatFromAxisAngle(axis, angle))

def matrixFromZYX(ZYX):
    """standard euler angle order
    """
    return np.dot(matrixFromAxisAngle([0, 0, 1], ZYX[2]), np.dot(matrixFromAxisAngle([0, 1, 0], ZYX[1]), matrixFromAxisAngle([1, 0, 0], ZYX[0])))

# ====