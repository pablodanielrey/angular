# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid

from model.systems.assistance.justifications.justification import Justification, Repetition
from model.systems.assistance.justifications.exceptions import *



"""
    Licencia Médica Largo Tratamiento
    no tiene límite
"""
class LMLTJustification(Justification):

    id = 'a93d3af3-4079-4e93-a891-91d5d3145155'

    def isJustification(self,id):
        return self.id == id

    """
        retorna la cantidad de justificaciones que se tienen disponibles dentro de un período de tiempo.
    """
    def available(self,utils,con,userId,date=None,period=None):

        return 365


    """
        inicializa un pedido en estado pendiente de una justificación en las fechas indicadas
        solo se tiene en cuenta begin
    """
    def requestJustification(self,utils,con,userId,begin,end,status):

        jid = str(uuid.uuid4())
        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into assistance.justifications_requests (id,user_id,justification_id,jbegin) values (%s,%s,%s,%s)',(jid,userId,self.id,begin))

        events = []
        e = {
            'type':'JustificationsRequestsUpdatedEvent',
            'data':{
                'justification_id':self.id,
                'user_id':userId
            }
        }
        events.append(e)

        req = {
            'id':jid,
            'user_id':userId,
            'justification_id':self.id,
            'begin':begin,
            'end':end
        }

        events.extend(self.updateJustificationRequestStatus(utils,con,userId,req,status))
        return events



    """ actualiza el estado del pedido de la justificacion al estado status """
    def updateJustificationRequestStatus(self,utils,con,userId,req,status):

        requestId = req['id']
        previousStatus = utils._getJustificationRequestStatus(con,requestId)

        cur = con.cursor()
        cur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status) values (%s,%s,%s)',(requestId,userId,status))

        events = []
        e = {
            'type':'JustificationStatusChangedEvent',
            'data':{
                'request_id':requestId,
                'status':status
            }
        }
        events.append(e)


        return events
