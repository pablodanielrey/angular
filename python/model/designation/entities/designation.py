# -*- coding: utf-8 -*-
from model.entity import Entity

class Designation(Entity):

    def __init__(self):
        self.id = None
        self.officeId = None
        self.positionId = '1'
        self.userId = None
        self.start = None
        self.end = None
        self.out = None
        self.parentId = None
        self.resolution = None
        self.record = None
        self.originalId = None

    def expire(self, ctx):
        con['dao'].expireByIds(ctx, [self.id])
