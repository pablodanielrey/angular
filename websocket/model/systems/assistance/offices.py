# -*- coding: utf-8 -*-

class Offices:

    """ obtiene todas las oficinas """
    def getOffices(self,con):
        cur = con.cursor()
        cur.execute('select id,parent,name from assistance.offices')
        offs = cur.fetchall()
        offices = []
        for off in offs:
            offices.append({'id':off[0],'parent':off[1],'name':off[2]})
        return offices


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
            """ obtengo todo el arbol de oficinas abajo de las actuales """
            pids = []
            pids.extends(ids)

            while len(pids) > 0:
                toFollow = []
                toFollow.extend(pids)
                pids = []

                for oId in toFollow:
                    cur.execute('select id,parent,name from asssitance.offices where parent = %s',(oId,))
                    if cur.rowcount <= 0:
                        continue

                    cOffs = cur.fetchall()
                    for cOff in cOffs:
                        cId = off[0]
                        if cId not in ids:
                            offices.append({'id':cId,'parent':cOff[1],'name':cOff[2]})
                            pids.append(cId)


        return offices
