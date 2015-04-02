# -*- coding: utf-8 -*-

import inject, uuid, logging

from model.systems.assistance.offices import Offices
from model.systems.assistance.restrictions import Repetition, CJustification, LAOJustification, AAJustification, BSJustification


class JustificationError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __init__(self,msg):
        Exception.__init__(self,msg)



class Justifications:

    offices = inject.attr(Offices)
    justifications = [
        CJustification(), LAOJustification(), AAJustification(), BSJustification()
    ]



    """ retorna todos los tipos de justificaciones que existan en la base """
    def getJustifications(self,con):
        cur = con.cursor()
        cur.execute('select id,name from assistance.justifications')
        if cur.rowcount <= 0:
            return []

        justs = []
        for j in cur:
            justs.append(
                {
                    'id':j[0],
                    'name':j[1]
                }
            )
        return justs


    """
        retorna el stock actual para la justificación indicada
    """
    def getJustificationStock(self,con,userId,justId,date):

        for j in self.justifications:
            if j.isJustification(justId):
                return j.available(self,con,userId,date)

        """ justificationes desconocidas = 0 """
        return 0



    def _removeStockFromJustification(self,con,userId,justId,stockToRemove):
        for j in self.justifications:
            if j.isJustification(justId):
                j.removeFromStock(self,con,userId,stockToRemove)



    def _addStockToJustification(self,con,userId,justId,stockToAdd):
        for j in self.justifications:
            if j.isJustification(justId):
                j.addToStock(self,con,userId,stockToAdd)


    """
        obtiene todas las justificaciones que estan como ultimo estado en la lista de estados pasada como parametro.
        status = una lista de estados posibles.
        retora un dict con los ids de las justificaciones como key y el estado como value
        { id: status }
    """
    def _getJustificationsInStatus(self,con,status=None):
        cur = con.cursor()

        """ obtengo el ultimo estado de los pedidos de justificacion """
        if status is None:
            cur.execute('select jrs.request_id,jrs.status from assistance.justifications_requests_status as jrs, (select request_id,max(created) as created from assistance.justifications_requests_status group by request_id) as r where r.created = jrs.created and r.request_id = jrs.request_id')
        else:
            cur.execute('select jrs.request_id,jrs.status from assistance.justifications_requests_status as jrs, (select request_id,max(created) as created from assistance.justifications_requests_status group by request_id) as r where r.created = jrs.created and r.request_id = jrs.request_id and jrs.status in %s',(tuple(status),))

        if cur.rowcount <= 0:
            return {}

        statusR = {}
        for rs in cur:
            statusR[rs[0]] = rs[1]

        return statusR



    """
        obtiene todas los pedidos de justificaciones con cierto estado
        status es el estado a obtener. en el caso de que no sea pasado entonces se obtienen todas, en su ultimo estado
        users es una lista de ids de usuarios que piden los requests, si = None o es vacío entonces retorna todas.
    """
    def getJustificationRequests(self,con,status=None,users=None):

        cur = con.cursor()

        statusR = self._getJustificationsInStatus(con,status)
        if len(statusR) <= 0:
            return []

        rids = tuple(statusR.keys())

        if users is None or len(users) <= 0:
            cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where id in %s',(rids,))
        else:
            cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where id in %s and user_id in %s',(rids,tuple(users)))

        if cur.rowcount <= 0:
            return []

        requests = []
        for j in cur:
            jid = j[0]
            requests.append(
                {
                    'id':jid,
                    'user_id':j[1],
                    'justification_id':j[2],
                    'begin':j[3],
                    'end':j[4],
                    'status':statusR[jid]
                }
            )

        return requests


    """
        cambia el estado de un pedido al nuevo estado especificado por status.
        retorna una tupla que contiene
        (
            statusChanged -- True si cambio el stock, False si no cambio el stock
            request -- pedido original al cual se le cambia el estado
        )

        estados posibles a cambiar : PENDING|APPROVED|REJECTED|CANCELED

        PENDING | APROVED = no cambian el stock
        REJECTED | CANCELED = retornan 1 al stock
    """
    def updateJustificationRequestStatus(self,con,userId,requestId,status):
        cur = con.cursor()
        cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where id = %s',(requestId,))
        if cur.rowcount <= 0:
            raise JustificationError('No existe ningún pedido de justificación con id = %s'.format(requestId))

        req = cur.fetchone()
        requester = req[1]
        justificationId = req[2]
        request = {
            'id':req[0],
            'user_id':requester,
            'justification_id':justificationId,
            'begin':req[3],
            'end':req[4],
            'status':status
        }

        changesStock = (status == 'REJECTED' or status == 'CANCELED')
        if changesStock:
            self._removeStockFromJustification(con,requester,justificationId,1)

        cur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status) values (%s,%s,%s)',(requestId,userId,status))

        return (changesStock,request)





    """
        realiza el pedido de justificación para ser aprobado
        estado inicial del pedido = PENDING, con la fecha actual del servidor.
    """
    def requestJustification(self,con,userId,justificationId,begin,end=None):

        stock = self.getJustificationStock(con,userId,justificationId,begin)
        if stock <= 0:
            raise JustificationError('no existe stock disponible')

        jid = str(uuid.uuid4())
        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        if end is None:
            cur.execute('insert into assistance.justifications_requests (id,user_id,justification_id,jbegin) values (%s,%s,%s,%s)',(jid,userId,justificationId,begin))
        else:
            cur.execute('insert into assistance.justifications_requests (id,user_id,justification_id,jbegin,jend) values (%s,%s,%s,%s,%s)',(jid,userId,justificationId,begin,end))

        cur.execute('insert into assistance.justifications_requests_status (request_id,user_id,status) values (%s,%s,%s)',(jid,userId,'PENDING'))

        self._removeStockFromJustification(con,userId,justificationId,1)
