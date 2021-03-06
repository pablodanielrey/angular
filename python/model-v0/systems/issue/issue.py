# -*- coding: utf-8 -*-
import uuid, datetime,psycopg2,inject
from model.systems.offices.offices import Offices
from model.systems.assistance.date import Date

class Issue:

    date = inject.attr(Date)
    offices = inject.attr(Offices)

    # -----------------------------------------------------------------------------------
    # ---------------- VISIBILIDAD DE LOS PEDIDOS QUE PUEDO VER -------------------------
    # -----------------------------------------------------------------------------------
    '''
    issues.visibility_group_owner {
        id VARCHAR NOT NULL PRIMARY KEY,
        request_id VARCHAR NOT NULL REFERENCES issues.request(id),
        office_id VARCHAR NOT NULL REFERENCES offices.offices (id),
        created TIMESTAMPTZ NOT NULL default now(),
        tree boolean default true
    }
    '''
    def _convertVisibilityOfficeToDict(self,visibility,type='OFFICE'):
        return {'id':visibility[0],'issue_id':visibility[1],'office_id':visibility[2],'created':visibility[3],'tree':visibility[4],'type':type}


    def getVisibilitiesOfficesView(self,con,issue_id):
        cur = con.cursor()
        cur.execute('select id,request_id,office_id,created,tree from issues.visibility_group_owner where request_id = %s',(issue_id,))
        if cur.rowcount <= 0:
            return []
        visibilities = []
        for v in cur:
            visibilities.append(self._convertVisibilityOfficeToDict(v))
        return visibilities

    '''
        obtiene los issues_id que puede ver la oficina office_id
    '''
    def findIssuesByOffice_View(self,con,office_id):
        ids = []
        cur = con.cursor()
        cur.execute('select DISTINCT request_id from issues.visibility_group_owner where office_id = %s',(office_id,))
        for i in cur:
            ids.append(i[0])
        return ids


    def removeVisibilityOffice_View(self,con,id):
        if id is None:
            return
        cur = con.cursor()
        cur.execute('delete from issues.visibility_group_owner where id = %s',(id,))

    def removeAllVisibilityOffice_View(self,con,issue_id):
        if id is None:
            return
        cur = con.cursor()
        cur.execute('delete from issues.visibility_group_owner where request_id = %s',(issue_id,))


    def createVisibilityOffice_View(self,con,issue_id,office_id,tree=True,created=None):
        if issue_id is None or office_id is None:
            return None

        cur = con.cursor()

        id = str(uuid.uuid4())
        if created is None:
            created = self.date.now()
        if tree is None:
            tree = True

        createdUtc = self.date.awareToUtc(created)
        params = (id,issue_id,office_id,created,tree)

        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into issues.visibility_group_owner (id,request_id,office_id,created,tree) values(%s,%s,%s,%s,%s)',params)

        return id


    # -----------------------------------------------------------------------------------
    # -------------------------- ESTADO DEL PEDIDO --------------------------------------
    # -----------------------------------------------------------------------------------
    def _convertStateToDict(self,state):
        return {'created':state[0],'state':state[1],'creator':state[2]}

    '''
        Obtiene el ultimo estado del pedido
    '''
    def getState(self,con,issue_id):
        cur = con.cursor()
        cur.execute('select created,state,user_id from issues.state where request_id = %s order by created desc limit 1',(issue_id,))
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

        createdUtc = self.date.awareToUtc(created)
        params = (state,createdUtc,creator_id,issue_id)

        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into issues.state (state,created,user_id,request_id) values(%s,%s,%s,%s)',params)

    # -----------------------------------------------------------------------------------
    # --------------------------------- PEDIDO ------------------------------------------
    # -----------------------------------------------------------------------------------

    def _convertToDict(self,issue,state,visibilities):
        return {'id':issue[0],'created':issue[1],
                'request':issue[2],'creator':issue[3],
                'parent_id':issue[4],'assigned_id':issue[5],
                'priority':issue[6],'office_id':issue[7],
                'visibilities':visibilities,'state':state['state']}


    def _getParamsPersistIssue(self, issue, id, userId):
        return   (issue['created'],
                  issue['request'] if 'request' in issue and issue['request'] is not None else '',
                  userId,
                  issue['parent_id'] if 'parent_id' in issue else None,
                  issue['assigned_id'] if 'assigned_id' in issue else None,
                  issue['priority'] if 'priority' in issue and issue['priority'] is not None else 0,
                  issue['office_id'],
                  id
                 )

    '''
        Crea un nuevo issue
        visibilities = [{'type':OFFICE|USER},'office_id':id office o 'user_id' si es USER,'tree':True]
    '''
    def create(self,con,issue,userId,visibilities,state='PENDING'):
        if issue is None or userId is None or visibilities is None or 'office_id' not in issue:
            return None


        id = str(uuid.uuid4())

        if 'created' in issue and issue['created'] is not None:
            issue['created'] = self.date.parse(issue['created'])
        else:
            issue['created'] = self.date.now()

        params = self._getParamsPersistIssue(issue,id,userId)

        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('insert into issues.request (created,request,requestor_id,related_request_id,assigned_id,priority,office_id,id) values(%s,%s,%s,%s,%s,%s,%s,%s)',params)

        self.updateState(con,id,userId,issue['created'],state)

        for v in visibilities:
            if v['type'] == 'OFFICE':
                self.createVisibilityOffice_View(con,id,v['office_id'],v['tree'])
        return id

    '''
        Actualiza el issuer
    '''
    def updateData(self,con,issue,userId):
        if issue is None or userId is None or 'id' not in issue or issue['id'] is None:
            return None

        params = (userId,
                  issue['parent_id'] if 'parent_id' in issue else None,
                  issue['assigned_id'] if 'assigned_id' in issue else None,
                  issue['priority'] if 'priority' in issue and issue['priority'] is not None else 0,
                  issue['office_id'],
                  issue['id']
                 )

        cur = con.cursor()
        cur.execute('set timezone to %s',('UTC',))
        cur.execute('update issues.request set requestor_id = %s, related_request_id = %s, assigned_id = %s, priority = %s, office_id = %s where id = %s',(params))

        # actualizo el estado
        if 'state' in issue and issue['state'] is not None:
            state = issue['state']
            self.updateState(con,issue['id'],userId,None,state)

        # elimino la visibilidad que ya posee
        self.removeAllVisibilityOffice_View(con,issue['id'])
        # actualizo la visibilidad
        for v in issue['visibilities']:
            if v['type'] == 'OFFICE':
                self.createVisibilityOffice_View(con,issue['id'],v['office_id'],v['tree'])

        return issue['id']


    '''
        Elimina el issue y sus hijos
    '''
    def delete(self,con,id):
        if id is None:
            return None

        childrens = self._getChildrens(con,id)
        if len(childrens) > 0:
            for child in childrens:
                self.delete(con,child['id'])

        cur = con.cursor()
        # elimino los estados
        cur.execute('delete from issues.state where request_id = %s',(id,))
        # elimino la visibilidad
        self.removeAllVisibilityOffice_View(con,id)
        # elimino los issues
        cur.execute('delete from issues.request where id = %s',(id,))

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
        cur.execute('select id,created,request,requestor_id,related_request_id,assigned_id,priority,office_id from issues.request where related_request_id = %s',(id,))
        if cur.rowcount <= 0:
            return []


        for cIss in cur:
            cId = cIss[0]
            state = self.getState(con,cId)
            visibilities = self.getVisibilitiesOfficesView(con,cId)
            obj = self._convertToDict(cIss,state,visibilities)
            obj['childrens'] = self._getChildrens(con,cId)
            childrens.append(obj)

        return childrens



    def _includeIssue(self,issue_id,issues):
        for iss in issues:
            if iss['id'] == issue_id:
                return True
            if self._includeIssue(issue_id,iss['childrens']):
                return True
        return False

    '''
        Retorna todas las issues solicitadas por el usuario
    '''
    def getIssues(self,con,userId):
        if userId is None:
            return None

        cur = con.cursor()

        # ---- issues por visibilidad de oficina -----
        offices = self.offices.getOfficesByUser(con,userId,True)
        issues = []
        for o in offices:
            aux = self.findIssuesByOffice_View(con,o['id'])
            for i in aux:
                issues.append(self.findIssue(con,i))
            issues.extend(self._getIssuesByParentsOffice(con,o['parent']))
        issuesRet = []
        while len(issues) > 0:
            issue = issues[0]
            issues.remove(issue)
            if not self._includeIssue(issue['id'],issues) and not self._includeIssue(issue['id'],issuesRet):
                issuesRet.append(issue)
        # self.filterIssuesByVisibilityOffices(issues,offices)
        return issuesRet

    # obtiene los issues de la oficina y de todos los padres que tengan el tree como true
    def _getIssuesByParentsOffice(self,con,officeId):
        issues = []
        if officeId is None:
            return issues

        office = self.offices.findOffice(con,officeId)
        cur = con.cursor()
        cur.execute('select DISTINCT request_id from issues.visibility_group_owner where office_id = %s and tree = true',(officeId,))
        for i in cur:
            issue = self.findIssue(con,i[0])
            issue['readOnly'] = True
            issues.append(issue)

        issues.extend(self._getIssuesByParentsOffice(con,office['parent']))
        return issues

    def filterIssuesByVisibilityOffices(self,issues,offices):
        removeIssues = []
        for issue in issues:
            for v in issue['visibilities']:
                if self._includeOffices(v['office_id'],offices):
                    break
            else:
                removeIssues.append(issue)
                continue
            self.filterIssuesByVisibilityOffices(issue['childrens'],offices)

        for i in removeIssues:
            issues.remove(i)

    def _includeOffices(self,id,offices):
        for o in offices:
            if o['id'] == id:
                return True
        return False

    def findIssue(self,con,id):
        cur = con.cursor()
        cur.execute('select id,created,request,requestor_id,related_request_id,assigned_id,priority,office_id from issues.request where id = %s',(id,))
        issue = cur.fetchone()
        if issue:
            state = self.getState(con,issue[0])
            visibilities = self.getVisibilitiesOfficesView(con,issue[0])
            obj = self._convertToDict(issue,state,visibilities)
            childrens = self._getChildrens(con,issue[0])
            obj['childrens'] = childrens
            return obj
        else:
            return None

    def _include(self,issue,issue2):
        if issue['id'] == issue2['id']:
            return True

        for iss in issue2['childrens']:
            if self._include(issue,iss):
                return True

        return False


    '''
        Retorna todas las issues asignadas al usuario
    '''
    def getIssuesAdmin(self,con,userId):
        if userId is None:
            return None

        cur = con.cursor()

        # ---- issues asignadas a la oficina del usuario -----
        offices = self.offices.getOfficesByUser(con,userId,True)
        issues = []
        for o in offices:
            iss = self.findIssuesByOffice(con,o['id'])
            issues.extend(iss)
        issuesRet = []
        while len(issues) > 0:
            issue = issues[0]
            issues.remove(issue)
            if not self._includeIssue(issue['id'],issues) and not self._includeIssue(issue['id'],issuesRet):
                issuesRet.append(issue)
        # self.filterIssuesByVisibilityOffices(issues,offices)
        return issuesRet


    def findIssuesByOffice(self,con,officeId):
        if officeId is None:
            return []

        cur = con.cursor()
        cur.execute('select id,created,request,requestor_id,related_request_id,assigned_id,priority,office_id from issues.request where office_id = %s',(officeId,))
        if cur.rowcount <= 0:
            return []

        issues = []
        for issue in cur:
            state = self.getState(con,issue[0])
            visibilities = self.getVisibilitiesOfficesView(con,issue[0])
            obj = self._convertToDict(issue,state,visibilities)
            childrens = self._getChildrens(con,issue[0])
            obj['childrens'] = childrens
            issues.append(obj)

        return issues
