# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid
import inject

from model.systems.assistance.justifications.exceptions import *

from model.systems.assistance.offices import Offices

from model.systems.assistance.justifications.AAJustification import AAJustification
from model.systems.assistance.justifications.BSJustification import BSJustification
from model.systems.assistance.justifications.CJustification import CJustification
from model.systems.assistance.justifications.LAOJustification import LAOJustification



class Justifications:

    offices = inject.attr(Offices)

    justifications = [
        CJustification(), LAOJustification(), AAJustification(), BSJustification()
    ]


    """ obtiene un requerimiento de justificacion dado el id """
    def _findJustificationRequestById(self,con,id):
        cur = con.cursor()
        cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where id = %s',(id,))
        if cur.rowcount <= 0:
            return None

        j = cur.fetchone()
        req = {
            'id':j[0],
            'user_id':j[1],
            'justification_id':j[2],
            'begin':j[3],
            'end':j[4]
        }

        return req


    """
        obtiene el ultimo estado del pedido de justificación indicado por reqId
    """
    def _getJustificationRequestStatus(self,con,reqId):
        cur = con.cursor()
        cur.execute('select jrs.status from assistance.justifications_requests_status as jrs, (select request_id,max(created) as created from assistance.justifications_requests_status group by request_id) as r where r.created = jrs.created and r.request_id = jrs.request_id')
        if cur.rowcount <= 0:
            return None

        return cur.fetchone()[0]


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
        obtiene todos los pedidos de justificaciones que tiene permisos de manejar, en cierto estado.
        group = ROOT|TREE --> ROOT = oficinas directas, TREE = oficinas directas y todas las hijas
    """
    def getJustificationRequestsToManage(self,con,userId,status,group='ROOT'):

        tree = False
        if group == 'TREE':
            tree = True
        offices = self.offices.getOfficesByUserRole(con,userId,tree)
        logging.debug('officesByUserRole : {}'.format(offices))

        if offices is None or len(offices) <= 0:
            return []

        officesIds = list(map(lambda o: o['id'], offices))
        users = self.offices.getOfficesUsers(con,officesIds)
        logging.debug('getOfficesUsers : {}'.format(users))

        while userId in users:
            users.remove(userId)

        if users is None or len(users) <= 0:
            return []

        justifications = self.getJustificationRequests(con,status,users)

        return justifications










    """
        retorna el stock actual para la justificación indicada
    """
    def getJustificationStock(self,con,userId,justId,date,period=None):

        for j in self.justifications:
            if j.isJustification(justId):
                return j.available(self,con,userId,date,period)

        """ justificationes desconocidas = 0 """
        return 0


    """
        cambia el estado de un pedido al nuevo estado especificado por status.
        retorna los eventos a ser disparados
        estados posibles a cambiar : PENDING|APPROVED|REJECTED|CANCELED
    """
    def updateJustificationRequestStatus(self,con,userId,requestId,status):

        req = self._findJustificationRequestById(con,requestId)
        if req is None:
            raise JustificationError('No existe ningún pedido de justificación con id = %s'.format(requestId))

        for j in self.justifications:
            if j.isJustification(req['justification_id']):
                return j.updateJustificationRequestStatus(self,con,userId,req,status)

        raise JustificationError('No se puede encontrar ese tipo de justificación')



    """
        realiza el pedido de justificación para ser aprobado
        estado inicial del pedido = PENDING, con la fecha actual del servidor.
    """
    def requestJustification(self,con,userId,justificationId,begin,end=None):

        for j in self.justifications:
            if j.isJustification(justificationId):
                return j.requestJustification(self,con,userId,begin,end)

        raise JustificationError('No se puede encontrar ese tipo de justificación')