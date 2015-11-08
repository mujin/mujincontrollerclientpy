# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 MUJIN Inc.

class ViewerMixin:

    def SetViewerFromParameters(self, viewerparameters, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewerparameters.update(kwargs)
        return self.Configure({'viewerparameters': viewerparameters}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
        
    def MoveCameraZoomOut(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraZoomOut',
            'zoomdelta': float(zoomdelta),
            'zoommult': float(zoommult),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraZoomIn(self, zoommult=0.9, zoomdelta=20, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraZoomIn',
            'zoomdelta': float(zoomdelta),
            'zoommult': float(zoommult),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraLeft(self, ispan=True, panangle=5.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraLeft',
            'pandelta': float(pandelta),
            'panangle': float(panangle),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraRight(self, ispan=True, panangle=5.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraRight',
            'pandelta': float(pandelta),
            'panangle':float(panangle),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraUp(self, ispan=True, angledelta=3.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraUp',
            'pandelta': float(pandelta),
            'angledelta': float(angledelta),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def MoveCameraDown(self, ispan=True, angledelta=3.0, pandelta=0.04, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        viewercommand = {
            'command': 'MoveCameraDown',
            'pandelta': float(pandelta),
            'angledelta': float(angledelta),
            'ispan': bool(ispan),
        }
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
    
    def SetCameraTransform(self, pose=None, transform=None, distanceToFocus=0.0, usewebapi=False, timeout=10, fireandforget=True, **kwargs):
        """sets the camera transform
        :param transform: 4x4 matrix
        """
        viewercommand = {
            'command': 'SetCameraTransform',
            'distanceToFocus': float(distanceToFocus),
        }
        if transform is not None:
            viewercommand['transform'] = [list(row) for row in transform]
        if pose is not None:
            viewercommand['pose'] = [float(f) for f in pose]
        viewercommand.update(kwargs)
        return self.Configure({'viewercommand': viewercommand}, usewebapi=usewebapi, timeout=timeout, fireandforget=fireandforget)
