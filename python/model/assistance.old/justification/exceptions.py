# -*- coding: utf-8 -*-

class JustificationError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __init__(self,msg):
        Exception.__init__(self,msg)



class RestrictionError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __init__(self,msg):
        Exception.__init__(self,msg)
