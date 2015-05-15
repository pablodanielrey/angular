# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid

from model.systems.assistance.justifications.justification import Justification, Repetition
from model.systems.assistance.justifications.exceptions import *



"""
    Licencia Anual Ordinaria
    no tiene límite, solo el stock actual.
"""
class LAOJustification(Justification):

    id = '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'

    def isJustification(self,id):
        return self.id == id

    """
        retorna la cantidad de justificaciones que se tienen disponibles dentro de un período de tiempo.
    """
    def available(self,utils,con,userId,date=None,period=None):
        cur = con.cursor()
        cur.execute('select stock from assistance.justifications_stock where justification_id = %s and user_id = %s',(self.id,userId))
        if cur.rowcount <= 0:
            return 0

        return cur.fetchone()[0]


    """
        inicializa un pedido en estado pendiente de una justificación en las fechas indicadas
        solo se tiene en cuenta begin
    """
    def requestJustification(self,utils,con,userId,begin,end,status):
        if self.available(utils,con,userId,begin) <= 0:
            raise RestrictionError('No existe stock disponible')

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

        if (previousStatus == 'PENDING' or previousStatus == 'ACCEPTED') and (status == 'CANCELED' or status == 'REJECTED'):

            cur.execute('update assistance.justifications_stock set stock = stock + %s where justification_id = %s and user_id = %s',(1,self.id,req['user_id']))
            e = {
                'type':'JustificationStockChangedEvent',
                'data':{
                    'justification_id':self.id,
                    'user_id':req['user_id']
                }
            }
            events.append(e)

        if (previousStatus is None or previousStatus == 'CANCELED' or previousStatus == 'REJECTED') and (status == 'PENDING' or status == 'APPROVED'):

            cur.execute('update assistance.justifications_stock set stock = stock - %s where justification_id = %s and user_id = %s',(1,self.id,req['user_id']))
            e = {
                'type':'JustificationStockChangedEvent',
                'data':{
                    'justification_id':self.id,
                    'user_id':req['user_id']
                }
            }
            events.append(e)

        return events
