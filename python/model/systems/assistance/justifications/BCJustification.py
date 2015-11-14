# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid

from model.systems.assistance.justifications.justification import Justification, Repetition
from model.systems.assistance.justifications.exceptions import *


"""
    Boletas en comision
"""
class BCJustification(Justification):

    id = 'cb2b4583-2f44-4db0-808c-4e36ee059efe'

    def isJustification(self,id):
        return self.id == id


    def _isJustifiedTimeStart(self,sched,whs,justification,tolerancia, date = None):
        return False

    def _isJustifiedTimeEnd(self,sched,whs, justification, tolerancia, date = None):

        whEnd = whs[-1]['end']
        if whEnd >= justification['begin'] and ('end' not in justification or justification['end'] is None or sched.getEnd(date) <= justification['end']):
            return True
        return False

    def _isJustifiedTime(self,justification,start,end):
        if 'begin' not in justification or start is None or end is None:
            return False
        if start >= justification['begin'] and ('end' not in justification or end <= justification['end']):
            return True
        return False

    """
        inicializa un pedido en estado pendiente de una justificación en las fechas indicadas
    """
    def requestJustification(self,utils,con,userId,requestor_id,begin,end=None,status='PENDING'):

        jid = str(uuid.uuid4())
        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into assistance.justifications_requests (id,user_id,requestor_id,justification_id,jbegin,jend) values (%s,%s,%s,%s,%s,%s)',(jid,userId,requestor_id,self.id,begin,end))

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
