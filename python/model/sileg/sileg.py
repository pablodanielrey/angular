
import logging
from model.sileg.designation.designation import Designation
from model.sileg.place.place import Place
from model.sileg.position.position import Position
from model.users.users import User

class SilegModel:

    @classmethod
    def getEconoPageDataUser(cls, con, userId):
        designationIds = Designation.findByUserId(con, [userId])
        designations = Designation.findById(con, designationIds)

        designationsActive = [d for d in designations if d.out is None and d.description == 'original' and Place.findById(con, [d.placeId])[0].type == 'Catedra' ]


        data = {}

        for designation in designationsActive:
            position = Position.findById(con, [designation.positionId])[0]
            place = Place.findById(con, [designation.placeId])[0]
            designation.place = place
            if position.description not in data:
                data[position.description] = {"position":position, "designations":[]}

            data[position.description]["designations"].append(designation)

        return data


    @classmethod
    def getEconoPageDataPlace(cls, con, placeId):

        designationIds = Designation.findByPlaceId(con, [placeId])
        designations = Designation.findById(con, designationIds)

        designationsActive = [d for d in designations if d.out is None and d.description == 'original' and Place.findById(con, [d.placeId])[0].type == 'Catedra' ]

        data = {}

        for designation in designationsActive:
            position = Position.findById(con, [designation.positionId])[0]
            user = User.findById(con, [designation.userId])[0]
            designation.user = user
            if position.description not in data:
                data[position.description] = {"position":position, "designations":[]}

            data[position.description]["designations"].append(designation)

        return data

    @classmethod
    def getUsers(cls, con):
        designationIds = Designation.findAll(con)
        designations = Designation.findById(con, designationIds)

        designationsActive = [d for d in designations if d.out is None and d.description == 'original' and Place.findById(con, [d.placeId])[0].type == 'Catedra' ]

        userIds = [d.userId for d in designationsActive]

        return User.findById(con, userIds)


    @classmethod
    def getCathedras(cls, con):
        designationIds = Designation.findAll(con)
        designations = Designation.findById(con, designationIds)

        designationsActive = [d for d in designations if d.out is None and d.description == 'original' and Place.findById(con, [d.placeId])[0].type == 'Catedra' ]

        placesIds = [d.placeId for d in designationsActive]

        return Place.findById(con, placesIds)




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
