# -*- coding: utf-8 -*-
import logging
from model.sileg.entities.teachingDesignation import TeachingDesignation
from model.sileg.entities.teachingPlace import TeachingPlace
from model.sileg.entities.teachingPosition import TeachingPosition
from model.users.entities.user import User




"""
from model.sileg.place.place import Place
from model.sileg.position.position import Position
from model.users.users import User
"""

class SilegModel:

    @classmethod
    def getUsers(cls, ctx):
        placesIds = TeachingPlace.find(ctx, type=["catedra"])
        designations = TeachingDesignation.find(ctx, placeId=placesIds).fetch(ctx)
        userIds = [d.userId for d in designations]
        return User.findByIds(ctx, userIds)


    @classmethod
    def findPositionsActiveByUser(cls, ctx, userId):
        placesIds = TeachingPlace.find(ctx, type=["catedra"])
        designations = TeachingDesignation.find(ctx, userId=[userId], out=False, placeId=placesIds).fetch(ctx)

        data = {}
        for d in designations:
            position = TeachingPosition.findByIds(ctx, [d.positionId])[0]
            place = TeachingPlace.findByIds(ctx, [d.placeId])[0]
            d.place = place
            if position.position not in data:
                data[position.position] = {"position":position, "designations":[]}

            data[position.position]["designations"].append(d)

        return data

    @classmethod
    def findPositionsActiveByPlace(cls, ctx, placeId):
        designations = TeachingDesignation.find(ctx, out=False, placeId=[placeId]).fetch(ctx)

        data = {}
        for d in designations:
            position = TeachingPosition.findByIds(ctx, [d.positionId])[0]
            user = User.findByIds(ctx, [d.userId])[0]
            d.user = user
            if position.position not in data:
                data[position.position] = {"position":position, "designations":[]}

            data[position.position]["designations"].append(d)

        return data
