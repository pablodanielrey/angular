# -*- coding: utf-8 -*-
import re
import uuid
import datetime


from model.tutoriascoordinadores.entities.User import User
from model.tutoriascoordinadores.entities.Tutoria import Tutoria
from model.tutoriascoordinadores.entities.Situation import Situation



class TutoriasCoordinadoresModel():


    @classmethod
    def getTutorias(cls, ctx, coordId):
        usersIds = User.findTutores(ctx, coordId)
        users = usersIds.fetch(ctx)
        tutorias = Tutoria.find(ctx, tutorId=usersIds.values).fetch(ctx)
        for t in tutorias:
            for u in users:
                if t.tutorId == u.id:
                    t.tutor = u


        return tutorias



    @classmethod
    def detailTutoria(cls, ctx, id):
       situations = Situation.find(ctx, tutoringId=[id]).fetch(ctx)      
       userIds = []

       for s in situations:
         userIds.append(s.userId)

       users = User.findByIds(ctx, userIds)
       for s in situations:
         for u in users:
            if s.userId == u.id:
                s.user = u
          
       
       
       return situations
       
       
       
       
