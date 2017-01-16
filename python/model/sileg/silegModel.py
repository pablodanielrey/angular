# -*- coding: utf-8 -*-
import logging
from model.sileg.entities import TeachingDesignation
from model.sileg.entities import TeachingPlace
from model.users.entities.user import User




"""
from model.sileg.place.place import Place
from model.sileg.position.position import Position
from model.users.users import User
"""

class SilegModel:

    @classmethod
    def getUsers(cls, ctx):
        placesIds = TeachingPlace.find(ctx, type=["cdepartment"])
        designations = TeachingDesignation.find(ctx, placeId=placesIds).fetch(ctx)
        userIds = [d.userId for d in designations]
        return User.findByIds(con, userIds)


    @classmethod
    def findPositionsActiveByUser(cls, con, userId):
        placesIds = TeachingPlace.find(ctx, type=["cdepartment"])
        designations = TeachingDesignation.find(ctx, userId=[userId], out=False, placeId=placesIds).fetch(ctx)

        """
        data = {}
        for designation in designations:
            position = Position.findByIds(con, [designation.positionId])[0]
            place = Office.findByIds(con, [designation.officeId])[0]
            designation.place = place
            if position.position not in data:
                data[position.position] = {"position":position, "designations":[]}

            data[position.position]["designations"].append(designation)

        return data
        """

    @classmethod
    def findPositionsActiveByPlace(cls, con, placeId):
        designationIds = Designation.findByPlaces(con, [placeId])
        designations = Designation.findByIds(con, designationIds)

        designationsActive = [d for d in designations if d.out is None and d.description == 'original' and Office.findByIds(con, [d.officeId])[0].type["value"] == 'cdepartment' ]

        data = {}

        for designation in designationsActive:
            position = Position.findByIds(con, [designation.positionId])[0]
            user = User.findById(con, [designation.userId])[0]
            designation.user = user
            if position.position not in data:
                data[position.position] = {"position":position, "designations":[]}

            data[position.position]["designations"].append(designation)

        return data
