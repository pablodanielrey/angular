# -*- coding: utf-8 -*-
from model.entity import Entity

class Designation(Entity):

    def __init__(self):
        self.id = None
        self.placeId = None
        self.positionId = '1'
        self.userId = None

        self.parentId = None
        self.originalId = None

        self.start = None
        self.end = None


    def expire(self, ctx):
        ctx.dao(self).expireByIds(ctx, [self.id])
