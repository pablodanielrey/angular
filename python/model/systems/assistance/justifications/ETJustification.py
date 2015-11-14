# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid

from model.systems.assistance.justifications.justification import Justification, Repetition
from model.systems.assistance.justifications.exceptions import *



"""
    Entrada tarde justificada
    no tiene límite
"""
class ETJustification(Justification):

    id = '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7'

    def isJustification(self,id):
        return self.id == id

    def _isJustifiedTimeStart(self,sched,whs,justification,tolerancia, date = None):
        if len(whs) > 0:
            return True
        return False

    def _isJustifiedTime(self,justification,start,end, date = None):
        return False

    """
        retorna la cantidad de justificaciones que se tienen disponibles dentro de un período de tiempo.
    """
    def available(self,utils,con,userId,date=None,period=None):

        return 365

    """
        inicializa un pedido en estado pendiente de una justificación en las fechas indicadas
        solo se tiene en cuenta begin
    """
    def requestJustification(self,utils,con,userId,requestor_id,begin,end,status):

        jid = str(uuid.uuid4())
        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into assistance.justifications_requests (id,user_id,requestor_id,justification_id,jbegin) values (%s,%s,%s,%s,%s)',(jid,userId,requestor_id,self.id,begin))

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

        created = datetime.datetime.now()
        aux = created - datetime.timedelta(seconds=60)
        e = self.updateJustificationRequestStatus(utils,con,userId,req,'PENDING',aux)
        if status != None and status != 'PENDING':
            e = self.updateJustificationRequestStatus(utils,con,userId,req,status,created)
        events.extend(e)
        return events



    """ actualiza el estado del pedido de la justificacion al estado status """
    def updateJustificationRequestStatus(self,utils,con,userId,req,status,created=datetime.datetime.now()):

        requestId = req['id']
        previousStatus = utils._getJustificationRequestStatus(con,requestId)

        cur = con.cursor()
        cur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status,created) values (%s,%s,%s,%s)',(requestId,userId,status,created))

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
