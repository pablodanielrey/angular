# -*- coding: utf-8 -*-
import json, base64, datetime, traceback, logging
import inject
import psycopg2

from model.exceptions import *

from model.config import Config
from model.profiles import AccessDenied, Profiles

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
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE','ADMIN-OFFICES','USER-OFFICES'])

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
Retorna los roles que puede asignar el usuario (userId) para las oficinas (officesId) y para los usuarios (usersId)
Ademas retorna los roles que ya poseen lso usarios
query:
{
  id:
  action:'getRolesAdmin'
  session:
  request: {
    userId: 'id del usuario -- opcional, en el caso de no existir se toma el usuario de sesión'
    officesId: [] 'ids de la oficina'
    usersId: [] 'listado de usarios'
  }
}

response:
{
  id:
  ok:
  error:
  response: {
    roles: [],
    assignedRoles: [{
        name:'',
        send_mail: '' --- 't' | 'f'   si tiene mas de un valor retorno false
    }]
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

        if ('session' not in message) or ('request' not in message) or ('officesId' not in message['request']) or ('usersId' not in message['request']):
            response = {'id':message['id'], 'error': 'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-OFFICES','USER-OFFICES'])

        req = message['request']
        officesId = req['officesId']
        usersId = req['usersId']

        if 'userId' in req:
            userId = req['userId']
        else:
            userId = self.profiles.getLocalUserId(sid)

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            roles = self.offices.getRolesAdmin(con, userId, officesId, usersId)
            assignedRoles = self.offices.getAssignedRoles(con, officesId, usersId, roles)
            response = {
                'id':message['id'],
                'ok':'',
                'response': {
                    'roles':roles,
                    'assignedRoles':assignedRoles
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
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE','ADMIN-OFFICES','USER-OFFICES'])
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
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE','ADMIN-OFFICES','USER-OFFICES'])

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
        self.profiles.checkAccess(sid,['ADMIN-ASSISTANCE','USER-ASSISTANCE','ADMIN-OFFICES','USER-OFFICES'])

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
        usersId: [],
        officesId: [],
        role: "nombre del rol que se desea eliminar"
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

        if ('session' not in message) or ('request' not in message) or ('usersId' not in message['request']) or ('role' not in message['request']) or ('officesId' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True

        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-OFFICES','USER-OFFICES'])

        req = message['request']
        officesId = req['officesId']
        usersId = req['usersId']
        role = req['role']

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            # verifico si el usuario de session tiene el rol admin-office para la oficina de la cual se desean eliminar el rol
            localUserId = self.profiles.getLocalUserId(sid)
            offices = self.offices.getOfficesByUserRole(con,localUserId,True,'admin-office')
            for officeId in officesId:
                listOff = list(map(lambda x: x == officeId, offices))
                if len(listOff) == 0:
                    response = {'id':message['id'], 'error':'No tiene permiso para realizar esta operación'}
                    server.sendMessage(response)
                    return True

            # elimino el rol
            for officeId in officesId:
                for userId in usersId:
                    self.offices.deleteRole(con,userId,officeId,role)

            con.commit()
            response = {'id':message['id'], 'ok':'El rol se ha eliminado correctamente'}
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            con.rollback()
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
        usersId: [],
        officesId: [],
        role: {
            name: '',
            send_mail: ''
        }
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

        if ('session' not in message) or ('request' not in message) or ('usersId' not in message['request']) or ('role' not in message['request']) or ('officesId' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-OFFICES','USER-OFFICES'])

        req = message['request']

        role = req['role']
        if ('name' not in role) or role["name"].strip() == "":
            response = {'id':message['id'], 'error':'El rol no tiene nombre'}
            server.sendMessage(response)
            return True

        roleName = req['role']['name']

        officesId = req['officesId']

        usersId = req['usersId']

        sendMail = (True,role['send_mail'])['send_mail' in role]

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            # verifico si el usuario de session tiene el rol admin-office para la oficina de la cual se desea agregar el rol
            localUserId = self.profiles.getLocalUserId(sid)
            offices = self.offices.getOfficesByUserRole(con,localUserId,True,'admin-office')
            for officeId in officesId:
                listOff = list(map(lambda x: x == officeId, offices))
                if len(listOff) == 0:
                    response = {'id':message['id'], 'error':'No tiene permiso para realizar esta operación'}
                    server.sendMessage(response)
                    return True

            # agrego el rol
            for userId in usersId:
                for officeId in officesId:
                    self.offices.addRole(con,userId,officeId,roleName,sendMail)

            con.commit()
            response = {'id':message['id'], 'ok':'El rol se ha creado correctamente'}
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            con.rollback()
            raise e

        finally:
            con.close()



'''
actualiza los roles para todos los usersId en officesId

query:{
    id:,
    action:'persistOfficeRole',
    session:,
    request:{
        usersId: [],
        officesId: [],
        roles: [{
            name: '',
            send_mail: ''
        }],
        oldRoles: [{
            name: '',
            send_mail: ''
        }]
    }
}

response: {
    id: "id de la petición",
    ok: "caso exito",
    error: "error del servidor"
}
'''
class PersistOfficeRole:
    profiles = inject.attr(Profiles)
    config = inject.attr(Config)
    offices = inject.attr(Offices)

    def handleAction(self, server, message):

        if (message['action'] != 'persistOfficeRole'):
            return False

        if ('session' not in message) or ('request' not in message) or ('usersId' not in message['request']) or ('roles' not in message['request']) or ('oldRoles' not in message['request'])  or ('officesId' not in message['request']):
            response = {'id':message['id'], 'error':'Insuficientes parámetros'}
            server.sendMessage(response)
            return True


        sid = message['session']
        self.profiles.checkAccess(sid,['ADMIN-OFFICES','USER-OFFICES'])

        req = message['request']

        roles = req['roles']

        oldRoles = req['oldRoles']

        officesId = req['officesId']

        usersId = req['usersId']

        con = psycopg2.connect(host=self.config.configs['database_host'], dbname=self.config.configs['database_database'], user=self.config.configs['database_user'], password=self.config.configs['database_password'])
        try:
            # verifico si el usuario de session tiene el rol admin-office para la oficina de la cual se desea agregar el rol
            localUserId = self.profiles.getLocalUserId(sid)
            offices = self.offices.getOfficesByUserRole(con,localUserId,True,'admin-office')
            for officeId in officesId:
                listOff = list(map(lambda x: x == officeId, offices))
                if len(listOff) == 0:
                    response = {'id':message['id'], 'error':'No tiene permiso para realizar esta operación'}
                    server.sendMessage(response)
                    return True


            # elimino los roles que tenia antes
            for userId in usersId:
                for officeId in officesId:
                    for role in oldRoles:
                        roleName = role['name']
                        self.offices.deleteRole(con,userId,officeId,roleName)

            # agrego los nuevos roles
            for userId in usersId:
                for officeId in officesId:
                    for role in roles:
                        sendMail = (True,role['send_mail'])['send_mail' in role]
                        self.offices.addRole(con,userId,officeId,role['name'],sendMail)

            con.commit()
            response = {'id':message['id'], 'ok':'Los roles se han modificado correctamente'}
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            con.rollback()
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
        self.profiles.checkAccess(sid,['SUPER-ADMIN-OFFICES','ADMIN-OFFICES','USER-OFFICES'])

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
            if 'parent' not in office or office['parent'] == '':
                parent = None
                if 'parent' in office:
                    parent = office['parent']
                # verifico si se modifico el padre
                actualOffice = None
                if 'id' in office:
                    actualOffice = self.offices.findOffice(con,office['id'])
                if actualOffice == None or actualOffice['parent'] != parent:
                    # en dicho caso verifico que tenga el perfil de super admin
                    self.profiles.checkAccess(sid,['SUPER-ADMIN-OFFICES'])

            self.offices.persist(con,office)
            con.commit()
            response = {'id':message['id'], 'ok':'La oficina se ha actualizado correctamente'}
            server.sendMessage(response)
            return True

        except psycopg2.DatabaseError as e:
            con.rollback()
            raise e

        except AccessDenied as e:
            logging.exception(e)
            con.rollback()

            response = {
                'id':message['id'],
                'error':'No tiene permisos necesarios para realizar esta operacion'
            }
            server.sendMessage(response)
            return True

        except Exception as e:
            logging.exception(e)
            con.rollback()

            response = {
                'id':message['id'],
                'error':str(e)
            }
            server.sendMessage(response)
            return True

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
            # verifico si el usuario de session tiene el rol admin-office para la oficina de la cual se desea eliminar el usuario
            localUserId = self.profiles.getLocalUserId(sid)
            offices = self.offices.getOfficesByUserRole(con,localUserId,True,'admin-office')
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
            # verifico si el usuario de session tiene el rol admin-office para la oficina de la cual se desea agregar el usuario
            localUserId = self.profiles.getLocalUserId(sid)
            offices = self.offices.getOfficesByUserRole(con,localUserId,True,'admin-office')
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
            con.rollback()
            raise e

        finally:
            con.close()
