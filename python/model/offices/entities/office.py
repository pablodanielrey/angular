# -*- coding: utf-8 -*-
import logging

from model import Ids
from model.entity import Entity

class Office(Entity):

    def __init__(self):
        self.id = None
        self.name = None
        self.telephone = None
        self.number = None
        self.type = None
        self.email = None
        self.parent = None
        self.public = None
        self.removed = None


    @classmethod
    def findByUserId(cls, ctx, userId, tree=False, *args, **kwargs):
        return Ids(cls, ctx.dao(cls).findByUserId(ctx, userId, tree=False, *args, **kwargs))

    @classmethod
    def findChildsByIds(cls, ctx, ids, tree=False, *args,  **kwargs):
        return Ids(cls, ctx.dao(cls).findChildsByIds(ctx, ids, tree, *args, **kwargs))
