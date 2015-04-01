# -*- coding: utf-8 -*-

from model.systems.assistance.restrictions import Repetition, CJustification, LAOJustification, AAJustification, BSJustification

class Justifications:

    offices = inject.attr(Offices)
    justifications = [
        CJustification(), LAOJustification(), AAJustification(), BSJustification()
    ]



    """ retorna todos los tipos de justificaciones que existan en la base """
    def getJustifications(self,con):
        cur = con.cursor()
        cur.execute('select id,name from assistance.justifications')
        if cur.rowcount <= 0:
            return []

        justs = []
        for j in cur:
            justs.append(
                {
                    'id':j[0],
                    'name':j[1]
                }
            )
        return justs


    """ retorna el stock actual para la justificación indicada """
    def getJustificationStock(self,con,userId,justId,date):

        for j in self.justifications:
            if j.isJustification(justId):
                return j.available(con,userId,date)

        """ justificationes desconocidas = 0 """
        return 0





    """
        obtiene todas los pedidos de justificaciones con cierto estado
        users es una lista de ids de usuarios que piden los requests, si = None entonces no lo tiene en cuenta.
    """
    def getJustificationRequests(self,con,status,users=None):

        cur = con.cursor()

        """ obtengo las justificaciones que tienen como ultimo estado el estado pasado por parámetro """
        cur.execute('select jrs.request_id from assistance.justifications_requests_status as jrs, (select request_id,max(created) as created from assistance.justifications_requests_status group by request_id) as r where r.created = jrs.created and r.request_id = jrs.request_id and r.status = %s',(status,))
        if cur.rowcount <= 0
            return []

        rids = []
        for rs in cur:
            rids.append(rs[0])

        if users is None:
            cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where id in ',(tuple(rids),))
        else:
            cur.execute('select id,user_id,justification_id,jbegin,jend from assistance.justifications_requests where id = %s and user_id in %s',(tuple(rids),tuple(users)))

        if cur.rowcount <= 0:
            return []

        requests = []
        for j in cur:
            requests.append(
                'id':j[0],
                'user_id':j[1],
                'justification_id':j[2],
                'begin':j[3],
                'end':j[4],
                'status':status
            )

        return requests




    """ realiza el pedido de justificación para ser aprobado """
    def requestJustification(self,con,userId,req):
        pass
