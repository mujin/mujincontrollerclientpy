from mujincontrollerclient import itlplanning2client
from mujinplanningcommon.planningutil import itlprogram, itlprogram2

from openravepy import *
import copy, json

controllerurl = 'http://127.0.0.1'
controllerusername = 'testuser'
controllerpassword = 'pass'
#pathtimingzmqport = 11000
pathtimingzmqport = 10900
pathtimingheartbeatport = None
pathtimingheartbeattimeout = 7
scenepk = 'komatsu_ntc.mujin.dae'
robotname = 'komatsu_ntc_TLM-610'
usewebapi = True
initializezmq = False
robotControllerUri = None #'tcp://192.168.13.83:7000'

self = itlplanning2client.ITLPlanning2ControllerClient(controllerurl, controllerusername, controllerpassword, robotControllerUri, scenepk, robotname, pathtimingzmqport, pathtimingheartbeatport, pathtimingheartbeattimeout, usewebapi, initializezmq)


env = Environment()

program = itlprogram.Program('11TEST')
program.LoadData(env, '/data/programs/gcode1')

program2 = itlprogram2.Program('11TEST')
program2.commands = []
program2.commands.append(itlprogram2.MoveCommand())
program2.commands.append(itlprogram2.MoveCommand())
program2.commands.append(itlprogram2.MoveCommand())
programtxt =  open(program.GetFullFilename('/data/programs/gcode1'), 'r+').read()
programtxt2 = json.dumps(program2.GetProgram())


def test_GCodeToITLConverter():
    pass

