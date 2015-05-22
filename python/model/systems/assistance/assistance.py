# -*- coding: utf-8 -*-
import json, base64, psycopg2, datetime, traceback, logging, sys, uuid
import inject
import datetime
import itertools
from collections import OrderedDict
import io
from pyexcel_ods3 import ODSWriter

from model.utils import DateTimeEncoder
from model.config import Config
from model.users.users import Users

from model.systems.assistance.fails import Fails
from model.systems.assistance.logs import Logs
from model.systems.assistance.date import Date
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.justifications.justifications import Justifications

class Assistance:

    config = inject.attr(Config)
    date = inject.attr(Date)
    logs = inject.attr(Logs)
    schedule = inject.attr(Schedule)
    users = inject.attr(Users)
    justifications = inject.attr(Justifications)



    """
        Obtiene el estado de asistencia del usuario
        IMPORANTE!!!
        la fecha se toma como aware y en zona local del cliente!!!
        se pasa a utc dentro de este método ya que se necesita saber el inicio del día y fin del día en zona local.
    """
    def getAssistanceStatus(self,con,userId,date=None):
        if date is None:
            date = self.date.now()

        if self.date.isNaive(date) or self.date.isUTC(date):
            date = self.date.localizeLocal(date)

        """ el cero y el fin del día son de la zona local """
        From = date.replace(hour=0,minute=0,second=0,microsecond=0)
        To = date.replace(hour=23,minute=59,second=59,microsecond=0)


        From = self.date.awareToUtc(From)
        To = self.date.awareToUtc(To)

        logging.debug('from: {}, to: {}'.format(From,To))

        # Chequeo que tenga horario
        scheds = self.schedule.getSchedule(con,userId,From)
        if (scheds is None) or (len(scheds) <= 0):
            """ no tiene horario declarado asi que no se chequea nada """
            return None

        logs = self.logs.findLogs(con,userId,From,To)
        logging.debug('logs {}'.format(logs))

        worked, attlogs = self.logs.getWorkedHours(logs)
        logging.debug('worked : {}, attlogs: {}'.format(worked,attlogs))

        sdate,edate,totalSeconds = self.logs.explainWorkedHours(worked)
        inside = 'Afuera' if len(attlogs) % 2 == 0 else 'Trabajando'

        assistanceStatus = {
            'date':date,
            'userId': userId,
            'status': inside,
            'start': sdate,
            'end': edate,
            'logs': attlogs,
            'justifications':[],
            'workedMinutes': totalSeconds / 60
        }
        return assistanceStatus






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
    /////////////////////////////////////////////////////
    """


    def _equalsTime(self,d1,d2):
        d1Aux = self.date.awareToUtc(d1)
        d1Aux = d1Aux.replace(hour=0, minute=0, second=0, microsecond=0)
        d2Aux = d2.replace(hour=0, minute=0, second=0, microsecond=0)
        return d1Aux == d2Aux



    def _resolveJustificationsNames(self,con,justifications):
        for j in justifications:
            jid = j['justification_id']
            j['name'] = self.justifications.getJustificationById(con,jid)['name']


    """
        Obtiene los estados de asistencia de los usuarios entre las fechas pasadas
    """
    def getAssistanceStatusByUsers(self,con,usersIds,dates,status):
        resp = []
        if (dates == None or len(dates) <= 0):
            return resp


        start = dates[0]
        end = dates[len(dates) - 1]
        # obtengo las justificaciones
        justifications = self.justifications.getJustificationRequestsByDate(con,status,usersIds,start,end)

        dstart = self.date.parse(start)
        dend = self.date.parse(end)
        gjustifications = self.justifications.getGeneralJustifications(con)
        for j in gjustifications:
            if j['begin'] >= dstart and j['begin'] <= dend:
                for uid in usersIds:
                    jnew = dict(j)
                    jnew['user_id'] = uid
                    justifications.append(jnew)


        self._resolveJustificationsNames(con,justifications)

        for userId in usersIds:
            for d in dates:
                date = self.date.parse(d)

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
                self._resolveJustificationsNames(con,l['justifications'])
                for j in l['justifications']:
                    v.append(j['name'])
            else:
                v.append('')

            values.append(v)

        return values


    def arrangeCheckSchedule(self, con, data):
        odata = self._arrangeForOdsChecks(con,data)
        return self._exportToOds(odata)


    """
        chequea el schedule de los usuarios pasados como parametro.
        las fechas start y end son aware
    """
    def checkSchedule(self, userIds, start, end):

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            if self.date.isNaive(start):
                start = self.date.localizeLocal(start)

            if self.date.isNaive(end):
                end = self.date.localizeLocal(end)

            schedulesFails = []
            users = []
            for u in userIds:
                logging.debug('chequeando usuario %s',(u,))
                users.append(self.users.findUser(con,u))
                schedulesFails.extend(self.schedule.checkConstraints(con,u,start,end))

            return (users,schedulesFails)

        finally:
            con.close()



    """
        chequea el schedule de los usuarios.
        las fechas start y end son aware
    """
    """
    def checkSchedule(self, start, end):

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            if self.date.isNaive(start):
                start = self.date.localizeLocal(start)

            if self.date.isNaive(end):
                end = self.date.localizeLocal(end)


            schedulesFails = []
            userIds = self.schedule.getUsersWithConstraints(con)

            users = []
            for u in userIds:
                users.append(self.users.findUser(con,u))

            delta = end - start

            if delta.days <= 0:
                for userId in userIds:
                    fails = self.schedule.checkSchedule(con,userId,start)
                    if fails is None or len(fails) <= 0:
                        continue
                    schedulesFails.extend(fails)
                return (users,schedulesFails)


            for i in range(delta.days + 1):
                date = start + datetime.timedelta(days=i)
                for userId in userIds:
                    fails = self.schedule.checkSchedule(con,userId,date)
                    if fails is None or len(fails) <= 0:
                        continue

                    schedulesFails.extend(fails)

            return (users,schedulesFails)

        finally:
            con.close()
    """



    """
        chequea el schedule de las personas que tienen algún schedule para chequear
        y envía mail en caso de que falle
    def checkSchedule(self):

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            userIds = self.schedule.getUsersInSchedules(con)
            logging.debug('users: {}'.format(userIds))


            dateIni = date = self.date.now() - datetime.timedelta(days=1)
            dateFin = date = self.date.now() + datetime.timedelta(days=1)
            delta = dateFin - dateIni
            for i in range(delta.days):
                date = dateIni + datetime.timedelta(days=i)

                start = date.replace(hour=0,minute=0,second=0,microsecond=0)
                end = start + datetime.timedelta(days=1)
                #end = date.replace(hour=23,minute=59,second=59,microsecond=0)

                ustart = self.date.awareToUtc(start)
                uend = self.date.awareToUtc(end)


                out = open('/tmp/fallas/' + str(date) + '.csv','w')

                for userId in userIds:
                    user = self.users.findUser(con,userId)

                    logs = self.logs.findLogs(con,userId,ustart,uend)
                    whs,attlogs = self.logs.getWorkedHours(logs)
                    userId,fails = self.schedule.checkSchedule(con,userId,ustart,uend,whs)

                    for fail in fails:
                        localDate = self.date.localizeAwareToLocal(fail['date']).replace(hour=0,minute=0,second=0,microsecond=0)
                        f = '{0},{1},{2},{3},{4},{5},{6},{7},{8}'.format(
                            localDate.date(),
                            user['dni'],
                            user['name'],
                            user['lastname'],
                            fail['description'],
                            self.date.localizeAwareToLocal(fail['start']).time() if 'start' in fail else (self.date.localizeAwareToLocal(fail['end']).time() if 'end' in fail else 'no tiene'),
                            self.date.localizeAwareToLocal(fail['startSchedule']).time() if 'startSchedule' in fail else (self.date.localizeAwareToLocal(fail['endSchedule']).time() if 'endSchedule' in fail else 'no tiene'),
                            fail['minutes'] if 'minutes' in fail else '',
                            fail['minutes']-datetime.timedelta(minutes=15) if 'minutes' in fail else '')
                        out.write(f)
                        out.write('\n')

                out.close()


        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()
    """



if __name__ == '__main__':

    if len(sys.argv) < 3:
        logging.warn('llamar el script con la fecha de inicio del chequeo y la de fin del chequeo')
        sys.exit(1)


    def config_injector(binder):
        binder.bind(Config,Config('server-config.cfg'))


    logging.basicConfig(level=logging.DEBUG)
    inject.configure(config_injector)
    config = inject.instance(Config)

    dateutils = inject.instance(Date)

    start = dateutils.parse(sys.argv[1])
    end = dateutils.parse(sys.argv[2])

    logging.info('\n\nChequeando schedule en {} --> {}'.format(start,end))

    assistance = inject.instance(Assistance)
    (users,sfails) = assistance.checkSchedule(start,end)

    logging.info("\n\n\n")

    fails = inject.instance(Fails)
    fails.toCsv('/tmp/p.csv',users,sfails)
