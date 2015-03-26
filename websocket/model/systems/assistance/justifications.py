# -*- coding: utf-8 -*-

class Justifications:


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
    def getJustificationStock(self,con,userId,justId):
        cur = con.cursor()
        cur.execute('select quantity from assistance.justifications_stock where user_id = %s and justification_id = %s',(userId,justId))
        stock = cur.fetchone()
        if stock == None:
            return None
        s = {'quantity':stock[0]}
        return s



    """ retorna el stock actual posible de tomarse para la justificación indicada """
    def getJustificationActualStock(self,con,userId,justId,date):

        """
        ('e0dfcef6-98bb-4624-ae6c-960657a9a741','Ausente con aviso')
        ('48773fd7-8502-4079-8ad5-963618abe725','Compensatorio')
        ('fa64fdbd-31b0-42ab-af83-818b3cbecf46','Boleta de Salida')
        ('4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb','Art 102')
        ('b70013e3-389a-46d4-8b98-8e4ab75335d0','Pre-Exámen')
        ('76bc064a-e8bf-4aa3-9f51-a3c4483a729a','Licencia Anual Ordinaria')
        ('50998530-10dd-4d68-8b4a-a4b7a87f3972','Resolución')
        """

        restrictions = [
            AARestriction(), BSRestriction(), CRestriction()
        ]

        for r in restrictions:
            if r.isJustification(justId):
                return r.available(self,con,userId,)

        """ si no existe ninguna restricción sobre la justificación entonces se retorna el stock """
        stock = assistance.getJustificationStock(con,userId,justId)
        if stock == None:
            return 0

        jstock = stock['quantity']
        if jstock <= 0:
            return 0
        else:
            return jstock





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
