# -*- coding: utf-8 -*-
import inject
import logging
import psycopg2

import asyncio
from asyncio import coroutine
from autobahn.asyncio.wamp import ApplicationSession

from model.config import Config
from model.profiles import Profiles
from model.systems.offices.offices import Offices


class OfficesWamp(ApplicationSession):

    def __init__(self, config=None):
        logging.debug('instanciando')
        ApplicationSession.__init__(self, config)

        self.serverConfig = inject.instance(Config)
        self.profiles = inject.instance(Profiles)
        self.offices = inject.instance(Offices)

    @coroutine
    def onJoin(self, details):
        logging.debug('registering methods')
        yield from self.register(self.getOffices_async, 'offices.offices.getOffices')
        yield from self.register(self.findOffices_async, 'offices.offices.findOffices')
        yield from self.register(self.getOfficesByUser_async, 'offices.offices.getOfficesByUser')
        yield from self.register(self.getOfficesTree_async, 'offices.offices.getOfficesTree')
        yield from self.register(self.getOfficesTreeByUser_async, 'offices.offices.getOfficesTreeByUser')
        yield from self.register(self.getOfficesUsers_async, 'offices.offices.getOfficesUsers')
        yield from self.register(self.getUserInOfficesByRole_async, 'offices.offices.getUserInOfficesByRole')
        yield from self.register(self.getOfficesByUserRole_async, 'offices.offices.getOfficesByUserRole')
        yield from self.register(self.deleteOfficeRole_async, 'offices.offices.deleteOfficeRole')
        yield from self.register(self.addOfficeRole_async, 'offices.offices.addOfficeRole')
        yield from self.register(self.persistOfficeRole_async, 'offices.offices.persistOfficeRole')
        yield from self.register(self.persistOffice_async, 'offices.offices.persistOffice')
        yield from self.register(self.removeUserFromOffice_async, 'offices.offices.removeUserFromOffice')
        yield from self.register(self.addUserToOffices_async, 'offices.offices.addUserToOffices')
        yield from self.register(self.getRolesAdmin_async, 'offices.offices.getRolesAdmin')
        yield from self.register(self.getUserOfficeRoles_async, 'offices.offices.getUserOfficeRoles')

    def _getDatabase(self):
        host = self.serverConfig.configs['database_host']
        dbname = self.serverConfig.configs['database_database']
        user = self.serverConfig.configs['database_user']
        passw = self.serverConfig.configs['database_password']
        return psycopg2.connect(host=host, dbname=dbname, user=user, password=passw)

    '''
        Obtiene los roles que tiene dentro de las oficinas el usuario
    '''
    def getUserOfficeRoles(self, userId):
        con = self._getDatabase()
        try:
            return self.offices.getOfficesRoles(con, userId)
        finally:
            con.close()

    @coroutine
    def getUserOfficeRoles_async(self, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getUserOfficeRoles, userId)
        return r

    def getOfficesByUser(self, sessionId, userId, tree):
        con = self._getDatabase()
        try:
            return self.offices.getOfficesByUser(con, userId, tree, False)
        finally:
            con.close()

    @coroutine
    def getOfficesByUser_async(self, sessionId, userId, tree):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOfficesByUser, sessionId, userId, tree)
        return r


    def getOfficesTree(self):
        con = self._getDatabase()
        try:
            return self.offices.getOfficesTree(con)
        finally:
            con.close()

    @coroutine
    def getOfficesTree_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOfficesTree)
        return r


    def getOfficesTreeByUser(self, sessionId, userId):
        con = self._getDatabase()
        try:
            if userId is None:
                userId = self.profiles.getLocalUserId(sessionId)
            return self.offices.getOfficesTreeByUser(con,userId)
        finally:
            con.close()

    @coroutine
    def getOfficesTreeByUser_async(self, sessionId, userId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOfficesTreeByUser, sessionId, userId)
        return r

    def getOffices(self):
        con = self._getDatabase()
        try:
            return self.offices.getOffices(con)
        finally:
            con.close()

    @coroutine
    def getOffices_async(self):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOffices)
        return r


    def getOfficesUsers(self, offices):
        con = self._getDatabase()
        try:
            return self.offices.getOfficesUsers(con,offices)
        finally:
            con.close()

    @coroutine
    def getOfficesUsers_async(self, offices):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOfficesUsers, offices)
        return r


    def getUserInOfficesByRole(self, userId, role, tree):
        con = self._getDatabase()
        try:
            tree = False if tree is None else tree
            self.offices.getUserInOfficesByRole(con,userId,tree,role)
        finally:
            con.close()

    @coroutine
    def getUserInOfficesByRole_async(self, userId, role, tree):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getUserInOfficesByRole, userId, role, tree)
        return r


    def getOfficesByUserRole(self, userId, role, tree):
        con = self._getDatabase()
        try:
            if tree is None:
                self.offices.getOfficesByUserRole(con,userId)
            elif role is None:
                self.offices.getOfficesByUserRole(con,userId,tree)
            else:
                self.offices.getOfficesByUserRole(con,userId,tree,role)

        finally:
            con.close()

    @coroutine
    def getOfficesByUserRole_async(self, userId, role, tree):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getOfficesByUserRole, userId, role, tree)
        return r


    def _checkRoleByOffices(officesId,role):
        localUserId = self.profiles.getLocalUserId(sid)
        offices = self.offices.getOfficesByUserRole(con,localUserId,True,role)
        for officeId in officesId:
            listOff = list(map(lambda x: x == officeId, offices))
            if len(listOff) == 0:
                return False
        return True


    def deleteOfficeRole(self, officesId, usersId, role):
        con = self._getDatabase()
        try:
            if self._checkRoleByOffices(officesId,'admin-office'):
                # elimino el rol
                for officeId in officesId:
                    for userId in usersId:
                        self.offices.deleteRole(con,userId,officeId,role)
                con.commit()
                return 'ok'
            else:
                return None

        except psycopg2.DatabaseError as e:
            con.rollback()
            return None
        except Exception as e:
            con.rollback()
            return None
        finally:
            con.close()

    @coroutine
    def deleteOfficeRole_async(self, officesId, usersId, role):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.deleteOfficeRole, officesId, usersId, role)
        return r


    def addOfficeRole(self, officesId, usersId, role):
        if ('name' not in role) or role["name"].strip() == "":
            return None
        con = self._getDatabase()
        try:
            if self._checkRoleByOffices(officesId,'admin-office'):
                for userId in usersId:
                    for officeId in officesId:
                        self.offices.addRole(con,userId,officeId,roleName,sendMail)
                con.commit()
                return 'ok'
            return None

        except psycopg2.DatabaseError as e:
            con.rollback()
            return None
        except Exception as e:
            con.rollback()
            return None
        finally:
            con.close()

    @coroutine
    def addOfficeRole_async(self, officesId, usersId, role):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.addOfficeRole, officesId, usersId, role)
        return r


    def _deleteRoles(self, con, userId, officesId, roles):
        for officeId in officesId:
            for role in oldRoles:
                roleName = role['name']
                self.offices.deleteRole(con, userId, officeId, roleName)

    def _addRoles(self, con, userId, officesId, roles):
        for officeId in officesId:
            for role in roles:
                if 'send_mail' in role:
                    self.offices.addRole(con, userId, officeId, role['name'], sendMail)
                else:
                    self.offices.addRole(con, userId, officeId, role['name'])


    def persistOfficeRole(self, officesId, usersId, roles, oldRoles):
        con = self._getDatabase()
        try:
            if self._checkRoleByOffices(officesId,'admin-office'):
                for userId in usersId:
                    self._deleteRoles(con,userId,officesId,oldRoles)
                    self._addRoles(con,userId,officesId,roles)

                con.commit()
                return 'ok'

            return None

        except psycopg2.DatabaseError as e:
            con.rollback()
            return None
        except Exception as e:
            con.rollback()
            return None

        finally:
            con.close()

    @coroutine
    def persistOfficeRole_async(self, officesId, usersId, roles, oldRoles):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistOfficeRole, officesId, usersId, roles, oldRoles)
        return r


    def persistOffice(self, sessionId, office):
        con = self._getDatabase()
        try:
            if 'parent' not in office or office['parent'] == '':
                if self._checkModifiedParent():
                    # si se modifico el padre me fijo que tenga el perfil de super admin
                    self.profiles.checkAccess(sessionId,['SUPER-ADMIN-OFFICES'])

            self.offices.persist(con,office)
            con.commit()
            return True

        except psycopg2.DatabaseError as e:
            con.rollback()
            return None
        except Exception as e:
            con.rollback()
            return None
        finally:
            con.close()

    @coroutine
    def persistOffice_async(self, sessionId, office):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.persistOffice, sessionId, office)
        return r


    def removeUserFromOffice(self, userId, officeId):
        con = self._getDatabase()
        try:
            if self._checkRoleByOffices([officeId],'admin-office'):
                self.offices.removeUser(con,officeId,userId)
                con.commit()
                return True

            return None
        except psycopg2.DatabaseError as e:
            con.rollback()
            return None
        except Exception as e:
            con.rollback()
            return None
        finally:
            con.close()

    @coroutine
    def removeUserFromOffice_async(self, userId, officeId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.removeUserFromOffice, userId, officeId)
        return r


    def addUserToOffices(self, userId, officeId):
        con = self._getDatabase()
        try:
            if self._checkRoleByOffices([officeId],'admin-office'):
                self.offices.addUserToOffices(con,officeId,userId)
                con.commit()
                return True

            return None
        except psycopg2.DatabaseError as e:
            con.rollback()
            return None
        except Exception as e:
            con.rollback()
            return None
        finally:
            con.close()

    @coroutine
    def addUserToOffices_async(self, userId, officeId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.addUserToOffices, userId, officeId)
        return r


    def getRolesAdmin(self, sessionId, userId, officesId, usersId):
        con = self._getDatabase()
        try:
            if userId is None:
                userId = self.profiles.getLocalUserId(sessionId)

            roles = self.offices.getRolesAdmin(con, userId, officesId, usersId)
            assignedRoles = self.offices.getAssignedRoles(con, officesId, usersId, roles)

            return True

        except psycopg2.DatabaseError as e:
            con.rollback()
            return None
        except Exception as e:
            con.rollback()
            return None
        finally:
            con.close()

    @coroutine
    def getRolesAdmin_async(self, sessionId, userId, officesId, usersId):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.getRolesAdmin, sessionId, userId, officesId, usersId)
        return r


    def findOffices(self, ids):
        con = self._getDatabase()
        try:
            return self.offices.findOffices(con,ids)
        finally:
            con.close()

    @coroutine
    def findOffices_async(self, ids):
        loop = asyncio.get_event_loop()
        r = yield from loop.run_in_executor(None, self.findOffices, ids)
        return r
