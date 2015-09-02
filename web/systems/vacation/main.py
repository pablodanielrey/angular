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
future = datetime.datetime(2020, 8, 31)
    

for userId in usersId:
    stock = justification.getJustificationStock(con, userId, '76bc064a-e8bf-4aa3-9f51-a3c4483a729a', begin)
    if stock > 0:
        userData = users.findUser(con,userId)
        print(userId + ' ' + userData["name"] + ' ' + userData["lastname"] + ' ' +  str(stock))

        
print("")
    

justificationRequests = justification.getJustificationRequestsByDate(con, ['APPROVED'], usersId, begin, future)

laoByUsers = {}
for justificationRequest in justificationRequests:
    if justificationRequest["justification_id"] == '76bc064a-e8bf-4aa3-9f51-a3c4483a729a':
      if justificationRequest['user_id'] not in laoByUsers:
        laoByUsers[justificationRequest['user_id']] = 0

      laoByUsers[justificationRequest['user_id']] += 1
      
        


for userId in laoByUsers:
    userData = users.findUser(con,userId)
    print(userData["name"] + ' ' + userData["lastname"] + ' ' + str(laoByUsers[userId]))


print("")

"""
firstDayOfYear = datetime.datetime(2015, 1, 1)
justificationRequestsUser = justification.getJustificationRequestsByDate(con, ['APPROVED'], ['c3f23c7c-4abf-402e-b6f3-ee3fd70f4484'], firstDayOfYear, future)
count = 0
for justificationRequestUser in justificationRequestsUser:
    if justificationRequestUser["justification_id"] == '76bc064a-e8bf-4aa3-9f51-a3c4483a729a':
        count += 1
        print(justificationRequestUser)
        print()
     
print(count)
"""








    
