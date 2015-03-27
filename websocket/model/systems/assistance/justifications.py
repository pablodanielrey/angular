# -*- coding: utf-8 -*-

from model.systems.assistance.restrictions import Repetition, CJustification, LAOJustification, AAJustification, BSJustification

class Justifications:


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



    """ retorna el stock total de la justificacion indicada """
    def getJustificationStock(self,con,userId,justId,date):

        for j in self.justifications:
            if j.isJustification(justId):
                ad = j.availableRep(Repetition.DAILY,userId,date)
                if ad is not None:
                    return ad

                aw = j.availableRep(Repetition.WEEKLY,userId,date)
                if aw is not None:
                    return aw

                am = j.availableRep(Repetition.MONTHLY,userId,date)
                if am is not None:
                    return am

                ay = j.availableRep(Repetition.YEARLY,userId,date)
                if ay is not None:
                    return ay

                return j.available(con,userId,date)

        """ justificationes desconocidas = 0 """
        return 0




    """ retorna el stock actual posible de tomarse para la justificación indicada """
    def getJustificationActualStock(self,con,userId,justId,date):

        for j in self.justifications:
            if j.isJustification(justId):
                return j.available(con,userId,date)

        """ justificationes desconocidas = 0 """
        return 0





    """
    obtiene todas los pedidos de justificaciones.
    los parámetros son opcionales y definen el filtro a usar para obtener
    """
    def getJustificationRequests(self,con,userId=None,justificationId=None,state=None):
        cur = con.cursor()

        if userId is None and justificationId == None and state is None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests')

        if userId != None and justificationId is None and state is None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where user_id = %s',(userId,))

        elif userId != None and justificationId != None and state is None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where user_id = %s and justification_id = %s',(userId,justificationId))

        elif userId != None and justificationId is None and state != None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where user_id = %s and state = %s',(userId,state))

        elif userId != None and justificationId != None and state != None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where user_id = %s and state = %s and justificationId = %s',(userId,state,justificationId))

        elif userId is None and justificationId != None and state is None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where justification_id = %s',(justificationId,))

        elif userId is None and justificationId != None and state != None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where justification_id = %s and state = %s',(justificationId,state))

        elif userId is None and  justificationId is None and state != None:
            cur.execute('select id,user_id,justification_id,jbegin,jend,status from assistance.justifications_requests where state = %s',(state,))


        req = cur.fetchall()
        requests = []
        for r in req:
            requests.append(
                {
                    'justification_id':req[2],
                    'begin':req[3],
                    'end':req[4],
                    'state':req[5]
                }
            )

        return requests



    """ realiza el pedido de justificación para ser aprobado """
    def requestJustification(self,con,userId,req):


        """ aca se deben chequear todos los parametros para ver si es posible realizar el pedido """


        cur = con.cursor()
        jid = str(uuid.uuid4())
        rreq = (jid,userId,req['justificationId'],req['begin'],req['end'],'PENDING')
        cur.execute('insert into assistance.justifications_request (id,user_id,justification_id,jbegin,jend,status) values (%s,%s,%s,%s,%s,%s)',rreq)
