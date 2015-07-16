# -*- coding: utf-8 -*-
import uuid
import pytz

class Issue:

    '''
     ' Insertar datos
     '''
    def insert(self,con,request,officeId,requestorId,created,priority,visibility,relatedRequestId):
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
            VALUES ('PENDING', %s, %s, %s);
        """,(createdutc, requestorId, id)) 
        
        events = [] 
        e = { 
            'type':'IssueInsertedEvent', 
            'data':{ 
               'entidadId':id, 
             } 
        } 
        events.append(e) 
  
        return events 
        
        
    def getIssuesByUser(self, con, userId):
        cur = con.cursor() 
        cur.execute('''
          SELECT r.*, s.*
          FROM issues.request AS r
          INNER JOIN issues.state AS s ON (r.id = s.request_id)
          INNER JOIN (
            SELECT request_id, max(created) AS created 
            FROM issues.state
            GROUP BY request_id
          ) AS s2 ON (s.request_id = s2.request_id AND s.created = s2.created);
        ''') 
        if cur.rowcount <= 0: 
            return [] 

        return cur
    
    
  
