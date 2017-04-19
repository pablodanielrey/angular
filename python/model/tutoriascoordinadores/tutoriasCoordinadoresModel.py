import re
import uuid
import datetime

#from model.tutoriascoordinadores.entities.tutorias import Tutoria
#from model.tutoriascoordinadores.entities.student import Student
#from model.tutoriascoordinadores.dao.coordinadorSqlDAO import CoordinadorSqlDAO

#from model.serializer import JSONSerializable


class TutoriasCoordinadoresModel():

    @classmethod
    def getTutorias(cls, ctx, coordId):
       return [1,2,3]
       #tutores = CoordinadorSqlDAO.getTutores(coordId)
       #tutorias = Tutorias.find(ctx, tutorId:tutores).fetch(ctx)
       #return tutorias
       

    @classmethod
    def detailTutoria(cls, ctx, id):
       return "detalle"
       #tutorias = Tutorias.find(ctx, {id:[id]}).fetch(ctx)
       
       
