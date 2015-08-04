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
               'id':id, 
               'request':request,
               'officeId':officeId,
               'requestorId':requestorId,
               'created':createdutc,
               'priority':priority,
               'visibility':visibility,
               'relatedRequestId':relatedRequestId,
               'state':'PENDING',
               'nodes':[],
             } 
        }
        events.append(e)
        return events 
        
        
    def getIssuesByUser(self, con, userId):
        cur = con.cursor() 
        cur.execute('''
          SELECT r.id, r.created, r.request, r.requestor_id, r.office_id, r.related_request_id, r.assigned_id, r.priority, r.visibility, s.state
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
        
        issues = [] 
        for issue in cur: 
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
            
        return issues;
        
    
    
    def deleteIssue(self, con, id):
        self.__deleteIssue(con, id)
        events = []
        e = {
            'type':'IssueDeletedEvent', 
            'data':{
                 'id':id, 
             }
        }
        events.append(e)
        return events
    
    
    def __deleteIssue(self, con, id):
        cur = con.cursor()
        cur.execute('''
          SELECT r.id
          FROM issues.request AS r
          WHERE r.related_request_id = %s
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
         
        
        


