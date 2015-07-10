# -*- coding: utf-8 -*-
import json, base64, traceback, logging
import inject, psycopg2
import pytz, datetime
import dateutil.parser

from model.exceptions import *

from model.config import Config
from model.profiles import Profiles
from model.utils import DateTimeEncoder
from model.events import Events

from model.systems.assistance.assistance import Assistance
from model.systems.assistance.fails import Fails
from model.systems.assistance.logs import Logs
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.check.checks import ScheduleChecks
from model.systems.offices.offices import Offices
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
    checks = inject.attr(ScheduleChecks)

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
            start = start.replace(microsecond=0)
            end = self.dateutils.parse(message['request']['end'])

            logging.debug('fecha de inicio {} y fin {}'.format(start,end))

            authorizedUsers = [userId]

            userIds = self.checks.getUsersWithConstraints(con)
            logging.debug('usuarios con chequeos : %s',(userIds,))

            offices = self.offices.getOfficesByUserRole(con,userId,tree=True,role='autoriza')
            if offices is not None and len(offices) > 0:
                logging.debug('officinas que autoriza : %s',(offices,))

                officesIds = list(map(lambda x : x['id'], offices))
                ousersIds = self.offices.getOfficesUsers(con,officesIds)
                logging.debug('usuarios en las oficinas : %s',(ousersIds,))

                if ousersIds is not None and len(ousersIds) > 0:
                    authorizedUsers.extend(list(filter(lambda x : x in ousersIds, userIds)))

            logging.debug('usuarios que se pueden autorizar : %s',(authorizedUsers,))


            assistanceFails = []
            (users,fails) = self.assistance.checkSchedule(authorizedUsers,start,end)

            # filteredFails = list(filter(lambda x: len(x['justifications']) <= 0,fails))
            b64 = self.assistance.arrangeCheckSchedule(con,fails)

            for user in users:
                ffails = self.fails.filterUser(user['id'],fails)
                for f in ffails:
                    #solo agrego las que no tienen justificaciones
                    '''
                    if ('justifications' not in f) or (len(f['justifications']) <= 0):
                        data = {
                            'user':user,
                            'fail':f
                        }
                        assistanceFails.append(data)
                    '''
                    data = {
                        'user':user,
                        'fail':f
                    }
                    assistanceFails.append(data)


            response = {
                'id':message['id'],
                'ok':'',
                'response':assistanceFails,
                'base64':b64
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
      dates: "fechas a buscar",
      status:[]
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  base64:'response en formato base64',
  response:[{
          userId: id del usuario consultado,
          status: 'estado del agente',
          start: "fecha y hora de inicio para el dia actual",
          end: "fecha y hora fin para el dia actual",
          logs: [ date1, date2, date3, .... ]       // son todas las marcaciones en bruto del dia actual
          workedMinutes: 'minutos trabajados dentro del dia actual'
        }]

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

        status = None
        if 'status' in message['request']:
            status = message['request']['status']
            status = status.split('|')

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            usersIds = message['request']['usersIds']
            dates = message['request']['dates']

            resp = self.assistance.getAssistanceStatusByUsers(con,usersIds,dates,status)
            b64 = self.assistance.arrangeAssistanceStatusByUsers(con,resp)

            response = {
                'id':message['id'],
                'ok':'',
                'base64':b64,
                'response':resp
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



"""

{
  id:,
  action:"getSchedules",
  session:,
  request:{
    user_id: "id del usuario",
    date:"date(opcional, si no le pasa retorna todos)"
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
  	  schedule:[
    		{
    	       start: "fecha y hora de inicio del turno",
    		   end: "fecha y hora de fin de turno",
               isDayOfWeek:,
               isDayOfMonth:,
               isDayOfYear:
    		}
  	  ]
  }

}

"""

class GetSchedules:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    schedule = inject.attr(Schedule)
    positions = inject.attr(Positions)
    dateutils = inject.attr(Date)




    def handleAction(self, server, message):

        if (message['action'] != 'getSchedules'):
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


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            date = None
            if 'date' in request:
                date = self.dateutils.parse(request['date'])
                # verifico que este en formato local
                if self.dateutils.isNaive(date) or self.dateutils.isUTC(date):
                    date = self.dateutils.localizeAwareToLocal(date)
                # le seteo la hora al inicio del dia
                date = date.replace(hour=0,minute=0,second=0,microsecond=0)

                schedule = self.schedule.getSchedulesOfWeek(con,userId,date)
            else:
                schedule = self.schedule.getSchedulesHistory(con,userId)


            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'userId': userId,
                    'schedule':schedule
                }
            }
            server.sendMessage(response)
            return True

        except Exception as e:
            raise e

        finally:
            con.close()


"""
{
    id:'',
    action:"newSchedule",
    session:,
    request:{
        user_id:"id del Usuario",
        date:"fecha de que se empieza a utilizar el schedule, si no se envia se toma la fecha actual",
        start:"hora de inicio del turno",
        end:"hora de fin de turno",
        daysOfWeek:[],
        isDayOfWeek:"es dia de la semana, si no se envia se toma como false",
        isDayOfMonth:"es dia un dia del mes, si no se envia se toma como false",
        isDayOfYear:"es dia del año, si no se envia se toma como false"
    }
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
}
"""

class NewSchedule:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    schedule = inject.attr(Schedule)
    offices = inject.attr(Offices)
    dateutils = inject.attr(Date)

    def getDate(self,day,date):
        # date.weekday=Monday is 0 and Sunday is 6.
        weekday = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        # Monday is 0 and Sunday is 6.
        dateWeek = date.weekday()

        dayWeek = None;
        for x in range(0, 6):
            if (day == weekday[x]):
                dayWeek = x;
                break;

        # calculo la cantidad de dias a incrementar
        inc = (dayWeek - dateWeek) if (dateWeek <= dayWeek) else ((7 - dateWeek) + dayWeek);

        date += datetime.timedelta(days=inc)
        return date

    def handleAction(self, server, message):

        if (message['action'] != 'newSchedule'):
            return False

        if 'request' not in message:
            response = {'id':message['id'],'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        """ precondiciones del request """
        request = message['request']

        if 'user_id' not in request:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True
        userId = request['user_id']

        if 'start' not in request or 'end' not in request:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        start = self.dateutils.parse(request['start'])
        end = self.dateutils.parse(request['end'])

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])


        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            # verifico que el usuario logueado pueda modificar los datos para el usuario user_id
            exist = False
            session_user_id = self.profiles.getLocalUserId(sid)
            users = self.offices.getUserInOfficesByRole(con,session_user_id,True,'autoriza')
            if users != None and len(users) > 0:
                for u in users:
                    if u == userId:
                        exist = True

            if not exist:
                response = {'id':message['id'], 'error':'No tiene permisos para modificar el horario'}
                server.sendMessage(response)
                return True

            # seteo el isDayOfWeek
            if 'isDayOfWeek' not in request:
                isDayOfWeek = False
            else:
                isDayOfWeek = request['isDayOfWeek']

            # seteo el isDayOfMonth
            if 'isDayOfMonth' not in request:
                isDayOfMonth = False
            else:
                isDayOfMonth = request['isDayOfMonth']

            # seteo el isDayOfYear
            if 'isDayOfYear' not in request:
                isDayOfYear = False
            else:
                isDayOfYear = request['isDayOfYear']


            if 'date' not in request:
                date = self.dateutils.now()
            else:
                date = self.dateutils.parse(request['date'])

            # lo paso a formato local
            if self.dateutils.isNaive(date) or self.dateutils.isUTC(date):
                date = self.dateutils.localizeAwareToLocal(date)

            if self.dateutils.isNaive(start) or self.dateutils.isUTC(start):
                start = self.dateutils.localizeAwareToLocal(start)

            if self.dateutils.isNaive(end) or self.dateutils.isUTC(end):
                end = self.dateutils.localizeAwareToLocal(end)

            # seteo el date a las 00:00:00
            date = date.replace(hour=0,minute=0,second=0,microsecond=0)

            # fechas a agregar
            dates = []

            if isDayOfWeek:
                # si no se le envia los dias de la semana devuelvo error
                if 'daysOfWeek' not in request or len(request['daysOfWeek'])<= 0:
                    response = {'id':message['id'], 'error':'Parámetros insuficientes'}
                    server.sendMessage(response)
                    return True

                # obtengo las fechas correspondiente al dia de la semana a partir del date

                daysOfWeek = request['daysOfWeek']

                for day in daysOfWeek:
                    dates.append(self.getDate(day,date))

            else:
                dates.append(date);

            for d in dates:
                # seteo el start
                dStart = d.replace(hour=start.time().hour,minute=start.time().minute,second=0,microsecond=0)

                # seteo el end
                dEnd = d.replace(hour=end.time().hour,minute=end.time().minute,second=0,microsecond=0)

                self.schedule.newSchedule(con,userId,d,dStart,dEnd,isDayOfWeek,isDayOfMonth,isDayOfYear)

            con.commit()
            response = {'id':message['id'], 'ok':'datos almacenados correctamente'}
            server.sendMessage(response)
            return True


        except Exception as e:
            con.rollback()
            raise e

        finally:
            con.close()


"""
{
    id:'',
    action:"deleteSchedule",
    session:,
    request:{
        schedule_id:"id del Usuario"
    }
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
}
"""
class DeleteSchedule:
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    schedule = inject.attr(Schedule)

    def handleAction(self, server, message):

        if message['action'] != 'deleteSchedule':
            return False

        if 'request' not in message or 'schedule_id' not in message['request']:
            response = {'id':message['id'],'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            self.schedule.deleteSchedule(con,message['request']['schedule_id'])
            con.commit()
            response = {'id':message['id'], 'ok':'datos almacenados correctamente'}
            server.sendMessage(response)
            return True

        except Exception as e:
            con.rollback()
            raise e

        finally:
            con.close()


"""
peticion:
{
	"id":"",
	"action":"getPosition",
	"session":"session de usuario",
	"request":{
         userId: identificacion del usuario
     }
}

respuesta:
{
	"id":"id de la peticion",
	"ok":"",
	"error":""
	response:{
  	  position: Cargo del usuario
  	  userId: Id del usuario
    }
}

"""

class GetPosition:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    positions = inject.attr(Positions)


    """ manejar accion """
    def handleAction(self, server, message):

        if (message['action'] != 'getPosition'):
            return False

        #chequear parametros
        if ('id' not in message) or ('session' not in message) or ('request' not in message) or ('userId' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        #chequear permisos
        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        """ definir datos """
        userId = message['request']['userId']

        """ definir conexión con la base de datos """
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            """ consultar datos """
            positions = self.positions.find(con,userId)
            position = None
            if len(positions) > 0:
               position = positions[0]['name']

            """ enviar mensaje de respuesta """
            response = {
               'id':message['id'],
               'ok':'',
               'response':{
                   'userId': userId,
                   'position':position
               }
            }
            server.sendMessage(response)

        except Exception as e:
            logging.exception(e)
            con.rollback()

            response = {
              'id':message['id'],
              'error':'Error realizando la consulta'
            }
            server.sendMessage(response)

        finally:
            con.close()
            return True



'''
query :
{
  id:,
  action:"updatePosition",
  session:,
  request:{
      userId: "id del usuario",
      position: "cargo del usuario"
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
  }

}

'''
class UpdatePosition:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    positions = inject.attr(Positions)
    events = inject.attr(Events)

    def handleAction(self, server, message):

        if (message['action'] != 'updatePosition'):
            return False

        if ('request' not in message) or ('session' not in message) or ('userId' not in message['request']) or ('position' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        userId = message['request']['userId']
        position = message['request']['position']
        sid = message['session']

        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])


        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            """ insertar datos """
            events = self.positions.update(con,userId,position)
            con.commit()

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'userId':userId,
                    'position':position,
                }
            }
            server.sendMessage(response)

            """ disparar eventos """
            for e in events:
                self.events.broadcast(server,e)

        except psycopg2.DatabaseError as e:
            logging.exception(e)
            con.rollback()

            response = {
                'id':message['id'],
                'error':'Error actualizando cargo'
            }
            server.sendMessage(response)

        finally:
            con.close()
