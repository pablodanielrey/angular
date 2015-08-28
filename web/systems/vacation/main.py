# -*- coding: utf-8 -*-
import signal
import sys
import inject, psycopg2
import logging
import datetime


# sys.path.append('../python')
sys.path.insert(0, '../../../python')

from model.systems.assistance.assistance import Assistance
from model.systems.offices.offices import Offices
#from model.systems.assistance.justifications.LAOJustification import LAOJustification
from model.systems.assistance.justifications.justifications import Justifications
from model.users.users import Users

assistance = Assistance()
offices = Offices()
justification = Justifications()
users = Users()

con = psycopg2.connect(host="127.0.0.1", dbname="dcsys", user="dcsys", password="dcsys")

officesList = offices.getOffices(con)
officesId = []
for office in officesList:
    officesId.append(office['id'])

usersId = offices.getOfficesUsers(con,officesId)

'''
for userId in usersId:
    officesId.append(office['id'])
    user = users.findUser(con,userId)
    print(user)
'''

begin = datetime.datetime(2015, 8, 31)
now = datetime.datetime(2020, 8, 31)
    
    
justificationRequests = justification.getJustificationRequestsByDate(con, ['APPROVED'], usersId, begin, now)

laoByUsers = {}
for justificationRequest in justificationRequests:
    if justificationRequest["justification_id"] == '76bc064a-e8bf-4aa3-9f51-a3c4483a729a':
      if justificationRequest['user_id'] not in laoByUsers:
        laoByUsers[justificationRequest['user_id']] = 0

      laoByUsers[justificationRequest['user_id']] += 1
      
        


for userId in laoByUsers:
    userData = users.findUser(con,userId)
    print(userData["name"] + ' ' + userData["lastname"] + ' ' + str(laoByUsers[userId]))


#print(justificationRequests)



    
