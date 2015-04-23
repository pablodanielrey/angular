# -*- coding: utf-8 -*-
import logging


class Offices:


    def _convertToDict(self,off):
        return {'id':off[0],'parent':off[1],'name':off[2]}


    """
        obtiene las oficinas hijas de las oficinas pasadas como parámetro
    """
    def _getChildOffices(self,con,offices):

        if len(offices) <= 0:
            return []

        """ obtengo todo el arbol de oficinas abajo de las offices """
        roffices = []
        pids = []
        pids.extend(offices)

        while len(pids) > 0:
            toFollow = []
            toFollow.extend(pids)
            pids = []

            for oId in toFollow:
                cur = con.cursor()
                cur.execute('select id,parent,name from assistance.offices where parent = %s',(oId,))
                if cur.rowcount <= 0:
                    continue

                for cOff in cur:
                    cId = cOff[0]
                    if cId not in pids:
                        roffices.append({'id':cId,'parent':cOff[1],'name':cOff[2]})
                        pids.append(cId)

        return roffices



    """
        obtiene las oficinas padres de las oficinas pasadas como parametro
    """
    def _getParentOffices(self,con,offices):

        if len(offices) <= 0:
            return []


        cur = con.cursor()
        cur.execute('select id,parent,name from assistance.offices')
        if cur.rowcount <= 0:
            return []

        offrs = cur.fetchall()
        data = []

        """ agrego las oficinas pasadas como parametro """
        for oid in offices:
            for x in offrs:
                if x[0] == oid:
                    data.append(self._convertToDict(x))
                    break


        parents = []
        parentsIds = []
        for office in data:
            pid = office['parent']
            while (pid != None) and (pid not in parentsIds):
                for parent in offrs:
                    if parent[0] == pid:
                        parentsIds.append(pid)
                        parents.append(self._convertToDict(parent))
                        pid = parent[1]
                        break

        return parents



    """
        obtiene los datos de las oficinas pasadas como parámetro
    """
    def _getOfficesData(self,con,officesIds):

        if len(offices) <= 0:
            return []

        cur = con.cursor()
        cur.execute('select id,parent,name from assistance.offices where id in %s',(tuple(officesIds),))
        if cur.rowcount <= 0:
            return []

        offices = []
        for off in cur:
            offices.append(self._convertToDict(off))

        return offices




    """ obtiene todas las oficinas """
    def getOffices(self,con):
        cur = con.cursor()
        cur.execute('select id,parent,name from assistance.offices')
        offs = cur.fetchall()
        offices = []
        for off in offs:
            offices.append(self._convertToDict(off))
        return offices


    """
        retorna los ids de los usuarios que pertenecen a las oficinas pasasdas como parámetro
        offices = lista de ids de oficinas
    """
    def getOfficesUsers(self,con,offices):

        if len(offices) <= 0:
            return []

        users = []
        cur = con.cursor()
        cur.execute('select distinct user_id from assistance.offices_users ou where ou.office_id in %s',(tuple(offices),))
        if cur.rowcount <= 0:
            return []

        for u in cur:
            users.append(u[0])

        return users




    """ obtiene todas las oficinas a las que pertenece un usuario y si tree=True obtiene todas las hijas también """
    def getOfficesByUser(self,con,userId,tree=False,parents=False):
        cur = con.cursor()
        cur.execute('select id,parent,name from assistance.offices o, assistance.offices_users ou where ou.user_id = %s and o.id = ou.office_id',(userId,))
        if cur.rowcount <= 0:
            return []

        offices = []
        ids = []
        for off in cur:
            oId = off[0]
            ids.append(oId)
            offices.append(self._convertToDict(off))

        if tree:
            offices.extend(self._getChildOffices(con,ids))

        if parents:
            offices.extend(self._getParentOffices(con,ids))

        return offices



    """
        obtiene todos los roles que tiene un usuario dentro de las oficinas
    """
    def getOfficesRoles(self,con,userId):
        cur = con.cursor()
        cur.execute('select user_id,office_id,role from assistance.offices_roles ou where ou.user_id = %s',(userId,))
        if cur.rowcount <= 0:
            return []

        roles = []
        for r in cur:
            roles.append({
                'userId':r[0],
                'officeId':r[1],
                'role':r[2]
            })

        return roles




    """
        obtiene todas las oficinas en las cuales el usuario tiene asignado un rol
        si tree=True obtiene todas las hijas también
    """
    def getOfficesByUserRole(self,con,userId,tree=False,role='administra'):
        cur = con.cursor()
        cur.execute('select id,parent,name from assistance.offices o, assistance.offices_roles ou where ou.user_id = %s and o.id = ou.office_id and ou.role = %s',(userId,role))
        if cur.rowcount <= 0:
            return []

        offices = []
        ids = []
        for off in cur:
            oId = off[0]
            ids.append(oId)
            offices.append({'id':oId,'parent':off[1],'name':off[2]})

        if tree:
            offices.extend(self._getChildOffices(con,ids))

        return offices


    """
        obtiene todos los ids de los usuarios que pertenecen a las oficinas en las cuales un usuario tiene cierto rol.
    """
    def getUserInOfficesByRole(self,con,userId,tree=False,role='autoriza'):
        offices = self.getOfficesByUserRole(con,userId,tree,role)
        logging.debug(offices)
        if offices is None or len(offices) <= 0:
            return []

        officesIds = list(map(lambda x : x['id'],offices))
        users = self.getOfficesUsers(con,officesIds)
        return users



    """
        obtiene todos los ids de los usuarios que tienen cierto rol en las oficinas pasadas como parámetro
        retorna :
            [(userId,sendMail)]
    """
    def getUsersWithRoleInOffices(self,con,officesIds,role='autoriza'):
        cur = con.cursor()
        cur.execute('select user_id,send_mail from assistance.offices_roles where office_id in %s and role = %s',(tuple(officesIds),role))
        if cur.rowcount <= 0:
            return []

        users = []
        for data in cur:
            users.append((data[0],data[1]))

        return users
