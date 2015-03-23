# -*- coding: utf-8 -*-
import json, base64, psycopg2, datetime, traceback, logging
import inject
from wexceptions import MalformedMessage
from model.profiles import AccessDenied
from model.utils import DateTimeEncoder
from model.config import Config
from model.users import Users

from model.systems.assistance.logs import Logs
from model.systems.assistance.date import Date

class Asssistance:

    date = inject.attr(Date)
    logs = inject.attr(Logs)

    """ http://stackoverflow.com/questions/4998427/how-to-group-elements-in-python-by-n-elements """
    def _grouper(n, iterable, fillvalue=None):
        "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)


    """ a partir de una lista de datetime obtiene los grupos de worked """
    def _getWorkedTimetable(self, dateList):
        worked = []
        bytwo = _grouper(2,dateList)
        for b in bytwo:
            w = { 'start':b[0], 'end':b[1], 'minutes':(b[1]-b[0]).total_seconds() }
            worked.append(w)
        return worked


    """ obtiene el estado de asistencia del dia actual del usuario """
    def getAssistanceStatus(self,con,userId):
        date = self.date.utcNow()
        logs = self.logs.findLogs(con,userId,date)

        attlogs = map(lambda e : e['date'] , logs)
        inside = len(attlogs) % 2
        worked = self._getWorkedTimetable(attlogs);
        sdate = worked[0]['start']
        edate = worked[-1]['end']
        totalMinutes = 0
        for w in worked:
            totalMinutes = totalMinutes + w['minutes']

        assistanceStatus = {
            'status': inside,
            'start': sdate,
            'end': edate,
            'logs': attlogs,
            'workedMinutes': totalMinutes
        }
        return assistanceStatus


    """ obtiene tods los schedules para un usuario en determinada fecha, solo deja los actuales, tiene en cuenta el historial ordenado por date """
    def getAssistanceData(self,con,userId,date):

        cur = con.cursor()
        cur.execute('select name from assistance.positions where user_id = %s',(userId,))
        position = cur.fetchone()

        """ obtengo todos los schedules que son en la fecha date del parámetro """
        cur.execute("select sstart, send, date from assistance.schedule where \
                    ((date = %s) or \
                    (isDayOfWeek = true and extract(dow from date) = extract(dow from %s)) or \
                    (isDayOfMonth = true and extract(dom from date) = extract(dom from %s)) or \
                    (isDayOfYear = true and extract(doy from date) = extract(doy from %s))) and \
                    user_id = %s \
                    order by date desc",(date,date,date,date,userId))
        scheduless = cur.fetchall()
        schedules = []
        dateS = None
        for schedule in scheduless:
            dateS = schedule[2] if dateS == None else dateS
            if schedule[2] == dateS:
                schedules.append({'start':schedule[0], 'end':schedule[1]})
            else:
                break

        data = {
            'position': position[0] if position != None else 'no tiene definida',
            'schedule': schedules
        }
        return data


    """ obtiene todas las oficinas """
    def getOffices(self,con):
        cur = con.cursor()
        cur.execute('select id,parent,name from assistance.offices')
        offs = cur.fetchall()
        offices = []
        for off in offs:
            offices.append({'id':off[0],'parent':off[1],'name':off[2]})
        return offices


    """ obtiene todas las oficinas a las que pertenece un usuario y si tree=True obtiene todas las hijas también """
    def getOfficesByUser(self,con,tree=False):
        cur = con.cursor()
        cur.execute('select id,parent,name from assistance.offices o, assistance.offices_users ou where ou.user_id = %s and o.id = ou.office_id')
        offs = cur.fetchall()

        offices = []
        ids = []
        for off in offs:
            oId = off[0]
            ids.append(oId)
            offices.append({'id':oId,'parent':off[1],'name':off[2]})


        if tree:
            """ obtengo todo el arbol de oficinas abajo de las actuales """
            pids = []
            pids.extends(ids)

            while len(pids) > 0:
                toFollow = []
                toFollow.extend(pids)
                pids = []

                for oId in toFollow:
                    cur.execute('select id,parent,name from asssitance.offices where parent = %s',(oId,))
                    cOffs = cur.fetchall()
                    for cOff in cOffs:
                        cId = off[0]
                        if cId not in ids:
                            offices.append({'id':cId,'parent':cOff[1],'name':cOff[2]})
                            pids.append(cId)


        return offices


    """ obtiene todas las justificaciones """
    def getJustificationStock(self,con,userId,justId):
        cur = con.cursor()
        cur.execute('select id,name from assistance.justifications')
        justs = cur.fetchall()
        justifications = []
        for just in justs:
            justifications.append({'id':just[0],'name':just[1]})
        return justifications


    """ retorna el stock total de la justificacion indicada """
    def getJustificationStock(self,con,userId,justId):
        cur = con.cursor()
        cur.execute('select quantity from assistance.justifications_stock where user_id = %s and justification_id = %s',(userId,justId))
        stock = cur.fetchone()
        if stock = None:
            return None
        s = {'quantity':stock[0]}
        return s



    """ retorna el stock actual posible de tomarse para la justificación indicada """
    def getJustificationActualStock(self,con,userId,justId,date):

        """
        ('e0dfcef6-98bb-4624-ae6c-960657a9a741','Ausente con aviso')
        ('48773fd7-8502-4079-8ad5-963618abe725','Compensatorio')
        ('fa64fdbd-31b0-42ab-af83-818b3cbecf46','Boleta de Salida')
        ('4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb','Art 102')
        ('b70013e3-389a-46d4-8b98-8e4ab75335d0','Pre-Exámen')
        ('76bc064a-e8bf-4aa3-9f51-a3c4483a729a','Licencia Anual Ordinaria')
        ('50998530-10dd-4d68-8b4a-a4b7a87f3972','Resolución')
        """

        restrictions = [
            AARestriction(), BSRestriction(), CRestriction()
        ]

        for r in restrictions:
            if r.isJustification(justId):
                return r.available(self,con,userId,)

        """ si no existe ninguna restricción sobre la justificación entonces se retorna el stock """
        stock = assistance.getJustificationStock(con,userId,justId)
        if stock = None:
            return 0

        jstock = stock['quantity']
        if jstock <= 0:
            return 0
        else:
            return jstock





    """
    obtiene todas los pedidos de justificaciones.
    los parámetros son opcionales y definen el filtro a usar para obtener
    """
    def getJustificationRequests(self,con,userId=None,justificationId=None,state=None):
        cur = con.cursor()

        if userId = None and justificationId = None and state = None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests')

        if userId != None and justificationId = None and state = None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where user_id = %s',(userId,))

        elif userId != None and justificationId != None and state = None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where user_id = %s and justification_id = %s',(userId,justificationId))

        elif userId != None and justificationId = None and state != None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where user_id = %s and state = %s',(userId,state))

        elif userId != None and justificationId != None and state != None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where user_id = %s and state = %s and justificationId = %s',(userId,state,justificationId))

        elif userId = None and justificationId != None and state = None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where justification_id = %s',(justificationId,))

        elif userId = None and justificationId != None and state != None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where justification_id = %s and state = %s',(justificationId,state))

        elif userId = None and  justificationId = None and state != None
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where state = %s',(state,))


        req = cur.fetchall()
        requests = []
        for r in req:
            requests.append(
                {
                    'justification_id':req[2],
                    'begin':req[3],
                    'end':req[4],
                    'state':req[5]
                }
            )

        return requests



    """ realiza el pedido de justificación para ser aprobado """
    def requestJustification(self,con,userId,req):


        """ aca se deben chequear todos los parametros para ver si es posible realizar el pedido """


        cur = con.cursor()
        jid = str(uuid.uuid4())
        rreq = (jid,userId,req['justificationId'],req['begin'],req['end'],'PENDING')
        cur.execute('insert into assistance.justifications_request (id,user_id,justification_id,jbegin,jend,status) values (%s,%s,%s,%s,%s,%s)',rreq)
