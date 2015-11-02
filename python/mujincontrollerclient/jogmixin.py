
class JogMixin:

    def StartJogMode(self, jogtype, robotspeed, robotaccelmult, checkcollision=True, usewebapi=False, timeout=1, fireandforget=False, **kwargs):
        """
        :param jogtype: joints, tools
        """
        taskparameters = {
            'command': 'StartJogMode',
            'jogtype': jogtype,
            'robotspeed': robotspeed,
            'robotaccelmult': robotaccelmult,
            'checkcollision': checkcollision,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def EndJogMode(self, usewebapi=False, timeout=1, fireandforget=False, **kwargs):
        taskparameters = {'command': 'EndJogMode'}
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)

    def SetJogDirection(self, dofindex, direction, usewebapi=False, timeout=1, fireandforget=False, **kwargs):
        taskparameters = {
            'command': 'SetJogDirection',
            'dofindex': dofindex,
            'direction': direction,
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
