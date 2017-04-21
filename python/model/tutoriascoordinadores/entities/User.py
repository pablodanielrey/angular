# -*- coding: utf-8 -*-
from model import Ids
from model.entity import Entity

class User(Entity):

    def __init__(self):
        self.id = None
        self.name = None
        self.lastname = None
        self.dni = None


    @classmethod
    def findTutores(cls, ctx, coordinadorId):
        return Ids(cls, ctx.dao(cls).findTutores(ctx, coordinadorId))
