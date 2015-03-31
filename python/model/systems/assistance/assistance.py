# -*- coding: utf-8 -*-
import json, base64, psycopg2, datetime, traceback, logging
import inject
import datetime
import itertools

from wexceptions import *

from model.profiles import AccessDenied
from model.utils import DateTimeEncoder
from model.config import Config
from model.users.users import Users

from model.systems.assistance.logs import Logs
from model.systems.assistance.date import Date
from model.systems.assistance.schedule import Schedule

class Assistance:

    config = inject.attr(Config)
    date = inject.attr(Date)
    logs = inject.attr(Logs)
    schedule = inject.attr(Schedule)
    users = inject.attr(Users)

    """
        Obtiene el estado de asistencia del usuario
        IMPORANTE!!!
        la fecha se toma como aware y en zona local del cliente!!!
        se pasa a utc dentro de este método ya que se necesita saber el inicio del día y fin del día en zona local.
    """
    def getAssistanceStatus(self,con,userId,date=None):
        if date is None:
            date = self.date.now()

        """ el cero y el fin del día son de la zona local """
        From = date.replace(hour=0,minute=0,second=0,microsecond=0)
        To = date.replace(hour=23,minute=59,second=59,microsecond=0)

        From = self.date.awareToUtc(From)
        To = self.date.awareToUtc(To)

        logs = self.logs.findLogs(con,userId,From,To)
        worked, attlogs = self.logs.getWorkedHours(logs)
        sdate,edate,totalSeconds = self.logs.explainWorkedHours(worked)
        inside = 'Afuera' if len(attlogs) % 2 == 0 else 'Trabajando'

        assistanceStatus = {
            'status': inside,
            'start': sdate,
            'end': edate,
            'logs': attlogs,
            'workedMinutes': totalSeconds / 60
        }
        return assistanceStatus


    """
        chequea el schedule de los usuarios.
        las fechas start y end estan en la zona local.
    """
    def checkSchedule(self, start, end):

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            schedulesFails = []

            userIds = self.schedule.getUsersInSchedules(con)
            logging.debug('users: {}'.format(userIds))

            users = []
            for u in userIds:
                users.append(self.users.findUser(con,u))

            delta = end - start
            for i in range(delta.days):
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
