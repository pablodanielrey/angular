# -*- coding: utf-8 -*-
import json, base64, traceback, logging
import inject, psycopg2
import pytz, datetime
import dateutil.parser

import uuid
import pytz
from model.systems.assistance.date import Date


from model.systems.issue.issue import Issue


class IssueModel:


    issue = inject.attr(Issue)
    
    
    '''
     ' Metodo recursivo de eliminacion de peticiones y sus hijos
     '''
    def __deleteIssue(self, con, id):
        cur = con.cursor()
        
        ids = self.issue.getChildsId(con, id)        
    
        for idChild in ids:
            self.__deleteIssue(con, idChild)

        self.issue.deleteStatesFromIssue(con, id)     
        
        self.issue.deleteIssue(con, id)       
        

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
     ' Insertar datos, se insertan los datos del request y el estado
     '''
    def insert(self,con,request,officeId,requestorId,created,priority,visibility,relatedRequestId, state):
        createdutc = created.astimezone(pytz.utc)
            
        id = str(uuid.uuid4()) 
        self.issue.insertIssue(con, id, request, officeId, requestorId, createdutc, priority, visibility, relatedRequestId)
        self.issue.insertState(con, id, requestorId, createdutc, state)
       
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


    def getIssuesByUser(self, 
       
                
                
          
