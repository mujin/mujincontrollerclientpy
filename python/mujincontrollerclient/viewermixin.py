# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.

class ViewerMixin:

    def SetViewerFromParameters(self, viewerparameters, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        taskparameters = {'command': 'SetViewerFromParameters',
                          'viewerparameters':viewerparameters
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
        
    def MoveCameraZoomOut(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        taskparameters = {'command': 'MoveCameraZoomOut',
                          'zoomdelta':float(zoomdelta),
                          'zoommult': float(zoommult)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraZoomIn(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        taskparameters = {'command': 'MoveCameraZoomIn',
                          'zoomdelta':float(zoomdelta),
                          'zoommult':float(zoommult)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraLeft(self, ispan=True, panangle=5.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        taskparameters = {'command': 'MoveCameraLeft',
                          'pandelta':float(pandelta),
                          'panangle':float(panangle),
                          'ispan':bool(ispan)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraRight(self, ispan=True, panangle=5.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        taskparameters = {'command': 'MoveCameraRight',
                          'pandelta':float(pandelta),
                          'panangle':float(panangle),
                          'ispan':bool(ispan)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraUp(self, ispan=True, angledelta=3.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        taskparameters = {'command': 'MoveCameraUp',
                          'pandelta':float(pandelta),
                          'angledelta':float(angledelta),
                          'ispan':bool(ispan)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraDown(self, ispan=True, angledelta=3.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        taskparameters = {'command': 'MoveCameraDown',
                          'pandelta':float(pandelta),
                          'angledelta':float(angledelta),
                          'ispan':bool(ispan)
        }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def SetCameraTransform(self, pose=None, transform=None, distanceToFocus=0.0, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        """sets the camera transform
        :param transform: 4x4 matrix
        """        
        taskparameters = {'command': 'SetCameraTransform',
                          'distanceToFocus':float(distanceToFocus),
                          }
        if transform is not None:
            taskparameters['transform'] = [list(row) for row in transform]
        if pose is not None:
            taskparameters['pose'] = [float(f) for f in pose]
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def GetCameraTransform(self, usewebapi=False, timeout=10, **kwargs):
        """gets the camera transform, and other
        """
        taskparameters = {'command': 'GetCameraTransform'
                          }
        taskparameters.update(kwargs)
        return self.ExecuteCommand(taskparameters, usewebapi=usewebapi, timeout=timeout)

