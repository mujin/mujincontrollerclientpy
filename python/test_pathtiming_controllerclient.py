from mujincontrollerclient import itlplanning2client
from mujinplanningcommon.planningutil import itlprogram, itlprogram2

from openravepy import *
import copy, json
from numpy import *

controllerurl = 'http://127.0.0.1'
controllerusername = 'testuser'
controllerpassword = 'pass'
pathtimingzmqport = 11000
#pathtimingzmqport = 10900
pathtimingheartbeatport = None
pathtimingheartbeattimeout = 7
scenepk = 'mh24_v3.mujin.dae'
robotname = 'Motoman_MH24'
usewebapi = True
initializezmq = False
robotControllerUri = None #'tcp://192.168.13.83:7000'

self = itlplanning2client.ITLPlanning2ControllerClient(controllerurl, controllerusername, controllerpassword, robotControllerUri, scenepk, robotname, pathtimingzmqport, pathtimingheartbeatport, pathtimingheartbeattimeout, usewebapi, initializezmq)


env = Environment()

# viewerparameters =  { 'type':'qtcoin', 'nearplane':0.01 }
# viewerparameters['type'] += ' 0 0 0 2'
# viewerparameters['mode'] = 'minimal'
# viewerparameters['trackobject'] = u''
# viewerparameters['tracklinkname'] = u''
# viewerparameters['trackmanipname'] = u''
# viewerparameters['trackikparam'] = u''
# 
# program = itlprogram.Program('11TEST')
# program.LoadData(env, '/data/programs/gcode1')
# 
# program2 = itlprogram2.Program('11TEST')
# program2.commands = []
# program2.commands.append(itlprogram2.MoveCommand())
# program2.commands.append(itlprogram2.MoveCommand())
# program2.commands.append(itlprogram2.MoveCommand())
# programtxt =  open(program.GetFullFilename('/data/programs/gcode1'), 'r+').read()
# programtxt2 = json.dumps(program2.GetProgram())


program = itlprogram2.Program('test')
program.commands = []
cmd = itlprogram2.MoveCommand()
cmd.movetype = 'MoveAlongSurface'
cmd.position = itlprogram2.Position()
cmd.position.poselocal = [  6.1019657330801003e-01,  -6.8890605027747270e-02,
         5.3384032281349386e-02,   7.8744166232137924e-01,
         7.9396265176304541e+02,   3.2023370625965549e+02,
         2.5383298996225722e+02]
program.commands.append(cmd)

cmd1 = itlprogram2.MoveCommand()
cmd1.movetype = 'MoveAlongSurface'
cmd1.position = itlprogram2.Position()
cmd1.position.poselocal = [  8.9266988671383984e-01,   3.8686962994562729e-02,
         7.8096666112977164e-02,  -4.4220436790085627e-01,
         5.4648693154972898e+02,  -7.7430567918633972e+02,
         2.5383298996251779e+02]
program.commands.append(cmd1)

jsonprogram = program.GetProgram()

def test_GCodeToITLConverter():
    pass

