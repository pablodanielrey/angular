# -*- coding: utf-8 -*-
import uuid, datetime

class Digesto:

    # -----------------------------------------------------------------------------------
    # --------------------- ESTADO DE LA NORMATIVA --------------------------------------
    # -----------------------------------------------------------------------------------

    '''
        EStados posibles de una normativa: PENDING,APPROVED
    '''

    def _convertStatusToDict(self,status):
        return {'id':status[0],'status':status[1],'created':status[2],'creator_id':status[3],'normative_id':status[4]}

    # Obtiene el ultimo estado de la normativa
    def getStatus(self,con,normative_id):
        cur = con.cursor()
        cur.execute('select id,status,created,creator_id,normative_id from digesto.status where normative_id =  %s order by created desc limit 1',(normative_id,))
        if cur.rowcount <= 0:
            return None
        return self._convertStatusToDict(cur.fetchone())

    # crea un nuevo estado, por defecto lo pone como pendiente
    def updateStatus(self,con,normative_id,creator_id,status='PENDING'):
        if normative_id is None or creator_id is None:
            return

        cur = con.cursor()

        id = str(uuid.uuid4())
        created = datetime.datetime.now()
        params = (id,status,created,creator_id,normative_id)

        cur.execute('insert into digesto.status (id,status,created,creator_id,normative_id) values(%s,%s,%s,%s,%s)',params)

    # -----------------------------------------------------------------------------------
    # --------------------- NORMATIVAs RELACIONADAS -------------------------------------
    # -----------------------------------------------------------------------------------

    def _convertRelatedToDict(self,related):
        return {'id':related[0],'normative_id':related[1],'related_id':related[2],'created':related[3],'creator_id':related[4],'type':related[5]}

    # relateds [{'related_id':'','type':''}]
    def addRelateds(self,con,relateds,creator_id,normative_id):
        if relateds is None or len(relateds) <= 0:
            return

        cur = con.cursor()
        for r in relateds:
            if 'related_id' not in r or 'type' not in r:
                continue
            id = str(uuid.uuid4())
            params = (id,normative_id,r['related_id'],creator_id,r['type'])
            cur.execute('insert into digesto.related (id,normative_id,related_id,creator_id,type) values(%s,%s,%s,%s,%s)',params)


    def deleteRelateds(self,con,ids):
        if len(ids) <= 0:
            return

        cur = con.cursor()
        cur.execute('delete from digesto.related where id in %s',(tuple(ids),))

    def findRelateds(self,con,id):
        if id is None:
            return []

        cur = con.cursor()
        cur.execute('select id,normative_id,related_id,created,creator_id,type from digesto.related where normative_id = %s',(id,))

        relateds = []
        for r in cur:
            relateds.append(self._convertRelatedToDict(r))

        return relateds
        
    # -----------------------------------------------------------------------------------
    # --------------------- VISIBILIDAD DE LA NORMATIVA ---------------------------------
    # -----------------------------------------------------------------------------------

    '''
        Una normativa solo tiene una visibilidad, no se mantiene historial de los cambios realizados sobre la misma
        TYPE: PUBLIC, PRIVATE(Default), GROUPPRIVATE
        ADDITIONAL_DATA: son los ids separados por coma de las oficinas
    '''
    def _convertVisibilityToDict(self,v):
        return {'id':v[0],'normative_id':v[1],'type':v[2],'additional_data':v[3]}


    def getVisibility(self,con,normative_id):
        cur = con.cursor()
        cur.execute('select id,normative_id,type,additional_data from digesto.visibility where normative_id =  %s',(normative_id,))
        if cur.rowcount <= 0:
            return None
        return self._convertVisibilityToDict(cur.fetchone())

    def persistVisibility(self,con,normative_id,type='PRIVATE',additional_data=''):

        if 'normative_id' is None:
            return

        cur = con.cursor()

        visibility = self.getVisibility(con,normative_id)
        if visibility is None:
            id = str(uuid.uuid4())
            params = (normative_id,type,additional_data,id)
            cur.execute('insert into digesto.visibility (normative_id,type,additional_data,id) values(%s,%s,%s,%s)',params)

        else:
            params = (type,additional_data,visibility['id'])
            cur.execute('update digesto.visibility set type = %s, additional_data = %s where id = %s',params)

    # -----------------------------------------------------------------------------------
    # -------------------------------- NORMATIVA ----------------------------------------
    # -----------------------------------------------------------------------------------

    def _convertNormativeToDict(self,norm, status, visibility, relateds):
        return {'id':norm[0],'issuer_id':norm[1],'file_id':norm[2],'type':norm[3],'file_number':norm[4],'normative_number':norm[5],'year':norm[6],'created':norm[7],'creator_id':norm[8],'extract':norm[9],'status':status,'visibility':visibility,'relateds':relateds}



    def createNormative(self,con,normative,status,visibility,relateds,file):





    def createStateNormative(con,state):
        if state is None:
            return

        if ('state' not in state or state['state'] is None or
            'creator_id' not in state or state['creator_id'] is None or
            'normative_id' not in state or state['normative_id'] is None):
            return


        cur = con.cursor()

        idState = str(uuid.uuid4())
        params = (idState,
                  state['state'],
                  state['created'] if 'created' in state and state['created'] is not None else datetime.datetime.now(),
                  state['creator_id'],
                  state['normative_id'])

        cur.execute('insert into digesto.state_normative (id,state,created,creator_id,normative_id) values(%s,%s,%s,%s,%s)',params)


    def _createNormative(self,con,normative):
        id = str(uuid.uuid4())

        params = (id,
                  normative['issuer_id'],
                  normative['file_id'] if 'file_id' in normative else None,
                  normative['type'] if 'type' in normative else None,
                  normative['file_number'],
                  normative['normative_number']
                  normative['year'] if 'year' in normative and normative['year'] is not None else datetime.datetime.now(),
                  normative['created'] if 'created' in normative and normative['created'] is not None else datetime.datetime.now(),
                  normative['creator_id'],
                  normative['extract'] if 'extract' in normative else '')

        cur = con.cursor
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into digesto.normative (id,issuer_id,file_id,type,file_number,normative_number,date,created,creator_id,extract) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,)',params)

        if 'state' in normative and normative['state'] is not None and 'state' in normative['state']:
            state = normative['state']
            state['creator_id'] = normative['creator_id']
            state['normative_id'] = id
            self.createStateNormative(con,state)

        if 'visibility' in normative and normative['visibility'] is not None:
            visibility = normative['visibility']
            visibility['normative_id'] = id
            self._persistVisibility(con,visibility)

        if 'relateds' in normative:
            # agrego los relacionados

    #  -------------- falta implemntar ---------------------
    def _updateNormative(con,normative):


    def persist(self,con,normative):
        if normative is None:
            return
        '''
        chequeo precondiciones, campos obligatorios
        '''
        if ('issuer_id' not in normative or normative['issuer_id'] is None or
            'file_number' not in normative or normative['file_number'] is None
            'normative_number' not in normative or normative['normative_number'] is None
            'creator_id' not in normative or normative['creator_id'] is None):

            return

        if 'id' not in normative:
            self._createNormative(con,normative)
        else:
            self._updateNormative(con,normative)


    # falta implementar
    def findNormativeById(con,id):


    # falta implementar
    def removeAllRelated(con,id):


    # falta implementar
    def addRelated(con,related):


    # falta implementar
    def stateUpdate(con,state):


    # falta implementar
    def changeVisibility(con,visibility):


    # falta implementar
    def deleteNormative(con,id):


    # falta implementar
    def changeFileToNormative(con,file,normative):
