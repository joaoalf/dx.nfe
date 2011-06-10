# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.component import adapts
from interfaces import INFeXml, INFeInput

class NFeXml(object):
    implements(INFeXml)
    adapts(INFeInput)
    
    def __init__(self, root):
        self.root = root
