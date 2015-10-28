# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid
import inject

from model.systems.assistance.justifications.exceptions import *

from model.systems.offices.offices import Offices

from model.systems.assistance.justifications.AAJustification import AAJustification
from model.systems.assistance.justifications.BSJustification import BSJustification
from model.systems.assistance.justifications.BCJustification import BCJustification
from model.systems.assistance.justifications.CJustification import CJustification
from model.systems.assistance.justifications.LAOJustification import LAOJustification
from model.systems.assistance.justifications.A102Justification import A102Justification
from model.systems.assistance.justifications.CumpJustification import CumpJustification
from model.systems.assistance.justifications.PEJustification import PEJustification
from model.systems.assistance.justifications.R638Justification import R638Justification
from model.systems.assistance.justifications.LMCDJustification import LMCDJustification
from model.systems.assistance.justifications.LMLTJustification import LMLTJustification
from model.systems.assistance.justifications.LMAFJustification import LMAFJustification
from model.systems.assistance.justifications.JMJustification import JMJustification
from model.systems.assistance.justifications.HolidayJustification import HolidayJustification
from model.systems.assistance.justifications.ParoJustification import ParoJustification
from model.systems.assistance.justifications.MourningJustification import MourningJustification
from model.systems.assistance.justifications.BloodDonationJustification import BloodDonationJustification
from model.systems.assistance.justifications.ARTJustification import ARTJustification
from model.systems.assistance.justifications.BJustification import BJustification
from model.systems.assistance.justifications.CCJustification import CCJustification
from model.systems.assistance.justifications.ICJustification import ICJustification

from model.systems.assistance.justifications.ETJustification import ETJustification
from model.systems.assistance.justifications.AUTJustification import AUTJustification
from model.systems.assistance.justifications.CONJustification import CONJustification
from model.systems.assistance.justifications.VJEJustification import VJEJustification
from model.systems.assistance.justifications.SUSJustification import SUSJustification
from model.systems.assistance.justifications.SGSJustification import SGSJustification
from model.systems.assistance.justifications.MATJustification import MATJustification
from model.systems.assistance.justifications.INVJustification import INVJustification
from model.systems.assistance.justifications.NACJustification import NACJustification
from model.systems.assistance.justifications.PONJustification import PONJustification
from model.systems.assistance.justifications.PRNJustification import PRNJustification






from model.systems.assistance.date import Date



class Justifications:

    offices = inject.attr(Offices)
    date = inject.attr(Date)

    justifications = [
        CJustification(), LAOJustification(), AAJustification(), BSJustification(), R638Justification(), PEJustification(),
        CumpJustification(), A102Justification(), LMCDJustification(), LMLTJustification(), BloodDonationJustification(),
        LMAFJustification(), JMJustification(), HolidayJustification(), ParoJustification(), MourningJustification(), BCJustification(),
        ARTJustification(), BJustification(), CCJustification(), ICJustification(), ETJustification(), AUTJustification(), CONJustification(),
        VJEJustification(), SUSJustification(), SGSJustification(), MATJustification(), INVJustification(), NACJustification(), PONJustification(),
        PRNJustification(),
    ]


    ''' obtiene un requerimiento de justificacion dado el id '''
    def findJustificationRequestById(self,con,id):
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


    '''
        obtiene el ultimo estado del pedido de justificación indicado por reqId
    '''
    def _getJustificationRequestStatus(self,con,reqId):
        cur = con.cursor()
        cur.execute('select jrs.status from assistance.justifications_requests_status as jrs, (select request_id,max(created) as created from assistance.justifications_requests_status group by request_id) as r where r.created = jrs.created and r.request_id = jrs.request_id and r.request_id = %s',(reqId,))
        if cur.rowcount <= 0:
            return None

        return cur.fetchone()[0]


    '''
        obtiene todas las justificaciones que estan como ultimo estado en la lista de estados pasada como parametro.
        status = una lista de estados posibles.
        retora un dict con los ids de las justificaciones como key y un array de el estado y el user_id como value
        { id: status }
    '''
    def _getJustificationsInStatus(self,con,status=None):
        cur = con.cursor()

        ''' obtengo el ultimo estado de los pedidos de justificacion '''
        if status is None:
            cur.execute('select jrs.request_id,jrs.status,jrs.user_id from assistance.justifications_requests_status as jrs, (select request_id,max(created) as created from assistance.justifications_requests_status group by request_id) as r where r.created = jrs.created and r.request_id = jrs.request_id')
        else:
            cur.execute('select jrs.request_id,jrs.status,jrs.user_id from assistance.justifications_requests_status as jrs, (select request_id,max(created) as created from assistance.justifications_requests_status group by request_id) as r where r.created = jrs.created and r.request_id = jrs.request_id and jrs.status in %s',(tuple(status),))

        if cur.rowcount <= 0:
            return {}

        statusR = {}
        for rs in cur:
            statusR[rs[0]] = [rs[1],rs[2]]

        return statusR




    ''' retorna todos los tipos de justificaciones que existan en la base '''
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

    ''' retorna todos los tipos de justificaciones que existan en la base '''
    def getJustificationsByUser(self,con,userId):
        cur = con.cursor()

        cur.execute("""
         SELECT DISTINCT j.id, j.name
         FROM assistance.justifications AS j
         INNER JOIN assistance.positions_justifications AS pj ON (j.id = pj.justification_id)
         INNER JOIN assistance.positions AS p ON (p.name = pj.position)
         WHERE p.user_id = %s;
         """,(userId,))

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




    ''' retorna todos los tipos de justificaciones que existan en la base '''
    def getJustificationById(self,con,id):
        cur = con.cursor()
        cur.execute('select id,name from assistance.justifications where id = %s',(id,))
        if cur.rowcount <= 0:
            return []

        for j in cur:
            justification = {
                    'id':j[0],
                    'name':j[1]
                }
            return justification

        return None



    '''
        obtiene las justificaciones generales
    '''
    def getGeneralJustificationRequests(self,con):
        cur = con.cursor()
        cur.execute('select id,justification_id,jbegin,jend from assistance.general_justifications')
        if cur.rowcount <= 0:
            return []

        justs = []
        for j in cur:
            justs.append(
                {
                    'id':j[0],
                    'justification_id':j[1],
                    'begin':j[2],
                    'end':j[3],
                }
            )

        return justs



    '''
        obtiene todas los pedidos de justificaciones con cierto estado
        status es el estado a obtener. en el caso de que no sea pasado entonces se obtienen todas, en su ultimo estado
        users es una lista de ids de usuarios que piden los requests, si = None o es vacío entonces retorna todas.
    '''
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
            userId = j[1]
            jid = j[0]
            requests.append(
                {
                    'id':jid,
                    'user_id':userId,
                    'justification_id':j[2],
                    'begin':j[3],
                    'end':j[4],
                    'status':statusR[jid][0],
                    'requestor_id':statusR[jid][1]
                }
            )

        return requests




    '''
        obtiene todas los pedidos de justificaciones con cierto estado y que se encuentre entre esas dos fechas
        start es la fecha de inicio de la busqueda. en el caso de que no sea pasado entonces no se pone como restriccion el inicio
        end es la fecha de limite de la busqueda. en el caso de que no sea pasado entonces no se pone como restriccion el end
        status es el estado a obtener. en el caso de que no sea pasado entonces se obtienen todas, en su ultimo estado
        users es una lista de ids de usuarios que piden los requests, si = None o es vacío entonces retorna todas.
    '''
    def getJustificationRequestsByDate(self,con,status=None,users=None,start=None,end=None):
        logging.debug('buscando justifications : {}, {}, {}, {}'.format(status,users,start,end))

        cur = con.cursor()

        statusR = self._getJustificationsInStatus(con,status)
        if len(statusR) <= 0:
            return []

        rids = tuple(statusR.keys())



        if start is not None and end is not None:
            if users is None or len(users) <= 0:
                cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where jbegin >= %s and jbegin <= %s and id in %s',(start,end,rids))
            else:
                cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where jbegin >= %s and jbegin <= %s and id in %s and user_id in %s',(start,end,rids,tuple(users)))
        else:
            if start is None:
                if users is None or len(users) <= 0:
                    cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where jbegin <= %s and id in %s',(end,rids))
                else:
                    cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where jbegin <= %s and id in %s and user_id in %s',(start,end,rids,tuple(users)))
            else:
                if users is None or len(users) <= 0:
                    cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where jbegin >= %s and id in %s',(end,rids))
                else:
                    cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where jbegin >= %s and id in %s and user_id in %s',(start,end,rids,tuple(users)))

        if cur.rowcount <= 0:
            return []

        requests = []
        for j in cur:
            userId = j[1]
            jid = j[0]
            requests.append(
                {
                    'id':jid,
                    'user_id':userId,
                    'justification_id':j[2],
                    'begin':j[3],
                    'end':j[4],
                    'status':statusR[jid][0],
                    'requestor_id':statusR[jid][1]
                }
            )

        return requests





    '''
        obtiene todos los pedidos de justificaciones que tiene permisos de manejar, en cierto estado.
        group = ROOT|TREE --> ROOT = oficinas directas, TREE = oficinas directas y todas las hijas
    '''
    def getJustificationRequestsToManage(self,con,userId,status,group='ROOT'):

        tree = False
        if group == 'TREE':
            tree = True
        offices = self.offices.getOfficesByUserRole(con,userId,tree,'autoriza')
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




    '''
        actualizar el stock actual para la justificación indicada
    '''
    def updateJustificationStock(self,con,userId,justId,stock):
        cur = con.cursor()
        cur.execute('''
          SELECT user_id,justification_id
          FROM assistance.justifications_stock
          WHERE user_id = %s AND justification_id = %s;
        ''',(userId,justId))

        if cur.rowcount <= 0:
            cur.execute('''
                INSERT INTO assistance.justifications_stock (user_id, justification_id, stock, calculated)
                VALUES (%s,%s,%s,now())
            ''',(userId,justId,stock))
        else:
            cur.execute('''
                UPDATE assistance.justifications_stock
                SET stock = %s, calculated = now()
                WHERE user_id = %s AND justification_id = %s
            ''',(stock,userId,justId))

        events = []
        e = {
          'type':'JustificationsStockUpdatedEvent',
          'data':{
             'justificationId':justId,
             'userId':userId,
             'stock':stock
           }
        }
        events.append(e)

        return events






    '''
        retorna el stock actual para la justificación indicada
    '''
    def getJustificationStock(self,con,userId,justId,date,period=None):


        for j in self.justifications:
            if j.isJustification(justId):
                return j.available(self,con,userId,date,period)

        ''' justificationes desconocidas = 0 '''
        return 0


    '''
        cambia el estado de un pedido al nuevo estado especificado por status.
        retorna los eventos a ser disparados
        estados posibles a cambiar : PENDING|APPROVED|REJECTED|CANCELED
    '''
    def updateJustificationRequestStatus(self,con,userId,requestId,status):

        req = self.findJustificationRequestById(con,requestId)
        if req is None:
            raise JustificationError('No existe ningún pedido de justificación con id = %s'.format(requestId))

        for j in self.justifications:
            if j.isJustification(req['justification_id']):
                return j.updateJustificationRequestStatus(self,con,userId,req,status)

        raise JustificationError('No se puede encontrar ese tipo de justificación')



    '''
        realiza el pedido de justificación para ser aprobado
    '''
    def requestJustification(self,con,userId,requestor_id,justificationId,begin,end=None):


        for j in self.justifications:
            if j.isJustification(justificationId):
                return j.requestJustification(self,con,userId,requestor_id,begin,end)

        raise JustificationError('No se puede encontrar ese tipo de justificación')



    def requestGeneralJustification(self, con, justificationId, begin):
      jid = str(uuid.uuid4())
      cur = con.cursor()
      cur.execute('set timezone to %s',('UTC',))
      cur.execute('insert into assistance.general_justifications (id,justification_id,jbegin) values (%s,%s,%s)',(jid,justificationId,begin))

      events = []
      e = {
        'type':'JustificationsRequestsUpdatedEvent',
        'data':{
           'justification_id':justificationId,
         }
      }
      events.append(e)

      return events

    def requestGeneralJustificationRange(self, con, justificationId, begin, end):
      date = begin
      diff = (end-begin).days
      events = []

      # incremento en 1 para que tome el ultimo dia
      for x in range(0, diff + 1):
        events.extend(self.requestGeneralJustification(con,justificationId,date))
        date = date + datetime.timedelta(days=1)

      return events


    def deleteGeneralJustificationRequest(self, con, requestId):
      cur = con.cursor()
      sql = "DELETE FROM assistance.general_justifications WHERE id = '" + requestId + "'"
      cur.execute(sql)

      events = []
      e = {
        'type':'JustificationsRequestsDeletedEvent',
        'data':{
           'request_id':requestId,
         }
      }
      events.append(e)

      return events





    '''
        realiza el pedido de justificación para ser aprobado entre un rango de fechas
        estado inicial del pedido = PENDING, con la fecha actual del servidor.
    '''
    def requestJustificationRange(self,con,userId,requestor_id,justificationId,begin,end):

        events = []
        for j in self.justifications:
            if j.isJustification(justificationId): #and (j.__class__.__name__ == 'LAOJustification' or j.__class__.__name__  == 'R638Justification'):
                date = begin
                diff = (end-begin).days
                # incremento en 1 para que tome el ultimo dia
                for x in range(0, diff + 1):
                    events.extend(j.requestJustification(self,con,userId,requestor_id,date,None))
                    date = date + datetime.timedelta(days=1)

                return events

        raise JustificationError('No se puede encontrar ese tipo de justificación')
