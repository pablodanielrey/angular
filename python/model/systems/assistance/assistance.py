# -*- coding: utf-8 -*-
import sys
import base64
import psycopg2
import datetime
import logging
import uuid
import inject
import datetime
import itertools
from collections import OrderedDict
import io
from pyexcel_ods3 import ODSWriter

from model.systems.offices.offices import Offices
from model.utils import DateTimeEncoder
from model.config import Config
from model.users.users import Users

from model.systems.assistance.fails import Fails
from model.systems.assistance.logs import Logs
from model.systems.assistance.date import Date
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.check.checks import ScheduleChecks
from model.systems.assistance.justifications.justifications import Justifications
from model.systems.positions.positions import Positions
import model.systems.assistance.date


class Assistance:

    config = inject.attr(Config)
    offices = inject.attr(Offices)
    date = inject.attr(Date)
    logs = inject.attr(Logs)
    schedule = inject.attr(Schedule)
    users = inject.attr(Users)
    justifications = inject.attr(Justifications)
    checks = inject.attr(ScheduleChecks)
    positions = inject.attr(Positions)
    date = inject.attr(model.systems.assistance.date.Date)


    """
    //////////////////////////////////////////////////
    //////////////
    ////////////// codigo para exportar a ods los resultados
    //////////////
    //////////////////////////////////////////////////
    """

    def _exportToOds(self,data):
        ods = OrderedDict()
        ods.update({"Datos": data})
        filename = '/tmp/{}.tmp'.format(str(uuid.uuid4()))
        writer = ODSWriter(filename)
        writer.write(ods)
        writer.close()

        b64 = ''
        with open(filename,'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')

        return b64

    def _equalsTime(self,d1,d2):
        d1Aux = self.date.awareToUtc(d1)
        d1Aux = d1Aux.replace(hour=0, minute=0, second=0, microsecond=0)
        d2Aux = d2.replace(hour=0, minute=0, second=0, microsecond=0)
        return d1Aux == d2Aux


    def _arrangeForOdsAssistanceStatus(self, con, data):

        values = [['Fecha','Dni','Nombre','Apellido','Hora de Entrada','Hora de Salida','Cantidad de Horas','Justificación']]
        for l in data:
            v = []

            userId = l['userId']
            user = self.users.findUser(con,userId)

            v.append(l['date'].astimezone(tz=None).date())
            v.append(user['dni'])
            v.append(user['name'])
            v.append(user['lastname'])

            if l['start'] != None and l['start'] != '':
                v.append(l['start'].astimezone(tz=None).time())
            else:
                v.append('')

            if l['end'] != None and l['end'] != '':
                v.append(l['end'].astimezone(tz=None).time())
            else:
                v.append('')

            v.append('{:02d}:{:02d}'.format(int(l['workedMinutes'] / 60), int(l['workedMinutes'] % 60)))

            if l['justifications'] != None and len(l['justifications']) > 0:
                jname = l['justifications'][0]['name']
                v.append(jname)
            else:
                v.append('')

            values.append(v)

        return values


    def arrangeAssistanceStatusByUsers(self, con, data):
        odata = self._arrangeForOdsAssistanceStatus(con,data)
        return self._exportToOds(odata)



    """
       Obtener datos de asistencia, los datos de asistencia consisten en el cargo (position) y schedule (horario)
       @param con Conexion con la base de datos
       @param userId Identificacion de usuario
       @param date Fecha de consulta de los datos de asistencia. Por defecto now()
    """
    def getAssistanceData(self, con, userId, date=None):
        ps = self.positions.find(con, userId)
        p = ''
        if len(ps) > 0:
            p = ps[0]['name']

        if date is None:
            date = datetime.datetime.now()
        if self.date.isNaive(date):
            ldate = self.date.localizeLocal(date)
            date = self.date.awareToUtc(ldate)


        sch = self.schedule.getSchedule(con, userId, date.date())

        rt = {
            'userId': userId,
            'schedule': sch,
            'position': p
        }
        return rt

    def _resolveJustificationsNames(self, con, justifications):
        for j in justifications:
            jid = j['justification_id']
            j['name'] = self.justifications.getJustificationById(con, jid)['name']




    def _getJustificationsForSchedule(self, con, userId, scheds, date):
        """
            Obtener justificaciones de un usuario a partir de una fecha
            @param con Conexion con la base de datos
            @param userId Identificacion de usuario
            @param scheds Lista de schedules
            @param date Fecha para la cual se obtendran las justificaciones
        """

        if scheds is None or len(scheds) <= 0:
            return []

        start = scheds[0].getStart(date)
        end = scheds[-1].getEnd(date)
        justifications = self.justifications.getJustificationRequestsByDate(con, None, [userId], start, end)
        self._resolveJustificationsNames(con, justifications)
        return justifications


    """
        Obtiene el estado de asistencia del usuario para cierta fecha: El estado de asistencia incluye las justificaciones, los logs, los minutos trabajados, el esatdo (si se encuentra trabajando o no)
        @param con Conexion con la base de datos
        @param userId Identificacion de usuario
        @param date Fecha de consulta del estado de asistencia. Por defecto now(). IMPORTANTE: La fecha se toma como aware y en zona local del cliente! Se pasa a utc dentro de este metodo ya que se necesita saber el inicio del día y fin del día en zona local.
    """
    def getAssistanceStatus(self, con, userId, date=None):
        if date is None:
            date = datetime.datetime.now()
        if self.date.isNaive(date):
            date = self.date.localizeLocal(date)

        # Chequeo que tenga horario
        scheds = self.schedule.getSchedule(con, userId, date.date())
        if (scheds is None) or (len(scheds) <= 0):
            """ no tiene horario declarado asi que no se chequea nada """
            return None

        logs = self.schedule.getLogsForSchedule(con, scheds, date.date())
        logging.debug('logs {}'.format(logs))

        worked, attlogs = self.logs.getWorkedHours(logs)
        logging.debug('worked : {}, attlogs: {}'.format(worked, attlogs))

        sdate, edate, totalSeconds = self.logs.explainWorkedHours(worked)
        inside = 'Afuera' if len(attlogs) % 2 == 0 else 'Trabajando'

        justifications = self._getJustificationsForSchedule(con, userId, scheds,date)

        assistanceStatus = {
            'date': date,
            'userId': userId,
            'status': inside,
            'start': sdate,
            'end': edate,
            'logs': attlogs,
            'justifications': justifications,
            # comente esto para que me funcione, todavia no se quien utiliza el scheds
            # 'schedules': scheds,
            'workedMinutes': totalSeconds / 60
        }
        return assistanceStatus



    def _getNullAssistanceStatus(self, con, userId, date):
        scheds = self.schedule.getSchedule(con, userId, date.date())
        justifications = self._getJustificationsForSchedule(con, userId, scheds,date)
        assistanceStatus = {
            'date': date,
            'userId': userId,
            'status': 'Afuera',
            'start': None,
            'end': None,
            'logs': [],
            'justifications': justifications,
            'schedules': scheds,
            'workedMinutes': 0
        }
        return assistanceStatus


    '''
    Codigo anterior, lo reemplace por el otro del mismo nombre
    def getAssistanceStatusByUsers(self, con, usersIds, dates):
        statuses = {}
        for userId in usersIds:
            sts = []
            for date in dates:
                st = self.getAssistanceStatus(con, userId, date)
                if st is not None:
                    sts.append(st)
                else:
                    st = self._getNullAssistanceStatus(con, userId, date)
                    sts.append(st)
            statuses[userId] = sts
        return statuses
    '''

    '''
        Obtiene los estados de asistencia de los usuarios entre las fechas pasadas
    '''

    def getAssistanceStatusByUsers(self,con,usersIds,dates,status):
        resp = []
        if (dates == None or len(dates) <= 0):
            return resp

        dstart = dates[0]

        # dend = self.date.parse(dates[len(dates) -1]) + datetime.timedelta(days=1)
        dend = dates[-1] + datetime.timedelta(days=1)

        # obtengo las justificaciones
        justifications = self.justifications.getJustificationRequestsByDate(con,status,usersIds,dstart,dend)


        gjustifications = self.justifications.getGeneralJustificationRequests(con)
        for j in gjustifications:
            if j['begin'] >= dstart and j['begin'] <= dend:
                for uid in usersIds:
                    jnew = dict(j)
                    jnew['user_id'] = uid
                    justifications.append(jnew)


        self._resolveJustificationsNames(con,justifications)


        for userId in usersIds:
            for date in dates:
                s = self.getAssistanceStatus(con,userId,date)
                if (s != None):
                    # verifico si coincide alguna justificacion con el userId y el date
                    just = list(filter(lambda j: j['user_id'] == userId and self._equalsTime(j["begin"],date), justifications))
                    s["justifications"] = just;
                    for j in just:
                        justifications.remove(j)
                    resp.append(s)

        # falta agrupar las justificaciones que quedaron
        # creo un assistance status por cada justificacion que quedaron sin matchear
        for j in justifications:
            a = {
                'date':j['begin'],
                'userId': j['user_id'],
                'status': "",
                'start': None,
                'end': None,
                'logs': [],
                'justifications':[j],
                'workedMinutes': 0
            }
            resp.append(a)

        return resp


    """
        ////////////////////////////////////////// chequeo del tema de incumplimientos ////////////////////
    """

    def _arrangeForOdsChecks(self, con, data):

        values = [['Fecha','Dni','Nombre','Apellido','Hora Declarada','Hora de Marcación','Diferencia','Descripción','Horas Trabajadas','Justificación']]
        for l in data:
            v = []

            userId = l['userId']
            user = self.users.findUser(con,userId)

            v.append(l['date'].astimezone(tz=None).date())
            v.append(user['dni'])
            v.append(user['name'])
            v.append(user['lastname'])

            if 'startSchedule' in l:
                v.append(l['startSchedule'].astimezone(tz=None).time())
            elif 'endSchedule' in l:
                v.append(l['endSchedule'].astimezone(tz=None).time())
            else:
                v.append('')

            if 'start' in l:
                v.append(l['start'].astimezone(tz=None).time())
            elif 'end' in l:
                v.append(l['end'].astimezone(tz=None).time())
            else:
                v.append('')

            if 'seconds' in l:
                v.append('{:02d}:{:02d}'.format(int(l['seconds'] / 60 / 60), int(l['seconds'] / 60 % 60)))
            else:
                v.append('')

            v.append(l['description'])

            if 'whSeconds' in l:
                v.append('{:02d}:{:02d}'.format(int(l['whSeconds'] / 60 / 60), int(l['whSeconds'] / 60 % 60)))
            else:
                v.append('')

            if 'justifications' in l:
                self._resolveJustificationsNames(con, l['justifications'])
                for j in l['justifications']:
                    v.append(j['name'])
            else:
                v.append('')

            values.append(v)

        return values

    def arrangeCheckSchedule(self, con, data):
        odata = self._arrangeForOdsChecks(con, data)
        return self._exportToOds(odata)




    """
        Obtiene las fallas que tenga el usuario en el rango de fechas correspondientes al Schedule
        @param userId Identificacion de usuario
        @param start Fecha (date) de inicio del periodo
        @param end Fecha (date de finalizacion del periodo
    """
    def getFailsByDate(self, con, userId, start, end):
        offices = self.offices.getOfficesByUserRole(con,userId,True,'autoriza')
        #logging.debug('officesByUserRole : {}'.format(offices))

        if offices is None or len(offices) <= 0:
            return []

        officesIds = list(map(lambda o: o['id'], offices))
        users = self.offices.getOfficesUsers(con,officesIds)
        fails = []
        for userId in users:
            fails = self.checks.checkConstraints(con, userId, start, end) #obtener fallas del usuario en determinado periodo
            user = self.users.findUser(con, userId) #definir usuario
            f = (user, fails)
            fails.append(f)
        return fails
