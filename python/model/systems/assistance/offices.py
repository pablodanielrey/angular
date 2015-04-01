# -*- coding: utf-8 -*-

class Offices:


    """
        obtiene las oficinas hijas de las oficinas pasadas como parámetro
    """
    def _getChildOffices(self,offices):

        if len(offices) <= 0:
            return []

        """ obtengo todo el arbol de oficinas abajo de las offices """
        roffices = []
        pids = []
        pids.extends(offices)

        while len(pids) > 0:
            toFollow = []
            toFollow.extend(pids)
            pids = []

            for oId in toFollow:
                cur.execute('select id,parent,name from asssitance.offices where parent = %s',(oId,))
                if cur.rowcount <= 0:
                    continue

                for cOff in cur:
                    cId = cOff[0]
                    if cId not in pids:
                        roffices.append({'id':cId,'parent':cOff[1],'name':cOff[2]})
                        pids.append(cId)

        return roffices



    """ obtiene todas las oficinas """
    def getOffices(self,con):
        cur = con.cursor()
        cur.execute('select id,parent,name from assistance.offices')
        offs = cur.fetchall()
        offices = []
        for off in offs:
            offices.append({'id':off[0],'parent':off[1],'name':off[2]})
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

        for u in cur:
            users.append(u[0])

        return users




    """ obtiene todas las oficinas a las que pertenece un usuario y si tree=True obtiene todas las hijas también """
    def getOfficesByUser(self,con,userId,tree=False):
        cur = con.cursor()
        cur.execute('select id,parent,name from assistance.offices o, assistance.offices_users ou where ou.user_id = %s and o.id = ou.office_id',(userId,))
        if cur.rowcount <= 0:
            return []

        offices = []
        ids = []
        for off in cur:
            oId = off[0]
            ids.append(oId)
            offices.append({'id':oId,'parent':off[1],'name':off[2]})

        if tree:
            offices.extend(self._getChildOffices(ids))

        return offices



    """
        obtiene todas las oficinas en las cuales el usuario tiene asignado un rol
        si tree=True obtiene todas las hijas también
    """
    def getOfficesByUserRole(self,con,userId,tree=False):
        cur = con.cursor()
        cur.execute('select id,parent,name from assistance.offices o, assistance.offices_roles ou where ou.user_id = %s and o.id = ou.office_id',(userId,))
        if cur.rowcount <= 0:
            return []

        offices = []
        ids = []
        for off in cur:
            oId = off[0]
            ids.append(oId)
            offices.append({'id':oId,'parent':off[1],'name':off[2]})

        if tree:
            offices.extend(self._getChildOffices(ids))

        return offices
