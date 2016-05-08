# -*- coding: utf-8 -*-
import uuid
import pytz
from model.systems.assistance.date import Date

class Issue:


    '''
     ' Obtener los hijos de un issue en base a su id
     '''
    def getChildsId(self, con, id):
        cur = con.cursor()
        cur.execute('''
          SELECT r.id
          FROM issues.request AS r
          WHERE r.related_request_id = %s
          ORDER BY r.created ASC;
        ''',(id,))
        
        ids = []
        for row in cur: 
            ids.append(issue[0])
           
        return ids
        
        
    '''
     ' Eliminar los estados de un issue en base a su id
     '''
    def deleteStatesFromIssue(self, con, id):
        cur = con.cursor()
        cur.execute('''
          DELETE FROM issues.state
          WHERE request_id = %s
        ''',(id,))       
        
    '''
     ' Eliminar un determinado issue, para poder ser eliminado no debe estar asociado a ningun estado
     ''' 
    def deleteIssue(self, con, id):
        cur = con.cursor()
        cur.execute('''
          DELETE FROM issues.request
          WHERE id = %s
        ''',(id,)) 
    
    
    '''
     ' Insertar issue
     '''
    def insertIssue(self, con, id, request, officeId, requestorId, created, priority, visibility, relatedRequestId):
        cur = con.cursor() 
        cur.execute('set timezone to %s',('UTC',))
        cur.execute("""
            INSERT INTO issues.request (id, request, office_id, requestor_id, created, priority, visibility, related_request_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """,(id, request, officeId, requestorId, created, priority, visibility, relatedRequestId))
        
    '''
     ' Insertar estado de un determinado issue
     '''
    def insertState(self, con, requestId, requestorId, created, state):        
        cur = con.cursor() 
        cur.execute('set timezone to %s',('UTC',))
        cur.execute("""
            INSERT INTO issues.state (state, created, user_id, request_id)
            VALUES (%s, %s, %s, %s);
        """,(state, created, requestorId, requestId))
        
        
  
        
        
        
        
        
        
        
        
        
        
    
   
        
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
        


