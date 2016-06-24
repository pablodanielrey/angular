
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
    def getPositionsById(cls, con, ids):
        return Position.findById(con, ids)
        
