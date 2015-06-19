# -*- coding: utf-8 -*-
import logging


class Offices:


    def _convertToDict(self,off):
        return {'id':off[0],'parent':off[1],'name':off[2],'telephone':off[3],'email':off[4]}


    '''
        obtiene las oficinas hijas de las oficinas pasadas como parámetro
    '''
    def _getChildOffices(self,con,offices):

        if len(offices) <= 0:
            return []

        '''  obtengo todo el arbol de oficinas abajo de las offices '''
        roffices = []
        pids = []
        pids.extend(offices)

        while len(pids) > 0:
            toFollow = []
            toFollow.extend(pids)
            pids = []

            for oId in toFollow:
                cur = con.cursor()
                cur.execute('select id,parent,name,telephone,email from offices.offices where parent = %s',(oId,))
                if cur.rowcount <= 0:
                    continue

                for cOff in cur:
                    cId = cOff[0]
                    if cId not in pids:
                        roffices.append({'id':cId,'parent':cOff[1],'name':cOff[2]})
                        pids.append(cId)

        return roffices



    '''
        obtiene las oficinas padres de las oficinas pasadas como parametro
    '''
    def _getParentOffices(self,con,offices):

        if len(offices) <= 0:
            return []


        cur = con.cursor()
        cur.execute('select id,parent,name,telephone,email from offices.offices')
        if cur.rowcount <= 0:
            return []

        offrs = cur.fetchall()
        data = []

        ''' agrego las oficinas pasadas como parametro '''
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



    '''
        obtiene los datos de las oficinas pasadas como parámetro
    '''
    def _getOfficesData(self,con,officesIds):

        if len(offices) <= 0:
            return []

        cur = con.cursor()
        cur.execute('select id,parent,name,telephone,email from offices.offices where id in %s',(tuple(officesIds),))
        if cur.rowcount <= 0:
            return []

        offices = []
        for off in cur:
            offices.append(self._convertToDict(off))

        return offices




    ''' obtiene todas las oficinas '''
    def getOffices(self,con):
        cur = con.cursor()
        cur.execute('select id,parent,name,telephone,email from offices.offices')
        offs = cur.fetchall()
        offices = []
        for off in offs:
            offices.append(self._convertToDict(off))
        return offices


    '''
        retorna los ids de los usuarios que pertenecen a las oficinas pasasdas como parámetro
        offices = lista de ids de oficinas
    '''
    def getOfficesUsers(self,con,offices):

        if len(offices) <= 0:
            return []

        users = []
        cur = con.cursor()

        # Obtengo las suboficinas
        logging.debug("------------------------")
        logging.debug(offices)

        logging.debug("------------------------")
        child = self._getChildOffices(con,offices)

        for o in child:
            offices.append(o['id'])

        logging.debug(offices)

        cur.execute('select distinct user_id from offices.offices_users ou where ou.office_id in %s',(tuple(offices),))
        if cur.rowcount <= 0:
            return []

        for u in cur:
            users.append(u[0])

        return users




    ''' obtiene todas las oficinas a las que pertenece un usuario y si tree=True obtiene todas las hijas también '''
    def getOfficesByUser(self,con,userId,tree=False,parents=False):
        cur = con.cursor()
        cur.execute('select id,parent,name,telephone,email from offices.offices o, offices.offices_users ou where ou.user_id = %s and o.id = ou.office_id',(userId,))
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



    '''
        obtiene todos los roles que tiene un usuario dentro de las oficinas
    '''
    def getOfficesRoles(self,con,userId):
        cur = con.cursor()
        cur.execute('select user_id,office_id,role from offices.offices_roles ou where ou.user_id = %s',(userId,))
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




    '''
        obtiene todas las oficinas en las cuales el usuario tiene asignado un rol
        si tree=True obtiene todas las hijas también
    '''
    def getOfficesByUserRole(self,con,userId,tree=False,role='autoriza'):
        cur = con.cursor()
        cur.execute('select id,parent,name,telephone,email from offices.offices o, offices.offices_roles ou where ou.user_id = %s and o.id = ou.office_id and ou.role = %s',(userId,role))
        if cur.rowcount <= 0:
            return []

        offices = []
        ids = []
        for off in cur:
            oId = off[0]
            ids.append(oId)
            offices.append({'id':oId,'parent':off[1],'name':off[2],'telephone':off[3],'email':off[4]})

        if tree:
            offices.extend(self._getChildOffices(con,ids))

        return offices




    '''
        obtiene todos los ids de los usuarios que pertenecen a las oficinas en las cuales un usuario tiene cierto rol.
    '''
    def getUserInOfficesByRole(self,con,userId,tree=False,role='autoriza'):
        offices = self.getOfficesByUserRole(con,userId,tree,role)
        logging.debug(offices)
        if offices is None or len(offices) <= 0:
            return []

        officesIds = list(map(lambda x : x['id'],offices))
        users = self.getOfficesUsers(con,officesIds)
        return users



    '''
        obtiene todos los ids de los usuarios que tienen cierto rol en las oficinas pasadas como parámetro
        retorna :
            [(userId,sendMail)]
    '''
    def getUsersWithRoleInOffices(self,con,officesIds,role='autoriza'):
        if officesIds is None or len(officesIds) <= 0:
            return []

        cur = con.cursor()
        cur.execute('select user_id,send_mail from offices.offices_roles where office_id in %s and role = %s',(tuple(officesIds),role))
        if cur.rowcount <= 0:
            return []

        users = []
        for data in cur:
            users.append((data[0],data[1]))

        return users


    '''
        agrega un usuario (userId) a una oficina (officeId)
    '''
    def addUserToOffices(self,con,officeId,userId):
        if officeId is None or userId is None:
            return

        params = (userId,officeId)
        cur = con.cursor()
        cur.execute('insert into offices.offices_users (user_id,office_id) values (%s,%s)',params)


    '''
        elimina un usuario de una oficina
    '''
    def removeUser(self,con,officeId,userId):
        if officeId is None or userId is None:
            return

        params = (userId,officeId)
        cur = con.cursor()
        cur.execute('delete from offices.offices_users where user_id = %s and office_id = %s',params)



    '''
        crea una nueva oficina si no existe o sino actualiza los datos
    '''
    def persist(self,con,office):
        if office is None or 'name' not in office:
            return

        cur = con.cursor()

        parent = (None,office['parent'])['parent' in office]
        telephone = (None,office['telephone'])['telephone' in office]
        email = (None,office['email'])['email' in office]
        name = office['name']

        params = (parent,name,telephone,email,id)

        if 'id' not in office:
            id = str(uuid.uuid4())
            params.append(id)
            cur.execute('insert into offices.offices (parent,name,telephone,email,id) values(%s,%s,%s,%s,%s)',params)
        else:
            id = office['id']
            params.append(id)
            cur.execute('update offices.offices set parent = %s, name = %s, telephone = %s, email = %s where id = %s',params)



    '''
        setea el rol role al usuario userId para la oficina officeId
        sendMail es un booleano
    '''
    def addRole(self,con,userId,officeId,role,sendMail=True):

        if userId is None or officeId in None or role is None:
            return

        params = (userId,officeId,role,sendMail)
        cur = con.cursor()
        cur.execute('insert into offices.offices (user_id,office_id,role,sendMail) values(%s,%s,%s,%s)',params)



    '''
        elimina el rol para usuario oficina
    '''
    def deleteRole(self,con,userId,officeId,role):
        if userId is None or officeId in None or role is None:
            return

        params = (userId,officeId,role)
        cur = con.cursor()
        cur.execute('delete from offices.offices where user_id = %s and office_id = %s and role = %s',params)
