import re
import uuid
import datetime

from model.tutoriascoordinadores.entities.tutorias import Tutoria
from model.tutoriascoordinadores.entities.student import Student

from model.serializer import JSONSerializable


class TutoriasCoordinadoresModel():

    @classmethod
    def getTutoriasByTutorId(cls, ctx, tutorId):
       tutorias = Tutorias.find(ctx, {tutorId:tutorId}).fetch(ctx)
       
       
       
