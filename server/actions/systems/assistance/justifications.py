# -*- coding: utf-8 -*-
import json, base64, datetime, traceback, logging
import inject, re
import psycopg2

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
        bossesIds = self.offices.getUsersWithRoleInOffices(con,officesIds,role='autoriza')


        logging.debug('oficinas {}\nids {}\n jefes {}'.format(offices,officesIds,bossesIds))

        for bid,sendMail in bossesIds:
            if sendMail:
                logging.debug('buscando mail para : {}'.format(bid))
                bemails = self.users.listMails(con,bid)
                if bemails != None and len(bemails) > 0:
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
  action:"getJustificationRequestsToManageByDate",
  session:,
  request:{
      status: 'estado de la justificacion PENDING|APPROVED|REJECTED|CANCELED' -- si no existe se obtienen todas,
      start: 'fecha de inicio de la busqueda'
      end: 'fecha limite de busqueda'
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

class GetJustificationRequestsToManageByDate:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    justifications = inject.attr(Justifications)

    def handleAction(self, server, message):

        if (message['action'] != 'getJustificationRequestsToManageByDate'):
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

            start = None
            if 'start' in message['request']:
                start = message['request']['start']

            end = None
            if 'end' in message['request']:
                end = message['request']['end']

            requests = self.justifications.getJustificationRequestsToManageByDate(con,userId,status,group,start,end)

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

            logging.debug('llamando a notify')
            self.notifier.notifyBosses(con,userId,'justifications_update_request_status')


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


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            events = self.justifications.requestJustification(con,userId,justificationId,begin,end)
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
