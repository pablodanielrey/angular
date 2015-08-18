# -*- coding: utf-8 -*-
import uuid, datetime,psycopg2,inject
from model.systems.files.files import Files
from model.systems.offices.offices import Offices
from model.systems.assistance.date import Date

class Digesto:

    date = inject.attr(Date)
    file = inject.attr(Files)
    offices = inject.attr(Offices)
    '''
        Tipos de normativa:
        ordenanza => ordinance
        resolución => resolution
        disposicion => regulation
    '''
    issuers = {
        'REGULATION':[
                '0bf25a58-15b0-40cc-861c-789480728d79',
                '2d0e035b-7cbd-4008-a3bc-13f101478de3',
                '47e03cc7-6c6e-425b-ad9b-f2fa60b2b2a1',
                '7ed358ce-208f-409f-99ca-96f971aa5400',
                '79a1ac02-70fb-487d-9727-2771aff2c5f5',
                '769ca706-c5e7-4b76-b16a-cec933cfb4f3',
                '9ad5cdaf-a323-4c88-a030-cf901ffe341f',
                'f34f0917-f1af-4cbc-8ce8-e4b6dfd77b5d',
                'a645e297-cc8e-43eb-a0a9-ce3484cc80d6'
                ],
        'RESOLUTION':[
                '0bf25a58-15b0-40cc-861c-789480728d79',
                'a07fbca6-d068-4bfb-94d7-9699d864d4c3'
                ],
        'ORDINANCE':[
                '0bf25a58-15b0-40cc-861c-789480728d79',
                'a07fbca6-d068-4bfb-94d7-9699d864d4c3'
            ]
        }

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
    def updateStatus(self,con,normative_id,creator_id,created,status='PENDING'):
        if normative_id is None or creator_id is None:
            return

        cur = con.cursor()

        id = str(uuid.uuid4())
        if created is None:
            created = self.date.now()

        createdUtc = self.date.awareToUtc(created)
        params = (id,status,createdUtc,creator_id,normative_id)

        cur.execute('set timezone to %s',('UTC',))
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
        adStr = v[3]
        additional_data  = adStr.split(',')
        return {'id':v[0],'normative_id':v[1],'type':v[2],'additional_data':additional_data}


    def getVisibility(self,con,normative_id):
        cur = con.cursor()
        cur.execute('select id,normative_id,type,additional_data from digesto.visibility where normative_id =  %s',(normative_id,))
        if cur.rowcount <= 0:
            return None
        return self._convertVisibilityToDict(cur.fetchone())

    def persistVisibility(self,con,normative_id,type='PRIVATE',additional_data=''):

        if 'normative_id' is None:
            return

        if type is None:
            type = 'PRIVATE'

        additional_dataStr = ''
        if additional_data is not None:
            i = 0
            for a in additional_data:
                if i != 0:
                    additional_dataStr = additional_dataStr + ','
                additional_dataStr = additional_dataStr + a
                i = i +1

        cur = con.cursor()

        visibility = self.getVisibility(con,normative_id)
        if visibility is None:
            id = str(uuid.uuid4())
            params = (normative_id,type,additional_dataStr,id)
            cur.execute('insert into digesto.visibility (normative_id,type,additional_data,id) values(%s,%s,%s,%s)',params)

        else:
            params = (type,additional_dataStr,visibility['id'])
            cur.execute('update digesto.visibility set type = %s, additional_data = %s where id = %s',params)

    # -----------------------------------------------------------------------------------
    # -------------------------------- NORMATIVA ----------------------------------------
    # -----------------------------------------------------------------------------------

    def _convertNormativeToDict(self,norm, status, visibility, relateds):
        return {'id':norm[0],'issuer_id':norm[1],'file_id':norm[2],'type':norm[3],'file_number':norm[4],'normative_number':norm[5],'year':norm[6],'created':norm[7],'creator_id':norm[8],'extract':norm[9],'status':status,'visibility':visibility,'relateds':relateds}



    def createNormative(self,con,normative,status,visibility,relateds,file,userId):

        if normative is None:
            return None

        '''
        chequeo precondiciones, campos obligatorios
        '''
        if ('issuer_id' not in normative or normative['issuer_id'] is None or
            'file_number' not in normative or normative['file_number'] is None or
            'normative_number_full' not in normative or normative['normative_number_full'] is None or
            userId is None):

            return None

        # tengo que hacer el split de normative['normative_number_full']
        array = normative['normative_number_full'].split('/')
        if len(array) != 2:
            return None

        # creo el normative['normative_number']
        normative['normative_number'] = array[0]
        # creo el normative['year']
        today = self.date.now()
        normative['year'] = self.date.now()
        yearStr = array[1]
        yearToday = int(today.strftime('%y'))
        if int(yearStr) > yearToday:
          year = 1900 + int(yearStr)
        else:
          year = 2000 + int(yearStr)

        normative['year'] = normative['year'].replace(year=year)

        id = str(uuid.uuid4())

        # creo el archivo
        fileId = None
        if file is not None:
            fileId = self.file.persist(con,file)

        if 'created' in normative and normative['created'] is not None:
            normative['created'] = self.date.parse(normative['created'])
        else:
            normative['created'] = self.date.now()
        params = (id,
                  normative['issuer_id'],
                  fileId,
                  normative['type'] if 'type' in normative else None,
                  normative['file_number'],
                  normative['normative_number'],
                  normative['year'] if 'year' in normative and normative['year'] is not None else self.date.now(),
                  normative['created'],
                  userId,
                  normative['extract'] if 'extract' in normative else '')

        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into digesto.normative (id,issuer_id,file_id,type,file_number,normative_number,date,created,creator_id,extract) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',params)

        created = normative['created']
        d2 = created - datetime.timedelta(seconds=1)
        self.updateStatus(con,id,userId,d2)
        if status is not None and status != 'PENDING':
            self.updateStatus(con,id,userId,created,status)

        if visibility is None:
            self.persistVisibility(con,id)
        else:
            type = visibility['type'] if 'type' in visibility else None
            additional_data = visibility['additional_data'] if 'additional_data' in visibility else None
            self.persistVisibility(con,id,type,additional_data)

        if relateds is not None:
            self.addRelateds(con,relateds,userId,id)

        return id

    def updateNormative(self,con,normative,file=None,visibility=None):
        if normative is None:
            return

        '''
        chequeo precondiciones, campos obligatorios
        '''
        if ('id' not in normative or normative['id'] is None or
            'issuer_id' not in normative or normative['issuer_id'] is None or
            'file_number' not in normative or normative['file_number'] is None or
            'normative_number' not in normative or normative['normative_number'] is None or
            'creator_id' not in normative or normative['creator_id'] is None or
            'status' not in normative or normative['status'] is None):

            return

        id = normative['id']

        # busca la normativa en la bd
        oldNormative = self.findNormativeById(con,id)
        if oldNormative is None:
            return

        # actualizo el archivo en caso de que sea necesario
        fileId = normative['file_id']
        if file is not None:
            if 'id' not in file:
                fileId = self.file.persist(con,file)
            elif file['id'] != fileId:
                fileId = file['id']


        # actualizo la normativa
        params = (normative['issuer_id'],
                  fileId,
                  normative['type'] if 'type' in normative else None,
                  normative['file_number'],
                  normative['normative_number'],
                  normative['year'] if 'year' in normative and normative['year'] is not None else datetime.datetime.now(),
                  normative['created'] if 'created' in normative and normative['created'] is not None else datetime.datetime.now(),
                  normative['creator_id'],
                  normative['extract'] if 'extract' in normative else '',
                  id)

        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('update from digesto.normative set issuer_id = %s,file_id = %s,type = %s,file_number = %s,normative_number = %s,date = %s,created = %s,creator_id = %s, extract = %s where id = %s',params)

        # actualizo el estado en caso de ser necesario
        status = normative['status']
        s = self.getStatus(con,id)
        if s is None or s['status'] != status['status']:
            self.updateStatus(con,id,normative['creator_id'],status['status'])

        # actualizo la visibilidad
        if visibility is not None:
            self.persistVisibility(con,id,visibility['type'],visibility['additional_data'])



    def findNormativeById(self,con,id):
        cur = con.cursor()
        cur.execute('select id,issuer_id,file_id,type,file_number,normative_number,date,created,creator_id,extract from digesto.normative where id = %s',(id,))
        if (cur.rowcount <= 0):
            return None
        else:
            status = self.getStatus(con,id)
            visibility = self.getVisibility(con,id)
            relateds = self.findRelateds(con,id)

            normative = self._convertNormativeToDict(cur.fetchone(),status, visibility, relateds)

            normative['issuer'] = self.offices.findOffice(con,normative['issuer_id'])
            yearStr = normative['year'].strftime('%y')
            normative['normative_number_full'] = normative['normative_number'] + '/' + yearStr[-2:]

            return normative


    def deleteNormative(self,con,id):
        if id is None:
            return

        normative = self.findNormativeById(con,id)
        if normative is None:
            return

        fileId = normative['file_id']

        cur = con.cursor()
        # elimino el archivo
        if fileId is not None:
            self.file.delete(con,fileId)
        # elimino el estado
        cur.execute('delete from digesto.status where normative_id = %s',(id,))
        # elimino la visibilidad
        cur.execute('delete from digesto.visibility where normative_id = %s',(id,))
        # elimino los relacionados
        cur.execute('delete from digesto.related where normative_id = %s',(id,))
        # elimino la normativa
        cur.execute('delete from digesto.normative where id = %s',(id,))


    # -----------------------------------------------------------------------------------
    # ---------------------------------- OTROS ------------------------------------------
    # -----------------------------------------------------------------------------------

    '''
        Retorna los tipos de emisores posibles de acuerdo al tipo de normativa: ORDINANCE | RESOLUTION | REGULATION
    '''
    def loadIssuers(self,con,type):
        if type is None:
            return []
        ids = self.issuers.get(type, [])
        offices = []
        for id in ids:
            office = self.offices.findOffice(con,id)
            if office is not None:
                offices.append(office)
        return offices


    # -----------------------------------------------------------------------------------
    # ---------------------------- BUSQUEDA DE NORMATIVAS -------------------------------
    # -----------------------------------------------------------------------------------

    '''
        Busca las normativas por numero de expediente
    '''
    def _findNormativeByNormativeNumber(self,con,number):
        cur = con.cursor()
        cur.execute('select id from digesto.normative where normative_number like %s',('%' + number + '%',))
        data = cur.fetchall()
        normatives = []
        for d in data:
            n = self.findNormativeById(con,d[0])
            normatives.append(n)
        return normatives

    '''
        Busca las normativas por el extracto
    '''
    def _findNormativeByExtract(self,con,extract):
        cur = con.cursor()
        cur.execute('select id from digesto.normative where extract like %s',('%' + extract + '%',))
        data = cur.fetchall()
        normatives = []
        for d in data:
            n = self.findNormativeById(con,d[0])
            normatives.append(n)
        return normatives

    '''
        Retorna las normativas con posean el texto
    '''
    def findNormative(self,con,text,filters):
        # busco por nro de expediente
        array = text.split('/')
        normatives = self._findNormativeByNormativeNumber(con,array[0])
        # si no encontro nada busco por el extracto
        if len(normatives) == 0:
            normatives = self._findNormativeByExtract(con,text)
        # si no encontro nada busco por el contenido del archivo

        return normatives
