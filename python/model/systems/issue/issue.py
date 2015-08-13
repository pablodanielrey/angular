# -*- coding: utf-8 -*-
import uuid
import pytz
from model.systems.assistance.date import Date

class Issue:

    '''
     ' Insertar datos, se insertan los datos del request y el estado
     '''
    def insert(self,con,request,officeId,requestorId,created,priority,visibility,relatedRequestId, state):
        createdutc = created.astimezone(pytz.utc)

        id = str(uuid.uuid4()) 
        cur = con.cursor() 
        cur.execute('set timezone to %s',('UTC',))
        cur.execute("""
            INSERT INTO issues.request (id, request, office_id, requestor_id, created, priority, visibility, related_request_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """,(id, request, officeId, requestorId, createdutc, priority, visibility, relatedRequestId))
        
        cur.execute("""
            INSERT INTO issues.state (state, created, user_id, request_id)
            VALUES (%s, %s, %s, %s);
        """,(state, createdutc, requestorId, id))
        
        events = []
        e = { 
            'type':'IssueInsertedEvent', 
            'data':{ 
               'id':id, 
               'request':request,
               'officeId':officeId,
               'requestorId':requestorId,
               'created':createdutc,
               'priority':priority,
               'visibility':visibility,
               'relatedRequestId':relatedRequestId,
               'state':state,
               'nodes':[],
             } 
        }
        events.append(e)
        return events 
        
    '''
     ' Obtener peticiones relacionadas en funcion de los ids
     '''
    def __getIssuesRelated(self, con, ids, relatedRequestIds):
        cur = con.cursor()
        cur.execute('''
          SELECT r.id, r.created, r.request, r.requestor_id, r.office_id, r.related_request_id, r.assigned_id, r.priority, r.visibility, s.state
          FROM issues.request AS r
          INNER JOIN issues.state AS s ON (r.id = s.request_id)
          INNER JOIN (
            SELECT request_id, max(created) AS created 
            FROM issues.state
            GROUP BY request_id
          ) AS s2 ON (s.request_id = s2.request_id AND s.created = s2.created)
          WHERE ((r.related_request_id = ANY(%s)) OR (r.related_request_id = ANY(%s))) AND NOT (r.id = ANY(%s))
          ORDER BY r.created ASC;
        ''', (ids, relatedRequestIds, ids))
        print(cur.query)
        
        issues = []  
        ids = []
        relatedRequestIds = []
        for issue in cur: 
            ids.append(issue[0])
            if issue[5] != None:
              relatedRequestIds.append(issue[5])
            issues.append( 
                { 
                    'id':issue[0], 
                    'created':issue[1], 
                    'request':issue[2], 
                    'requestor_id':issue[3], 
                    'office_id':issue[4],
                    'related_request_id':issue[5],
                    'assigned_id':issue[6],
                    'priority':issue[7],
                    'visibility':issue[8],
                    'state':issue[9],
                } 
            )
        
        return {
          "ids":ids,
          "relatedRequestIds":relatedRequestIds,
          "issues":issues
        }
            

    '''
     ' Obtener peticiones asociadas a un determinado usuario
     '''
    def getIssuesByUser(self, con, userId):
        ids = []
        relatedRequestIds = []
        
        cur = con.cursor() 
        cur.execute('''
          SELECT r.id, r.created, r.request, r.requestor_id, r.office_id, r.related_request_id, r.assigned_id, r.priority, r.visibility, s.state
          FROM issues.request AS r
          INNER JOIN issues.state AS s ON (r.id = s.request_id)
          INNER JOIN (
            SELECT request_id, max(created) AS created 
            FROM issues.state
            GROUP BY request_id
          ) AS s2 ON (s.request_id = s2.request_id AND s.created = s2.created)
          WHERE r.requestor_id = %s OR r.assigned_id = %s
          ORDER BY r.created ASC;
        ''', (userId, userId)) 
        if cur.rowcount <= 0: 
            return [] 
        

        issues = []         
        ids = []
        relatedRequestIds = []
        for issue in cur: 
            ids.append(issue[0])
            if issue[5] != None:
              relatedRequestIds.append(issue[5])
            issues.append( 
                { 
                    'id':issue[0], 
                    'created':issue[1], 
                    'request':issue[2], 
                    'requestor_id':issue[3], 
                    'office_id':issue[4],
                    'related_request_id':issue[5],
                    'assigned_id':issue[6],
                    'priority':issue[7],
                    'visibility':issue[8],
                    'state':issue[9],
                } 
            )

        while True:
       
          
          data = self.__getIssuesRelated(con, ids, relatedRequestIds)
          print(data)
          
          if(len(data["ids"]) == 0):
            break;
            
          ids = list(set(ids + data["ids"]))
          relatedRequestIds = data["relatedRequestIds"]
          issues = issues + data["issues"]
         
        return issues;
        
        
    
    
    '''
     ' Eliminar peticion y sus hijos
     '''
    def deleteIssue(self, con, id):
        self.__deleteIssue(con, id)
        events = []
        e = {
            'type':'IssueDeletedEvent', 
            'data':id, 
        }
        events.append(e)
        return events
    
    '''
     ' Metodo recursivo de eliminacion de peticiones y sus hijos
     '''
    def __deleteIssue(self, con, id):
        cur = con.cursor()
        cur.execute('''
          SELECT r.id
          FROM issues.request AS r
          WHERE r.related_request_id = %s
          ORDER BY r.created ASC;
        ''',(id,))
    
        for issue in cur:
            self.__deleteIssue(con, issue[0])

        cur.execute('''
          DELETE FROM issues.state
          WHERE request_id = %s
        ''',(id,))       

        cur.execute('''
          DELETE FROM issues.request
          WHERE id = %s
        ''',(id,))       
         
        
        
    
    '''
     ' Actualizar los datos de un pedido, solo los datos y no las relaciones
     '''
    def updateData(self,con,id,request,priority,visibility,state,userId):
        cur = con.cursor()

        cur.execute("""
            UPDATE issues.request SET request = %s, priority = %s, visibility = %s
            WHERE issues.request.id = %s;
        """,(request, priority, visibility, id))
             
       
        cur.execute('''
          SELECT state
          FROM issues.state AS r
          WHERE r.request_id = %s
          ORDER BY created DESC
          LIMIT 1
        ''',(id,))
        
        oldState = None
        
        for issue in cur:
            oldState = issue[0]
        
        if(oldState != state):
            cur.execute('set timezone to %s',('UTC',))
            
            cur.execute("""
            INSERT INTO issues.state (created, state, user_id, request_id)
            VALUES (now(), %s, %s, %s);
        """,(state, userId, id))
        
        
        events = []
        e = { 
            'type':'IssueUpdatedData', 
            'data':{ 
               'id':id, 
               'request':request,
               'priority':priority,
               'visibility':visibility,
               'state':state,
             } 
        }
        events.append(e)
        return events 
        


