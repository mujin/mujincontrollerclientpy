# -*- coding: utf-8 -*-
# Copyright (C) 2014 MUJIN Inc.

class ControllerClientError(Exception):
    pass

class APIServerError(Exception):
    pass

class FluidPlanningError(Exception):
    pass

class BinPickingError(Exception):
    def __init__(self,msg=u''):
        self.msg = unicode(msg)
    def __unicode__(self):
        return u'%s: %s'%(self.__class__.__name__, self.msg)
    
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __repr__(self):
        return '<%s(%r)>'%(self.__class__.__name__, self.msg)
    
    def __eq__(self, r):
        return self.msg == r.msg
    
    def __ne__(self, r):
        return self.msg != r.msg

class HandEyeCalibrationError(Exception):
    def __init__(self,msg=u''):
        self.msg = unicode(msg)
    def __unicode__(self):
        return u'%s: %s'%(self.__class__.__name__, self.msg)
    
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __repr__(self):
        return '<%s(%r)>'%(self.__class__.__name__, self.msg)
    
    def __eq__(self, r):
        return self.msg == r.msg
    
    def __ne__(self, r):
        return self.msg != r.msg

class CablePickingError(Exception):
    def __init__(self,msg=u''):
        self.msg = unicode(msg)
    def __unicode__(self):
        return u'%s: %s'%(self.__class__.__name__, self.msg)
    
    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __repr__(self):
        return '<%s(%r)>'%(self.__class__.__name__, self.msg)
    
    def __eq__(self, r):
        return self.msg == r.msg
    
    def __ne__(self, r):
        return self.msg != r.msg

