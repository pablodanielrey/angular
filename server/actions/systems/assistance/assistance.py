# -*- coding: utf-8 -*-
import json, base64, traceback, logging
import inject, psycopg2
import pytz, datetime
import dateutil.parser

from model.exceptions import *

from model.config import Config
from model.profiles import Profiles
from model.utils import DateTimeEncoder

from model.systems.assistance.assistance import Assistance
from model.systems.assistance.fails import Fails
from model.systems.assistance.logs import Logs
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.offices import Offices
from model.systems.assistance.positions import Positions
from model.systems.assistance.date import Date



"""
query :
{
  id:,
  action:"getFailsByDate",
  session:,
  request:{
      start: "fecha de inicio"
      end: 'fecha de fin'
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{[
      user: 'datos del usuario ',
      fail: "datos correspondiente a la falla"
  ]}

}
"""

class GetFailsByDate:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    assistance = inject.attr(Assistance)
    fails = inject.attr(Fails)
    dateutils = inject.attr(Date)

    offices = inject.attr(Offices)
    schedule = inject.attr(Schedule)




    def _filterJustificationsByUser(self,justifications,userId):
        result = []
        for j in justifications:
            if j['user_id'] == userId:
                result.append(j)
        return result



    def handleAction(self, server, message):

        if(message['action'] != 'getFailsByDate'):
            return False

        if ('request' not in message) or ('start' not in message['request']) or 'end' not in message['request']:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])
        userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            start = self.dateutils.parse(message['request']['start'])
            end = self.dateutils.parse(message['request']['end'])

            logging.debug('fecha de inicio {} y fin {}'.format(start,end))

            userIds = self.schedule.getUsersWithConstraints(con)
            logging.debug('usuarios con chequeos : %s',(userIds,))
            offices = self.offices.getOfficesByUserRole(con,userId,tree=True,role='autoriza')
            logging.debug('officinas que autoriza : %s',(offices,))
            officesIds = list(map(lambda x : x['id'], offices))
            ousersIds = self.offices.getOfficesUsers(con,officesIds)
            logging.debug('usuarios en las oficinas : %s',(ousersIds,))
            authorizedUsers = list(filter(lambda x : x in ousersIds, userIds))
            logging.debug('usuarios que se pueden autorizar : %s',(authorizedUsers,))


            assistanceFails = []
            (users,fails,justifications) = self.assistance.checkSchedule(authorizedUsers,start,end)


            for user in users:
                ffails = self.fails.filterUser(user['id'],fails)
                jjust = self._filterJustificationsByUser(justifications,user['id'])
                for f in ffails:
                    f['date'] = self.dateutils.localizeAwareToLocal(f['date']);
                    data = {
                        'user':user,
                        'fail':f,
                        'justification': jjust
                    }
                    assistanceFails.append(data)

            response = {
                'id':message['id'],
                'ok':'',
                'response':assistanceFails
            }
            server.sendMessage(response)
            return True

        except Exception as e:
            logging.exception(e)
            raise e

        finally:
            con.close()


"""
query :
{
  id:,
  action:"getAssistanceStatus",
  session:,
  request:{
      user_id: "id del usuario"
      date: 'fecha opcional' -- si no se brinda entonces se obteiene la info del día actual.
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
    assistance = inject.attr(Assistance)
    date = inject.attr(Date)

    def handleAction(self, server, message):

        if (message['action'] != 'getAssistanceStatus'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            userId = message['request']['user_id']

            date = None
            if 'date' in message['request']:
                date = self.date.parse(message['request']['date'])

            status = self.assistance.getAssistanceStatus(con,userId,date)

            response = {
                'id':message['id'],
                'ok':'',
                'response':status
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()

"""
query :
{
  id:,
  action:"getAssistanceStatusByUsers",
  session:,
  request:{
      usersIds: "listado de ids de los usuarios a buscar",
      dates: "fechas a buscar"
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{[
      userId: id del usuario consultado,
      status: 'estado del agente',
      start: "fecha y hora de inicio para el dia actual",
      end: "fecha y hora fin para el dia actual",
      logs: [ date1, date2, date3, .... ]       // son todas las marcaciones en bruto del dia actual
      workedMinutes: 'minutos trabajados dentro del dia actual'
  ]}

}
"""


class GetAssistanceStatusByUsers:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    assistance = inject.attr(Assistance)
    date = inject.attr(Date)

    def handleAction(self, server, message):

        if (message['action'] != 'getAssistanceStatusByUsers'):
            return False

        if ('request' not in message) or ('usersIds' not in message['request']) or ('dates' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            usersIds = message['request']['usersIds']
            dates = message['request']['dates']

            status = []
            for userId in usersIds:
                for d in dates:
                    date = self.date.parse(d)
                    s = self.assistance.getAssistanceStatus(con,userId,date)
                    status.append(s)

            response = {
                'id':message['id'],
                'ok':'',
                'response':status
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
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
    positions = inject.attr(Positions)
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

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            positions = self.positions.find(con,userId)
            position = ''
            if len(positions) > 0:
                position = positions[0]['name']

            schedule = self.schedule.getSchedule(con,userId,date)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'userId': userId,
                    'position':position,
                    'schedule':schedule
                }
            }
            server.sendMessage(response)
            return True

        except Exception as e:
            raise e

        finally:
            con.close()
