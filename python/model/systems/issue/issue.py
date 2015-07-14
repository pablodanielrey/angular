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
  
