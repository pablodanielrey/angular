# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid
import inject

from model.systems.assistance.date import Date
from model.systems.assistance.logs import Logs

from model.systems.assistance.justifications.exceptions import *

from model.systems.offices.offices import Offices

from model.systems.assistance.justifications.AAJustification import AAJustification
from model.systems.assistance.justifications.BSJustification import BSJustification
from model.systems.assistance.justifications.CJustification import CJustification
from model.systems.assistance.justifications.LAOJustification import LAOJustification

from model.systems.assistance.schedule import Schedule

class Overtime:

    offices = inject.attr(Offices)
    date = inject.attr(Date)
    schedule = inject.attr(Schedule)
    logs = inject.attr(Logs)


    """
        obtiene el ultimo estado del pedido de horas extras indicado por reqId
    """
    def _getOvertimeRequestStatus(self,con,reqId):
        cur = con.cursor()
        cur.execute('select jrs.status from assistance.overtime_requests_status as jrs, (select request_id,max(created) as created from assistance.overtime_requests_status group by request_id) as r where r.created = jrs.created and r.request_id = jrs.request_id')
        if cur.rowcount <= 0:
            return None

        return cur.fetchone()[0]


    """
        obtiene todas los pedidos de horas extras que estan como ultimo estado en la lista de estados pasada como parametro.
        status = una lista de estados posibles.
        retora un dict con los ids como key y el estado como value
        { id: status }
    """
    def _getOvertimesInStatus(self,con,status=[]):

        cur = con.cursor()
        if status is None or len(status) <= 0:
            cur.execute('select jrs.request_id,jrs.status from assistance.overtime_requests_status as jrs, (select request_id,max(created) as created from assistance.overtime_requests_status group by request_id) as r where r.created = jrs.created and r.request_id = jrs.request_id')
        else:
            cur.execute('select jrs.request_id,jrs.status from assistance.overtime_requests_status as jrs, (select request_id,max(created) as created from assistance.overtime_requests_status group by request_id) as r where r.created = jrs.created and r.request_id = jrs.request_id and jrs.status in %s',(tuple(status),))

        if cur.rowcount <= 0:
            return {}

        statusR = {}
        for rs in cur:
            statusR[rs[0]] = rs[1]

        return statusR



    '''
    Definir horas extras trabajadas para una determinada fecha
    @param con Conexion con la base de datos
    @param userId Identificacion de usuario
    @param date Fecha para la cual se quiere calcular el tiempo extra trabajado
    '''
    def getWorkedOvertime(self, con, userId, date):

        t = datetime.time(hour=0, minute=0, second=0)
        dateStart = datetime.datetime.combine(date, t)

        dateEnd = date.replace(hour=23, minute=59, second=59)

        print("**************************************** date")
        print(date)
        print(dateStart)
        print(dateEnd)
        print("****************************************")

        #calcular overtimes del dia
        overtimeRequests = self.getOvertimeRequests(con, ['APPROVED'], None, [userId], dateStart, dateEnd)

        print("**************************************** overtime")
        for overtime in overtimeRequests:
             print(overtime)

        print("****************************************")

        #definir fecha inicial del ultimo schedule del dia anterior
        schedulesPre = None
        dateAux = dateStart
        print("**************************************** dateAux")
        while schedulesPre is None or len(schedulesPre) == 0:
            dateAux = dateAux - datetime.timedelta(days = 1)
            print(dateAux)
            schedulesPre = self.schedule.getSchedule(con, userId, dateAux)
        print("****************************************")

        datePre = schedulesPre[-1]["start"]


        print("**************************************** schedulesPre")
        for sch in schedulesPre:
            print(sch)
        print("****************************************")


        #definir fecha final del ultimo schedule del dia siguiente
        schedulesPos = None
        dateAux = dateStart
        while schedulesPos is None or len(schedulesPos) == 0:
            dateAux = dateAux + datetime.timedelta(days = 1)
            schedulesPos = self.schedule.getSchedule(con, userId, dateAux)
        datePos = schedulesPos[-1]["end"]


        print("**************************************** schedulesPos")
        for sch in schedulesPos:
            print(sch)
        print("****************************************")


        print("**************************************** datePre datePos")
        print(datePre)
        print(datePos)
        print("****************************************")

        #obtener worked hours en base a las fechas definidas de los schedules anterior y posterior
        logs = self.logs.findLogs(con, userId, datePre, datePos)
        (workedHours, attlogs) = self.logs.getWorkedHours(logs)

        print("**************************************** workedHours")
        for wh in workedHours:
             print(wh)

        print("****************************************")

        for o in overtimeRequests:
            for wh in workedHours:
                if wh["end"] is None or wh["start"] is None or o["end"] is None or o["begin"] is None:
                    return 0
                if wh["end"] <= o["end"] and wh["end"] >= o["begin"]:
                   print("calcular y sumar minutos")
                elif wh["start"] <= o["begin"] and wh["end"] >= o["end"]:
                   print("calcular y sumar minutos")
                elif wh["start"] >= o["begin"] and wh["start"] <= o["end"]:
                   print("calcular y sumar minutos")
                else:
                   print("no sera calculado")







    def getOvertimeRequests(self, con, status=[], requestors=None, users=None, begin=None, end=None):

        """
            obtiene todas los pedidos de horas extras con cierto estado
            status es el estado a obtener. en el caso de que no sea pasado entonces se obtienen todas, en su ultimo estado
            users es una lista de ids de usuarios para los que se piden los requests, si = None o es vacío entonces retorna todas.
            requestors es una lista de ids de usuarios que piden los requests, si = None o es vacío entonces no se toma en cuenta.
        """

        statusR = self._getOvertimesInStatus(con,status)
        #logging.debug('in status = {} req {}'.format(status,statusR))
        if len(statusR) <= 0:
            return []

        ids = tuple(statusR.keys())
        params = (ids, )

        sql = "select id,user_id,requestor_id,jbegin,jend,reason from assistance.overtime_requests where id in %s"


        if users is not None and len(users) > 0:
            users = tuple(users)
            params = params + (users, )
            sql += " AND user_id IN %s"

        if requestors is not None and len(requestors) > 0:
            requestors = tuple(requestors)
            params = params + (requestors, )
            sql += " AND requestor_id in %s"

        if begin is not None:
            params = params + (begin, )
            sql += " AND jbegin >= %s"

        if end is not None:
            params = params + (end, )
            sql += " AND jend <= %s"

        sql += ";"


        cur = con.cursor()
        cur.execute(sql, params)


        if cur.rowcount <= 0:
            return []

        requests = []
        for j in cur:
            jid = j[0]
            requests.append(
                {
                    'id':jid,
                    'user_id':j[1],
                    'requestor_id':j[2],
                    'begin':j[3],
                    'end':j[4],
                    'reason':j[5],
                    'status':statusR[jid]
                }
            )

        return requests

        return []


    """
        obtiene todos los pedidos de horas extras que tiene permisos de manejar, en cierto estado.
        group = ROOT|TREE --> ROOT = oficinas directas, TREE = oficinas directas y todas las hijas
    """
    def getOvertimeRequestsToManage(self,con,userId,status,group='ROOT'):

        tree = False
        if group == 'TREE':
            tree = True
        offices = self.offices.getOfficesByUserRole(con,userId,tree,'horas-extras')
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

        overtimes = self.getOvertimeRequests(con,status,users=users)

        return overtimes



    """
        cambia el estado de un pedido al nuevo estado especificado por status.
        retorna los eventos a ser disparados
        estados posibles a cambiar : PENDING|APPROVED|REJECTED|CANCELED
    """
    def updateOvertimeRequestStatus(self,con,userId,requestId,status):

        cur = con.cursor()
        cur.execute('insert into assistance.overtime_requests_status (request_id,user_id,status) values (%s,%s,%s)',(requestId,userId,status))

        events = []
        e = {
            'type':'OvertimeStatusChangedEvent',
            'data':{
                'overtime_id':requestId,
                'user_id':userId,
                'status':status
            }
        }
        events.append(e)
        return events



    """
        realiza el pedido de horas extras para ser aprobado
        estado inicial del pedido = PENDING, con la fecha actual del servidor.
    """
    def requestOvertime(self,con,requestorId,userId,begin,end,reason):

        oid = str(uuid.uuid4())
        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into assistance.overtime_requests (id,requestor_id,user_id,jbegin,jend,reason) values (%s,%s,%s,%s,%s,%s)',(oid,requestorId,userId,begin,end,reason))

        events = []
        e = {
            'type':'OvertimesUpdatedEvent',
            'data':{
                'overtime_id': oid,
                'user_id':userId,
                'requestor_id':requestorId
            }
        }
        events.append(e)
        events.extend(self.updateOvertimeRequestStatus(con,requestorId,oid,'PENDING'))

        return events
