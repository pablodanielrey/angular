# -*- coding: utf-8 -*-
import json, base64, datetime, traceback, logging
import inject
import psycopg2

from model.exceptions import *

from model.config import Config
from model.profiles import Profiles

from model.utils import DateTimeEncoder

from model.systems.offices.offices import Offices



"""
retorna los usuarios que pertenecen a las oficinas y suboficinas en las cuales la persona userId tiene un rol determinado

query:
{
  id:
  action:'getUserInOfficesByRole'
  session:
  request: {
    userId: id del usuario que tiene los roles en las oficinas -- opcional,. si no va se toma el usuario actual de la session
    role: rol a buscar
    tree: False|True -- retorna el arbol o solo las oficinas directas que tienen el rol.
  }
}

response:
{
  id:
  ok:
  error:
  response: {
    users: [
        userId: 'id del usuario'
    ]
  }
}

"""
class GetUserInOfficesByRole:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'getUserInOfficesByRole'):
            return False

        if 'role' not in message['request']:
            raise MalformedMessage()

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        userId = self.profiles.getLocalUserId(sid)
        if 'userId' in message['request']:
            userId = message['request']['userId']

        tree = False
        if 'tree' in message['request']:
            tree = message['request']['tree']

        role = message['request']['role']

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            logging.debug('getUserInOfficesByRole')
            users = self.offices.getUserInOfficesByRole(con,userId,tree,role)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'users':users
                }
            }
            server.sendMessage(response)
            return True

        except Exception as e:
            logging.exception(e)
            raise e

        finally:
            con.close()



'''
Retorna los roles que puede asignar el usuario (userId) para las oficinas (officesId)
query:
{
  id:
  action:'getRolesAdmin'
  session:
  request: {
    userId: 'id del usuario -- opcional, en el caso de no existir se toma el usuario de sesión'
    officesId: []'ids de la oficina'
  }
}

response:
{
  id:
  ok:
  error:
  response: {
    roles: []
  }
}

'''
class GetRolesAdmin:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'getRolesAdmin'):
            return False

        if ('session' not in message) or ('request' not in message) or ('officesId' not in message['request']):
            response = {'id':message['id'], 'error': 'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-OFFICES','USER-OFFICES'])

        req = message['request']
        officesId = req['officesId']

        if 'userId' in req:
            userId = req['userId']
        else:
            userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            roles = self.offices.getRolesAdmin(con, userId, officesId)
            response = {
                'id':message['id'],
                'ok':'',
                'response': {
                    'roles':roles
                }
            }
            server.sendMessage(response)
            return True
        except Exception as e:
            logging.exception(e)
            raise e
        finally:
            con.close()



"""
query:
{
  id:
  action:'getUserOfficeRoles'
  session:
  request: {
    officeId: 'id de la oficina' -- opcional, en el caso de no existir obtiene todos los roles que tenga en las oficinas
  }
}

response:
{
  id:
  ok:
  error:
  response: {
    roles: [
      {
        officeId: 'id de la oficina',
        role: 'rol en la oficina'
      }
    ]
  }
}

"""
class GetUserOfficeRoles:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'getUserOfficeRoles'):
            return False

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])
        userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            roles = self.offices.getOfficesRoles(con,userId)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'roles':roles
                }
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
  action:"getOffices",
  session:,
  request:{
      user_id: "id del usuario" -- opcional. si no existe el parámetro entonces retorna todas las oficinas.
      tree: "True|False" -- obtiene todo el arbol de las oficinas abajo de las que la persona pertenece.
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    offices: [
      {
        id: 'id de la oficina',
        name: 'nombre de la oficina',
        parent: 'id de la oficina padre' -- o no existente en el caso de ser oficina de primer nivel.
      }
    ]
  }

}


"""

class GetOffices:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'getOffices'):
            return False

        userId = None
        if 'request' in message and 'user_id' in message['request']:
            userId = message['request']['user_id']


        tree = False
        if 'request' in message and 'tree' in message['request']:
            tree = message['request']['tree']


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            offices = []
            if userId is not None:
                offices = self.offices.getOfficesByUser(con,userId,tree)
            else:
                offices = self.offices.getOffices(con)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'offices':offices
                }
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
  action:"getOfficesByUserRole",
  session:,
  request:{
      user_id: "id del usuario" -- opcional. si no existe el parámetro entonces retorna todas las oficinas.
      role: "por defecto es administra"
      tree: "True|False" -- obtiene todo el arbol de las oficinas abajo de las que la persona pertenece.
  }

}

response :
{
  id: "id de la petición",
  ok: "caso exito",
  error: "error del servidor",
  response:{
    offices: [
      {
        id: 'id de la oficina',
        name: 'nombre de la oficina',
        parent: 'id de la oficina padre' -- o no existente en el caso de ser oficina de primer nivel.
      }
    ]
  }

}


"""

class GetOfficesByUserRole:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'getOfficesByUserRole'):
            return False

        userId = None
        if 'request' in message and 'user_id' in message['request']:
            userId = message['request']['user_id']

        else:
            response = {'id':message['id'], 'error':'Parámetros insuficientes'}
            server.sendMessage(response)
            return True

        tree = False
        if 'tree' in message['request']:
            tree = message['request']['tree']

        role = 'administra'
        if 'role' in message['request']:
            role = message['request']['role']


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE'])

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            offices = self.offices.getOfficesByUserRole(con,userId,tree,role)

            response = {
                'id':message['id'],
                'ok':'',
                'response':{
                    'offices':offices
                }
            }
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()



"""
retorna los usuarios que pertenecen a las oficinas y suboficinas en las cuales la persona userId tiene un rol determinado

query:
{
  id:
  action:'getOfficesUsers'
  session:
  request: {
    offices:[] lista de ids de oficinas
  }
}

response:
{
  id:
  ok:
  error:
  response: {
    users: [
        userId: 'id del usuario'
    ]
  }
}

"""

class GetOfficesUsers:

    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'getOfficesUsers'):
            return False

        if 'offices' not in message['request']:
            raise MalformedMessage()


        offices = message['request']['offices']
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            users = self.offices.getOfficesUsers(con,offices)

            response = {
                'id':message['id'],
                'ok':'',
                'response': {
                    'users':users
                }
            }
            server.sendMessage(response)
            return True
        except Exception as e:
            logging.exception(e)
            raise e

        finally:
            con.close()


'''
elimina el rol para usuario oficina

query:{
    id:,
    action:'deleteOfficeRole',
    session:,
    request:{
        userId: "id del usuario a eliminar el rol",
        officeId: "id de la oficina de la cual se desea eliminar el rol",
        role: "rol que se desea eliminar"
    }
}

response: {
    id: "id de la petición",
    ok: "caso exito",
    error: "error del servidor"
}

'''

class DeleteOfficeRole:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'deleteOfficeRole'):
            return False

        if ('session' not in message) or ('request' not in message) or ('userId' not in message['request']) or ('role' not in message['request']) or ('officeId' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-OFFICES','USER-OFFICES'])

        req = message['request']
        officeId = req['officeId']
        userId = req['userId']
        role = req['role']

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            # verifico si el usuario de session tiene el rol autoriza para la oficina de la cual se desean eliminar el rol
            localUserId = self.profiles.getLocalUserId(sid)
            offices = self.offices.getOfficesByUserRole(con,localUserId,True,'autoriza')
            listOff = list(map(lambda x: x == officeId, offices))
            if len(listOff) == 0:
                response = {'id':message['id'], 'error':'No tiene permiso para realizar esta operación'}
                server.sendMessage(response)
                return True

            # elimino el rol
            self.offices.deleteRole(con,userId,officeId,role)
            con.commit()
            response = {'id':message['id'], 'ok':'El rol se ha eliminado correctamente'}
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()


'''
setea el rol role al usuario userId para la oficina officeId

query:{
    id:,
    action:'addOfficeRole',
    session:,
    request:{
        userId: "id del usuario",
        officeId: "id de la oficina",
        role: "rol",
        sendMail: ""
    }
}

response: {
    id: "id de la petición",
    ok: "caso exito",
    error: "error del servidor"
}
'''
class AddOfficeRole:
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'addOfficeRole'):
            return False

        if ('session' not in message) or ('request' not in message) or ('userId' not in message['request']) or ('role' not in message['request']) or ('officeId' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-OFFICES','USER-OFFICES'])

        req = message['request']
        officeId = req['officeId']
        userId = req['userId']
        role = req['role']
        sendMail = (True,req['sendMail'])['sendMail' in req]

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            # verifico si el usuario de session tiene el rol autoriza para la oficina de la cual se desea agregar el rol
            localUserId = self.profiles.getLocalUserId(sid)
            offices = self.offices.getOfficesByUserRole(con,localUserId,True,'autoriza')
            listOff = list(map(lambda x: x == officeId, offices))
            if len(listOff) == 0:
                response = {'id':message['id'], 'error':'No tiene permiso para realizar esta operación'}
                server.sendMessage(response)
                return True

            # agrego el rol
            self.offices.addRole(con,userId,officeId,role,sendMail)
            con.commit()
            response = {'id':message['id'], 'ok':'El rol se ha creado correctamente'}
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()


'''
crea una nueva oficina si no existe o sino actualiza los datos

query:{
    id:,
    action:'persistOffice',
    session:,
    request:{
        office: {
            id: "",
            name: "",
            parent: "",
            telephone: "",
            email: ""
        }
    }
}

response: {
    id: "id de la petición",
    ok: "caso exito",
    error: "error del servidor"
}
'''
class PersistOffice:
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'persistOffice'):
            return False

        if ('session' not in message) or ('request' not in message) or ('office' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-OFFICES','USER-OFFICES'])

        req = message['request']
        office = req['office']

        if office is None:
            response = {'id':message['id'], 'error':'Oficina es null'}
            server.sendMessage(response)
            return True

        if 'name' not in office or office['name'].strip() == '':
            response = {'id':message['id'], 'error':'La oficina no posee nombre'}
            server.sendMessage(response)
            return True

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            self.offices.persist(con,office)
            con.commit()
            response = {'id':message['id'], 'ok':'La oficina se ha actualizado correctamente'}
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()


'''
elimina un usuario de una oficina

query:{
    id:,
    action:'removeUserFromOffice',
    session:,
    request:{
        userId: "id del usuario",
        officeId: "id de la oficina"
    }
}

response: {
    id: "id de la petición",
    ok: "caso exito",
    error: "error del servidor"
}

'''
class RemoveUserFromOffice:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'removeUserFromOffice'):
            return False

        if ('session' not in message) or ('request' not in message) or ('userId' not in message['request']) or ('officeId' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-OFFICES','USER-OFFICES'])

        req = message['request']
        officeId = req['officeId']
        userId = req['userId']
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            # verifico si el usuario de session tiene el rol autoriza para la oficina de la cual se desea eliminar el usuario
            localUserId = self.profiles.getLocalUserId(sid)
            offices = self.offices.getOfficesByUserRole(con,localUserId,True,'autoriza')
            listOff = list(map(lambda x: x == officeId, offices))
            if len(listOff) == 0:
                response = {'id':message['id'], 'error':'No tiene permiso para realizar esta operación'}
                server.sendMessage(response)
                return True

            # elimino el usuario de la oficina
            self.offices.removeUser(con,officeId,userId)
            con.commit()
            response = {'id':message['id'], 'ok':'El usuario se ha eliminado correctamente'}
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()

'''
    agrega un usuario (userId) a una oficina (officeId)

query:{
    id:,
    action:'addUserToOffices',
    session:,
    request:{
        userId: "id del usuario",
        officeId: "id de la oficina"
    }
}

response: {
    id: "id de la petición",
    ok: "caso exito",
    error: "error del servidor"
}
'''
class AddUserToOffices:

    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'addUserToOffices'):
            return False

        if ('session' not in message) or ('request' not in message) or ('userId' not in message['request']) or ('officeId' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-OFFICES','USER-OFFICES'])

        req = message['request']
        officeId = req['officeId']
        userId = req['userId']
        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            # verifico si el usuario de session tiene el rol autoriza para la oficina de la cual se desea agregar el usuario
            localUserId = self.profiles.getLocalUserId(sid)
            offices = self.offices.getOfficesByUserRole(con,localUserId,True,'autoriza')
            listOff = list(map(lambda x: x == officeId, offices))
            if len(listOff) == 0:
                response = {'id':message['id'], 'error':'No tiene permiso para realizar esta operación'}
                server.sendMessage(response)
                return True

            # agrego el usuario de la oficina
            self.offices.addUserToOffices(con,officeId,userId)
            con.commit()
            response = {'id':message['id'], 'ok':'El usuario se ha guardado correctamente'}
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            raise e

        finally:
            con.close()
