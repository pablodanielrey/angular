# -*- coding: utf-8 -*-
import json, base64, datetime, traceback, logging
import inject, re
import psycopg2
import time

from model.exceptions import *

from model.config import Config
from model.profiles import Profiles
from model.events import Events
from model.users.users import Users
from model.mail.mail import Mail

from model.systems.assistance.assistance import Assistance
from model.systems.assistance.date import Date
from model.systems.assistance.justifications.justifications import Justifications
from model.systems.assistance.offices import Offices



class BossesNotifier:

    config = inject.attr(Config)
    date = inject.attr(Date)
    events = inject.attr(Events)
    mail = inject.attr(Mail)
    users = inject.attr(Users)
    offices = inject.attr(Offices)

    def _sendEmail(self, Tos, config, request):

        """
            variables a reemplazar :
            ###NAME###
            ###LASTNAME###
        """

        From = self.config.configs['{}_from'.format(config)]
        subject = self.config.configs['{}_subject'.format(config)]
        template = self.config.configs['{}_template'.format(config)]

        subject = re.sub('###NAME###', request['name'], subject)
        subject = re.sub('###LASTNAME###', request['lastname'], subject)

        replace = [
            ('###NAME###',request['name']),
            ('###LASTNAME###',request['lastname'])
        ]

        self.mail.sendMail(From,Tos,subject,replace,html=template)




    """
        notifica a los jefes y al usuario de un pedido.
        solo a los que tienen configurado que debería enviarles mails.
    """
    def notifyBosses(self,con,userId,config):

        emails = []

        logging.debug('notifyBosses')

        uemails = self.users.listMails(con,userId)
        if uemails != None and len(uemails) > 0:
            emails.extend(list(map(lambda x: x['email'],uemails)))

        logging.debug('emails {}'.format(emails))

        user = self.users.findUser(con,userId)
        request = {
            'name': user['name'],
            'lastname': user['lastname']
        }

        offices = self.offices.getOfficesByUser(con,userId,parents=True)
        officesIds = list(map(lambda x: x['id'], offices))

        if officesIds is not None and len(officesIds) > 0:
            bossesIds = self.offices.getUsersWithRoleInOffices(con,officesIds,role='autoriza')
            logging.debug('oficinas {}\nids {}\n jefes {}'.format(offices,officesIds,bossesIds))

            for bid,sendMail in bossesIds:
                if sendMail:
                    logging.debug('buscando mail para : {}'.format(bid))
                    bemails = self.users.listMails(con,bid)
                    if bemails != None and len(bemails) > 0:
                        bemails = list(filter(lambda x: 'econo.unlp.edu.ar' in x['email'],bemails))
                        logging.debug('añadiendo {}'.format(bemails))
                        emails.extend(list(map(lambda x: x['email'],bemails)))

        logging.debug('emails {}'.format(emails))

        if len(emails) > 0:
            self._sendEmail(emails,config,request)









"""

query :
{
  id:,
  action:"getJustifications",
  session:
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    justifications: [
      {
        id: 'id de la justificacion',
        name: 'nombre de la justificacion'
      }
    ]
  }

}
"""


class GetJustifications:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)

    def handleAction(self, server, message):

        if (message['action'] != 'getJustifications'):
            return False

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            justs = self.justifications.getJustifications(con)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'justifications':justs
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            con.rollback()
            raise e

        finally:
            con.close()







"""
query :
{
  id:,
  action:"getJustificationStock",
  session:,
  request:{
      user_id: "id del usuario",
      justification_id: "id de la justificación"
      date: 'fecha a consultar'    -- opcional. si no se pasa etnonces se toma la fecha actual.
      period: 'MONTH|YEAR'         -- opcional. período en el cual se analiza la consulta. si no se pasa se analizan todos. el stock es el minimo de todos.
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    justificationId: 'id de la justificación'
    count: "cantidad de justificaciones disponibles de ese tipo"
  }

}

"""

class GetJustificationStock:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)
    date = inject.attr(Date)

    def handleAction(self, server, message):

        if (message['action'] != 'getJustificationStock'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']) or ('justification_id' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        userId = message['request']['user_id']
        justificationId = message['request']['justification_id']

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            date = self.date.utcNow()
            if 'date' in message['request']:
                date = self.date.parse(message['request']['date'])

            period = None
            if 'period' in message['request']:
                period = message['request']['period']

                if period != 'WEEK' and period != 'MONTH' and period != 'YEAR':
                    response = {'id':message['id'], 'error':'período no válido'}
                    server.sendMessage(response)
                    return True


            stock = self.justifications.getJustificationStock(con,userId,justificationId,date,period)
            if stock == None:
                response = {'id':message['id'], 'error':'No existe stock para esa justificación'}
                server.sendMessage(response)
                return True

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'justificationId':justificationId,
                    'stock':stock
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()





"""
query : Obtener todas las solicitudes de justificationces
{
  id:,
  action:"getJustificationRequestsToManage",
  session:,
  request:{
      status: 'estado de la justificacion PENDING|APPROVED|REJECTED|CANCELED' -- si no existe se obtienen todas,
      group: "ROOT|TREE" -- si no existe obtiene las del grupo directo que puede manejar.
  }
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    requests : [ "lista de solicitudes de un determinado usuario"
  		{
        id: "id de la solicitud de justificacion",
        user_id:"id del usuario",
    		justification_id: "id de la justificacion o licencia solicitada"
    		begin: 2014-12-01 00:00:00 "fecha de inicio de la justificacion o licencia solicitada"
    		end: 2014-12-02 00:00:00 "fecha de finalizacion de la justificacion o licencia solicitada"
    		status: "PENDING|APPROVED|REJECTED|CANCELED"
  		}
	]

}
"""

class GetJustificationRequestsToManage:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)

    def handleAction(self, server, message):

        if (message['action'] != 'getJustificationRequestsToManage'):
            return False

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        status = None
        if 'status' in message['request']:
            status = message['request']['status']

        group = None
        if 'group' in message['request']:
            group = message['request']['group']


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            requests = self.justifications.getJustificationRequestsToManage(con,userId,status,group)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'requests':requests
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()





"""
query : Obtener todas las solicitudes de justificationces
{
  id:,
  action:"getJustificationRequestsByDate",
  session:,
  request:{
      status: 'estado de la justificacion PENDING|APPROVED|REJECTED|CANCELED' -- si no existe se obtienen todas,
      start: 'fecha de inicio de la busqueda'
      end: 'fecha limite de busqueda'
      usersIds: 'ids de usuarios'
  }
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    requests : [ "lista de solicitudes de un determinado usuario"
  		{
        id: "id de la solicitud de justificacion",
        user_id:"id del usuario",
    		justification_id: "id de la justificacion o licencia solicitada"
    		begin: 2014-12-01 00:00:00 "fecha de inicio de la justificacion o licencia solicitada"
    		end: 2014-12-02 00:00:00 "fecha de finalizacion de la justificacion o licencia solicitada"
    		status: "PENDING|APPROVED|REJECTED|CANCELED"
  		}
	]

}
"""
class GetJustificationRequestsByDate:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)

    def handleAction(self, server, message):

        if (message['action'] != 'getJustificationRequestsByDate'):
            return False

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        if 'usersIds' not in message['request']:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        status = None
        if 'status' in message['request']:
            status = message['request']['status']
            status = status.split('|')



        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        userId = self.profiles.getLocalUserId(sid)

        usersIds = message['request']['usersIds']



        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:

            start = None
            if 'start' in message['request']:
                start = message['request']['start']

            end = None
            if 'end' in message['request']:
                end = message['request']['end']

            requests = []
            if len(usersIds) > 0:
                requests = self.justifications.getJustificationRequestsByDate(con,status,usersIds,start,end)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'requests':requests
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()


"""

query : Obtener todas las solicitudes de justificationces
{
  id:,
  action:"getJustificationRequests",
  session:,
  request:{
      status: 'estado de la justificacion PENDING|APPROVED|REJECTED|CANCELED' -- si no existe se obtienen todas,
  }
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    requests : [ "lista de solicitudes de un determinado usuario"
  		{
        id: "id de la solicitud de justificacion",
        user_id:"id del usuario",
    		justification_id: "id de la justificacion o licencia solicitada"
    		begin: 2014-12-01 00:00:00 "fecha de inicio de la justificacion o licencia solicitada"
    		end: 2014-12-02 00:00:00 "fecha de finalizacion de la justificacion o licencia solicitada"
    		status: "PENDING|APPROVED|REJECTED|CANCELED"
  		}
	]

}
"""
class GetJustificationRequests:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)

    def handleAction(self, server, message):

        if (message['action'] != 'getJustificationRequests'):
            return False

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        status = None
        if 'status' in message['request']:
            status = message['request']['status']


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            requests = self.justifications.getJustificationRequests(con,status,[userId])

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'requests':requests
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()






"""
query : solicitud de justificaciones de un determinado usuario
{
  id:,
  action:"updateJustificationRequestStatus",
  session:,
  request:{
      request_id: "id del pedido",
      status: "PENDING|APPROVED|REJECTED|CANCELED"
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor"
}

"""
class UpdateJustificationRequestStatus:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)
    date = inject.attr(Date)
    events = inject.attr(Events)
    notifier = inject.attr(BossesNotifier)


    def handleAction(self, server, message):

        if (message['action'] != 'updateJustificationRequestStatus'):
            return False

        if ('session' not in message) or ('request' not in message) or ('request_id' not in message['request']) or ('status' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        requestId = message['request']['request_id']
        status = message['request']['status']

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])
        userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            events = self.justifications.updateJustificationRequestStatus(con,userId,requestId,status)
            con.commit()

            """ se debe notificar a los jefes del usuaro del pedido original """
            req = self.justifications.findJustificationRequestById(con,requestId)
            if req['user_id'] is not None:
                self.notifier.notifyBosses(con,req['user_id'],'justifications_update_request_status')


            response = {
                'id':message['id'],
                'ok':'El cambio se ha realizado correctamente'
            }
            server.sendMessage(response)

            for e in events:
                self.events.broadcast(server,e)

            return True

        except Exception as e:
            logging.exception(e)
            con.rollback()

            response = {
                'id':message['id'],
                'error':'Error realizando pedido'
            }
            server.sendMessage(response)
            return True

        finally:
            con.close()






"""
query : solicitud de justificaciones de un determinado usuario
{
  id:,
  action:"requestJustification",
  session:,
  request:{
      user_id: "id del usuario",
      justification_id: "id de la justificacion o licencia solicitada"
  	  begin: "fecha de inicio de la justificacion o licencia solicitada"
  	  end: "fecha de finalizacion de la justificacion o licencia solicitada" -- algunas justificaciones no tienen fin. es el turno completo.
      status: estado por defecto de la nueva solicitud -- por defecto PENDING
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor"
}
"""

class RequestJustification:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)
    date = inject.attr(Date)
    events = inject.attr(Events)
    notifier = inject.attr(BossesNotifier)

    def handleAction(self, server, message):

        if (message['action'] != 'requestJustification'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']) or ('justification_id' not in message['request']) or ('begin' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True


        userId = message['request']['user_id']
        justificationId = message['request']['justification_id']
        begin = message['request']['begin']
        begin = self.date.parse(begin)
        end = None
        if 'end' in message['request']:
            end = message['request']['end']
            end = self.date.parse(end)

        status = None
        if 'status' in message['request']:
            status = message['request']['status']


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        requestor_id = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            events = self.justifications.requestJustification(con,userId,requestor_id,justificationId,begin,end)
            con.commit()

            if status != None and status != 'PENDING':
                # obtengo el id del request del evento de updateStatus que tiene por defecto
                reqId = None
                for ev in events:
                    if 'data' in ev and 'request_id' in ev['data']:
                        reqId = ev['data']['request_id']

                if reqId != None:
                    e = self.justifications.updateJustificationRequestStatus(con,requestor_id,reqId,status)
                    events.extend(e)

                con.commit()



            self.notifier.notifyBosses(con,userId,'justifications_request')

            response = {
                'id':message['id'],
                'ok':'El pedido se ha realizado correctamente'
            }
            server.sendMessage(response)

            for e in events:
                self.events.broadcast(server,e)

            return True


        except Exception as e:
            logging.exception(e)
            con.rollback()

            response = {
                'id':message['id'],
                'error':'Error realizando pedido'
            }
            server.sendMessage(response)
            return True

        finally:
            con.close()



"""
peticion:
{
	"id":"",
	"action":"requestGeneralJustification",
	"session":"session de usuario",
	request:{
        justificationId:"id de la justificacion",
        begin:"fecha de inicio"
        end:"fecha de fin" (opcional)
        status: "estado" (opcional)
    }
}

respuesta:
{
	"id":"id de la peticion",
	"ok":"",
	"error":""
}

"""
class RequestGeneralJustification:

  profiles = inject.attr(Profiles)
  config = inject.attr(Config)
  date = inject.attr(Date)
  events = inject.attr(Events)

  justifications = inject.attr(Justifications)



  """ manejar accion """
  def handleAction(self, server, message):



    if (message['action'] != 'requestGeneralJustification'):
        return False

    """ chequeo de datos """
    if ('id' not in message) or ('session' not in message) or ('request' not in message) or ('justification_id' not in message['request']) or ('begin' not in message['request']):
      response = {'id':message['id'], 'error':'Insuficientes parámetros'}
      server.sendMessage(response)
      return True

    """ chequeo de permisos """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

    """ definir datos a insertar """
    justificationId = message['request']['justification_id']
    begin = message['request']['begin']
    begin = self.date.parse(begin)
    end = None
    if 'end' in message['request']:
      end = message['request']['end']
      end = self.date.parse(end)

    """ insertar datos """
    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])

    try:
      events = self.justifications.requestGeneralJustification(con,justificationId,begin)
      con.commit()

      response = {
       'id':message['id'],
       'ok':'El pedido se ha realizado correctamente'
      }
      server.sendMessage(response)

      for e in events:
        self.events.broadcast(server,e)

    except Exception as e:
      logging.exception(e)
      con.rollback()

      response = {
        'id':message['id'],
        'error':'Error realizando pedido'
      }

      server.sendMessage(response)

    finally:
      con.close()
      return True



"""
peticion:
{
	"id":"",
	"action":"deleteGeneralJustificationRequest",
	"session":"session de usuario",
	request:{
    request_id:"id de la justificacionRequest",
  }
}

respuesta:
{
	"id":"id de la peticion",
	"ok":"",
	"error":""
}

"""
class DeleteGeneralJustificationRequest:
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)
  events = inject.attr(Events)

  justifications = inject.attr(Justifications)

  """ manejar accion """
  def handleAction(self, server, message):


    if (message['action'] != 'deleteGeneralJustificationRequest'):
      return False

    """ chequeo de datos """
    if ('id' not in message) or ('session' not in message) or ('request' not in message) or ('request_id' not in message["request"]):
      response = {'id':message['id'], 'error':'Insuficientes parámetros'}
      server.sendMessage(response)
      return True

    """ chequeo de permisos """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

    """ definir datos """
    request_id = message['request']['request_id']

    """ conexion con base de datos """
    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      events = self.justifications.deleteGeneralJustificationRequest(con, request_id)
      con.commit()

      """ enviar mensaje de respuesta """
      response = {
          'id':message['id'],
          'ok':'Solicitud eliminada correctamente',
      }
      server.sendMessage(response)

      """ disparar eventos """
      for e in events:
       self.events.broadcast(server,e)


    except Exception as e:
      logging.exception(e)

      response = {
        'id':message['id'],
        'error':'Error realizando pedido'
      }

      server.sendMessage(response)

    finally:
      con.close()
      return True;

"""
peticion:
{
	"id":"",
	"action":"getGeneralJustificationRequests",
	"session":"session de usuario",

}

respuesta:
{
	"id":"id de la peticion",
	"ok":"",
	"error":""
}

"""
class GetGeneralJustificationRequests:
  profiles = inject.attr(Profiles)
  config = inject.attr(Config)

  justifications = inject.attr(Justifications)

  """ manejar accion """
  def handleAction(self, server, message):


    if (message['action'] != 'getGeneralJustificationRequests'):
        return False

    """ chequeo de datos """
    if ('id' not in message) or ('session' not in message):
      response = {'id':message['id'], 'error':'Insuficientes parámetros'}
      server.sendMessage(response)
      return True

    """ chequeo de permisos """
    sid = message['session']
    self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])


    """ conexion con base de datos """
    con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
    try:
      requests = self.justifications.getGeneralJustificationRequests(con)

      response = {
          'id':message['id'],
          'ok':'',
          'response':{
              'requests':requests
          }
      }
      server.sendMessage(response)


    except Exception as e:
      logging.exception(e)

      response = {
        'id':message['id'],
        'error':'Error realizando pedido'
      }

      server.sendMessage(response)

    finally:
      con.close()
      return True;



"""
query : solicitud de justificaciones de un determinado usuario
{
  id:,
  action:"requestJustificationRange",
  session:,
  request:{
      user_id: "id del usuario",
      justification_id: "id de la justificacion o licencia solicitada"
  	  begin: "fecha de inicio de la justificacion o licencia solicitada"
  	  end: "fecha de finalizacion de la justificacion o licencia solicitada"
      status:estado por defecto de la nueva solicitud -- por defecto PENDING
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor"
}
"""

class RequestJustificationRange:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)
    date = inject.attr(Date)
    events = inject.attr(Events)
    notifier = inject.attr(BossesNotifier)

    def handleAction(self, server, message):

        if (message['action'] != 'requestJustificationRange'):
            return False

        if ('request' not in message) or ('user_id' not in message['request']) or ('justification_id' not in message['request']) or ('begin' not in message['request']) or ('end' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True


        userId = message['request']['user_id']
        justificationId = message['request']['justification_id']
        begin = message['request']['begin']
        begin = self.date.parse(begin)
        end = message['request']['end']
        end = self.date.parse(end)

        status = None
        if 'status' in message['request']:
            status = message['request']['status']


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        requestor_id = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            events = self.justifications.requestJustificationRange(con,userId,requestor_id,justificationId,begin,end)

            con.commit()

            if status != None and status != 'PENDING':
                # obtengo el id del request del evento de updateStatus que tiene por defecto
                reqIds = []
                for ev in events:
                    if 'data' in ev and 'request_id' in ev['data']:
                        reqIds.append(ev['data']['request_id'])

                for reqId in reqIds:
                    e = self.justifications.updateJustificationRequestStatus(con,requestor_id,reqId,status)
                    events.extend(e)

                con.commit()


            self.notifier.notifyBosses(con,userId,'justifications_request')

            response = {
                'id':message['id'],
                'ok':'El pedido se ha realizado correctamente'
            }
            server.sendMessage(response)

            for e in events:
                self.events.broadcast(server,e)

            return True


        except Exception as e:
            logging.exception(e)
            con.rollback()

            response = {
                'id':message['id'],
                'error':'Error realizando pedido'
            }
            server.sendMessage(response)
            return True

        finally:
            con.close()



"""

query : Obtener todas las justificationces especiales que puede solicitar el usuario logueado
{
  id:,
  action:"getSpecialJustifications",
  session:,
  request:{

  }
}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    justifications: [
      {
        id: 'id de la justificacion',
        name:''
      }
    ]

}
"""
class GetSpecialJustifications:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)
    justifications = inject.attr(Justifications)

    def handleAction(self, server, message):

        if (message['action'] != 'getSpecialJustifications'):
            return False

        if 'request' not in message:
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            role = 'realizar-solicitud'
            tree = False
            offices = self.offices.getUserInOfficesByRole(con,userId,tree,role);

            ids = []

            if (offices != None and len(offices) > 0):
                # 'f9baed8a-a803-4d7f-943e-35c436d5db46','Licencia Médica Corta Duración'
                # 'a93d3af3-4079-4e93-a891-91d5d3145155','Licencia Médica Largo Tratamiento'
                # 'b80c8c0e-5311-4ad1-94a7-8d294888d770','Licencia Médica Atención Familiar'
                # '478a2e35-51b8-427a-986e-591a9ee449d8','Justificado por Médico'
                # '0cd276aa-6d6b-4752-abe5-9258dbfd6f09','Duelo'
                # 'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b','Donación de Sangre'
                ids.extend([
                    'f9baed8a-a803-4d7f-943e-35c436d5db46', #medica corta duracion
                    'b80c8c0e-5311-4ad1-94a7-8d294888d770', #medica atencion familiar
                    'a93d3af3-4079-4e93-a891-91d5d3145155', #medica largo tratamiento
                  
                    '478a2e35-51b8-427a-986e-591a9ee449d8', #justificado por medico
                    'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b', #donacion sangre
                    
                    '70e0951f-d378-44fb-9c43-f402cbfc63c8', #ART                    
                    '0cd276aa-6d6b-4752-abe5-9258dbfd6f09', #duelo
                    
                    '30a249d5-f90c-4666-aec6-34c53b62a447', #matrimonio
                    'aa41a39e-c20e-4cc4-942c-febe95569499', #Pre natal
                    '68bf4c98-984d-4b71-98b0-4165c69d62ce', #pos natal
                    'e249bfce-5af3-4d99-8509-9adc2330700b', #nacimiento
                    
                    '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9', #viaje
                    '508a9b3a-e326-4b77-a103-3399cb65f82a', #cursos / capacitacion
                    '5289eac5-9221-4a09-932c-9f1e3d099a47', #concurso
                    
                    '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7', #entrada tarde justificada
                    'c32eb2eb-882b-4905-8e8f-c03405cee727', #justificado por autoridad
                    '1c14a13c-2358-424f-89d3-d639a9404579', #licencia sin goce de sueldo
                    'bfaebb07-8d08-4551-b264-85eb4cab6ef1', #suspensión
                    
                    
                    '5c548eab-b8fc-40be-bb85-ef53d594dca9', #dia del bibliotecario
                    '3d486aa0-745a-4914-a46d-bc559853d367', #incumbencias climaticas
                    
                ])

            role = 'realizar-solicitud-admin'
            offices = self.offices.getUserInOfficesByRole(con,userId,tree,role);
            if (offices != None or len(offices) > 0):
                # por ahora no existe la justificacion "Justificado por autoridad"
                ids.extend([])

            justifications = []
            for idJ in ids:
                justifications.append(self.justifications.getJustificationById(con,idJ))

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'justifications':justifications
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()
