# -*- coding: utf-8 -*-

class ObjectView(object):
  def __init__(self,d):
      self.__dict__ = d
