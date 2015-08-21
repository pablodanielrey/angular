# -*- coding: utf-8 -*-
import uuid, datetime,psycopg2,inject
from model.systems.offices.offices import Offices
from model.systems.assistance.date import Date

class Issue:

    date = inject.attr(Date)
    offices = inject.attr(Offices)

    # -----------------------------------------------------------------------------------
    # -------------------------- ESTADO DEL PEDIDO --------------------------------------
    # -----------------------------------------------------------------------------------
    def _convertStateToDict(self,state):
        return {'created':state[0],'state':state[1],'creator':state[2]}

    '''
        Obtiene el ultimo estado del pedido
    '''
    def getState(self,con,issue_id):
        cur = con.cursor
        cur.execute('select created,state,user_id from issues.request where request_id = %s order by created desc limit 1',(issue_id,))
        if cur.rowcount <= 0:
            return None
        return self._convertStateToDict(cur.fetchone())

    '''
        Crea un nuevo estado, por defecto lo pone como ...
    '''
    def updateState(self,con,issue_id,creator_id,created,state='PENDING'):
        if issue_id is None or creator_id is None:
            return

        cur = con.cursor()

        if created is None:
            created = self.date.now()

        createdUtc = self.date.awareUtc(created)
        params = (state,cratedUtc,creator_id,issue_id)

        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into (state,created,user_id,request_id) values(%s,%s,%s,%s)',params)

    # -----------------------------------------------------------------------------------
    # --------------------------------- PEDIDO ------------------------------------------
    # -----------------------------------------------------------------------------------

    def _convertToDict(self,issue,state):
        return {'id':issue[0],'created':issue[1],
                'request':issue[2],'creator':issue[3],
                'office_id':issue[4],'parent_id':issue[5],
                'assigned_id':issue[6],'priority':issue[7],
                'visibility':issue[8],'state':state}


    def _getParamsPersistIssue(self, issue, id, userId):
        return   (issue['created'],
                  issue['request'] if 'request' in issue and issue['request'] is not None else '',
                  userId,
                  issue['office_id'],
                  issue['parent_id'] if 'parent_id' in issue else None,
                  issue['assigned_id'] if 'assigned_id' in issue else None,
                  issue['priority'] if 'priority' in issue and issue['priority'] is not None else 0,
                  issue['visibility'] if 'visibility' in issue and issue['visibility'] is not None else 'AUTHENTICATED',
                  id
                 )

    '''
        Crea un nuevo issue
    '''
    def create(self,con,issue,userId):
        if issue is None or userId is None:
            return None

        '''
            chequeo precondiciones
        '''
        if 'office_id' not in issue or issue['office_id'] is None:
            return None

        id = str(uuid.uuid4())

        if 'created' in issue and issue['created'] is not None:
            issue['created'] = self.date.parse(issue['created'])
        else:
            issue['created'] = self.date.now()

        params = self._getParamsPersistIssue(issue,id,userId)

        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into issues.request (created,request,requestor_id,office_id,related_request_id,assigned_id,priority,visibility,id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',params)

        self.updateState(con,id,userId,issue['created'])

        return id

    '''
        Actualiza el issuer
    '''
    def updateData(self,con,issue,userId):
        if issue is None or userId is None or 'id' not in issue or issue['id'] is None:
            return None

        params = self._getParamsPersistIssue(issue,issue['id'],userId)

        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('update issues.request')

        # actualizo el estado
        if 'state' in issue and issue['state'] is not None:
            state = issue['state']
            self.updateState(con,issue['id'],userId,state['created'],state['state'])

        return issue['id']

    '''
        Elimina el issue y sus hijos
    '''
    def delete(self,con,id):
        if id is None:
            return None

        childrens = self_getChildrens(con,id)
        ids = list(map(lambda x : x['id'],childrens))
        ids.append(id)
        cur = con.cursor()
        # elimino los estados
        cur.execute('delete from issues.state where request_id in %s',(tuple(ids),))
        # elimino los issues
        cur.execute('delete from issues.request where id in %s',(tuple(ids),))

        return True


    '''
        Obtiene los hijos
    '''
    def _getChildrens(self,con,id):
        if id is None:
            return []

        pids = []
        pids.append(id)
        childrens = []

        cur = con.cursor()
        cur.execute('select id,created,request,requestor_id,office_id,related_request_id,assigned_id,priority,visibility from issues.request where related_request_id = %s',(issueId,))
        if cur.rowcount <= 0:
            return []


        for cIss in cur:
            cId = cIss[0]
            state = self.getState(con,cId)
            obj = self._convertToDict(con,cIss,state)
            obj['childrens'] = self._getChildrens(con,cId)
            childrens.append(obj)

        return childrens




    '''
        Retorna todas las issues solicitadas por el usuario o aquellas cuyo responsable es el usuario
    '''
    def getIssues(self,con,userId):
        if userId is None:
            return None

        cur = con.cursor()
        cur.execute('select id,created,request,requestor_id,office_id,related_request_id,assigned_id,priority,visibility from issues.request where requestor_id  = %s or assigned_id = %s',(userId,userId))
        issues = []
        ids = []
        # elimino los repetidos y los convierto a diccionario
        for issue in cur:
            if issue[0] in ids:
                continue

            ids.append(issue[0])
            state = self.getState(con,issue[0])
            obj = self._convertToDict(con,issue,state)
            childrens = self._getChildrens(con,issue[0])
            obj['childrens'] = childrens
            issues.append(obj)

        ret = []
        for issue in issues:
            include = False
            for aux in issues:
                if aux['id'] != issue['id'] and self._include(issue,aux):
                    include = True
                    continue
            if not include:
                ret.append(issue)

        return ret


    def _include(self,issue,issue2):
        if issue['id'] == issue2['id']:
            return True

        for iss in issue2['childrens']:
            if self._include(issue,iss):
                return True

        return False
