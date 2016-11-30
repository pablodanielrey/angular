# -*- coding: utf-8 -*-
import logging
from model.designation.designation import Designation
from model.offices.office import Office
from model.users.users import User
from model.offices.office import Office
from model.designation.position import Position



"""
from model.sileg.place.place import Place
from model.sileg.position.position import Position
from model.users.users import User
"""

class SilegModel:

    @classmethod
    def getUsers(cls, con):
        placesIds = Office.findAll(con, [{"value":"cdepartment"}])
        designationIds = Designation.findByPlaces(con, placesIds)
        designations = Designation.findByIds(con, designationIds)
        userIds = [d.userId for d in designations]
        return User.findById(con, userIds)

    @classmethod
    def getCathedras(cls, con):
        placesIds = Office.findAll(con, [{"value":"cdepartment"}])
        return Office.findByIds(con, placesIds)


    @classmethod
    def findPositionsActiveByUser(cls, con, userId):
        designationIds = Designation.findByUsers(con, [userId])
        designations = Designation.findByIds(con, designationIds)

        designationsActive = [d for d in designations if d.out is None and d.description == 'original' and Office.findByIds(con, [d.officeId])[0].type == 'cdepartment']

        data = {}
        for designation in designationsActive:
            position = Position.findByIds(con, [designation.positionId])[0]
            place = Office.findByIds(con, [designation.officeId])[0]
            designation.place = place
            if position.position not in data:
                data[position.position] = {"position":position, "designations":[]}

            data[position.position]["designations"].append(designation)

        return data


    @classmethod
    def findPositionsActiveByPlace(cls, con, placeId):
        designationIds = Designation.findByPlaces(con, [placeId])
        designations = Designation.findByIds(con, designationIds)

        designationsActive = [d for d in designations if d.out is None and d.description == 'original' and Office.findByIds(con, [d.officeId])[0].type == 'cdepartment' ]

        data = {}

        for designation in designationsActive:
            position = Position.findByIds(con, [designation.positionId])[0]
            user = User.findById(con, [designation.userId])[0]
            designation.user = user
            if position.position not in data:
                data[position.position] = {"position":position, "designations":[]}

            data[position.position]["designations"].append(designation)

        return data

    """


    @classmethod
    def findPlacesByIds(cls, con, ids):
        return Place.findById(con, ids)

    @classmethod
    def findPositionsByIds(cls, con, ids):
        return Position.findById(con, ids)

    @classmethod
    def findDesignationsByIds(cls, con, ids):
        designations = Designation.findById(con, ids)

        for i in range(len(designations)):
            position = Position.findById(con, [designations[i].positionId])[0]
            designations[i].position = position
            user = User.findById(con, [designations[i].userId])[0]
            designations[i].user = user
            place = Place.findById(con, [designations[i].placeId])[0]
            designations[i].place = place

        return designations


    @classmethod
    def findUsersByIds(cls, con, ids):
        return User.findById(con, ids)


    @classmethod
    def findPositionsAll(cls, con):
        positionIds =  Position.findAll(con)
        positions = Position.findById(con, positionIds)
        return positions

    @classmethod
    def findPlacesAll(cls, con):
        placesIds =  Place.findAll(con)
        places = Place.findById(con, placesIds)
        return places


    @classmethod
    def findDesignationsBySearch(cls, con, search):
        if search is None:
            return

        designations = Designation.findBySearch(con, search)

        for i in range(len(designations)):
            position = Position.findById(con, [designations[i].positionId])[0]
            designations[i].position = position
            user = User.findById(con, [designations[i].userId])[0]
            designations[i].user = user
            place = Place.findById(con, [designations[i].placeId])[0]
            designations[i].place = place

        return designations


    @classmethod
    def persistDesignation(cls, con, designation):
        designation.persist(con);
    """
