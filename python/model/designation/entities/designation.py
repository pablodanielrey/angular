# -*- coding: utf-8 -*-
from model.entity import Entity

class Designation(Entity):

    def __init__(self):
        self.id = None
        self.placeId = None
        self.positionId = None
        self.userId = None

        self.parentId = None
        self.startId = None

        self.start = None
        self.end = None

        self.type = None
