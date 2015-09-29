from mujincontrollerclient import itlplanning2client
from mujinplanningcommon.planningutil import itlprogram
from openravepy import *

controllerurl = 'http://127.0.0.1'
controllerusername = 'testuser'
controllerpassword = 'pass'
pathtimingzmqport = 11000
pathtimingheartbeatport = None
pathtimingheartbeattimeout = 7
scenepk = 'komatsu_ntc.mujin.dae'
robotname = 'komatsu_ntc_TLM-610'
usewebapi = False
initializezmq = True
robotControllerUri = None #'tcp://192.168.13.83:7000'

self = itlplanning2client.ITLPlanning2ControllerClient(controllerurl, controllerusername, controllerpassword, robotControllerUri, scenepk, robotname, pathtimingzmqport, pathtimingheartbeatport, pathtimingheartbeattimeout, usewebapi, initializezmq)


env = Environment()

program = itlprogram.Program('11TEST')
program.LoadData(env, '/data/programs/gcode1')
programtxt =  open(program.GetFullFilename('/data/programs/gcode1'), 'r+').read()


def test_GCodeToITLConverter():
    pass

