# -*- coding: utf-8 -*-
import json, base64, traceback, logging
import inject, psycopg2
import pytz, datetime
import dateutil.parser

from wexceptions import *

from model.config import Config
from model.profiles import Profiles
from model.utils import DateTimeEncoder

from model.systems.assistance.logs import Logs
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.date import Date






"""
query :
{
  id:,
  action:"getAssistanceStatus",
  session:,
  request:{
      user_id: "id del usuario"
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
      status: 'estado del agente ',
      start: "fecha y hora de inicio para el dia actual",
      end: "fecha y hora fin para el dia actual",
      logs: [ date1, date2, date3, .... ]       // son todas las marcaciones en bruto del dia actual
      workedMinutes: 'minutos trabajados dentro del dia actual'
  }

}
"""


class GetAssistanceStatus:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)

    def handleAction(self, server, message):

        if (message['action'] != 'getAssistanceStatus'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            status = assistance.getAssistanceStatus(con,message['request']['user_id'])

            response = {
                'id':message['id'],
                'ok':'',
                'response':status
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            con.rollback()
            raise e

        finally:
            con.close()


"""

{
  id:,
  action:"getAssistanceData",
  session:,
  request:{
    user_id: "id del usuario",
    date: "fecha a consultar" -- en caso de que no exista consulta el día actual.
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
      position: 'cargo de la persona',
  	  schedule:[
    		{
    	       start: "fecha y hora de inicio del turno",
    		   end: "fecha y hora de fin de turno"
    		}
  	  ]
  }

}

"""

class GetAssistanceData:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    schedule = inject.attr(Schedule)
    dateutils = inject.attr(Date)


    """ todas las fechas deben ser tratadas en UTC dentro del sistema """
    def adjustTimeZone(self,request):

        date = datetime.datetime.now()
        if 'date' in request:
            date = dateutil.parser.parse(request['date'])

        """ asumo que es fecha local si no vino con tzinfo, no se hace corrección de horario """
        if self.dateutils.isNaive(date):
            date = date.replace(tzinfo=dateutil.tz.tzlocal())

        utcDate = date.astimezone(pytz.utc)
        return utcDate





    def handleAction(self, server, message):

        if (message['action'] != 'getAssistanceData'):
            return False

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True


        """ precondiciones del request """
        request = message['request']

        if 'user_id' not in request:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        userId = request['user_id']

        date = self.adjustTimeZone(request)

        """
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN','USER'])
        """

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            schedule = self.schedule.getSchedule(con,userId,date)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'position':'prueba',
                    'schedule':schedule
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()
