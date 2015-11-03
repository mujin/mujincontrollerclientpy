
class JogMixin:

    def SetJogModeVelocities(self, jogtype, movejointsigns, toolname=None, robotspeed=None, robotaccelmult=None, usewebapi=False, timeout=1, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'SetJogModeVelocities',
            'jogtype': jogtype,
            'movejointsigns': movejointsigns,
        }
        if toolname is not None:
            taskparameters['toolname'] = toolname
        if robotspeed is not None:
            taskparameters['robotspeed'] = robotspeed
        if robotaccelmult is not None:
            taskparameters['robotaccelmult'] = robotaccelmult
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
