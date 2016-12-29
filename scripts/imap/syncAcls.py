import logging
import sys
sys.path.append('../../python')
import os

import inject
inject.configure()

from model.registry import Registry
from model.connection.connection import Connection


class Acl:

    def __init__(self, group, users):
        self.directory = "/home/grupos/{}".format(group)
        self.file = "dovecot-acl"
        self.users = users

    def toFile(self, f):
        for u in self.users:
            f.write("user={} lrwstipeka\n".format(u))



# Obtengo las oficinas con email:
def findOfficesWithEmail(con):
    cur = con.cursor()
    try:
        cur.execute("select id, email from offices.offices where removed is null and email != '' and not name ilike '%alias%' order by email")
        return [{'email':o['email'], 'id':o['id']} for o in cur]
    finally:
        cur.close()

# obtengo los dni de los usuarios que pertenecen al grupo
def getUsers(con, oId):
    cur = con.cursor()
    try:
        cur.execute('select dni from designations.designations d inner join profile.users u on (d.user_id = u.id) where send is null and office_id = %s',(oId,))
        return [r['dni'] for r in cur]
    finally:
        cur.close()

# crea los arhivos acl
def createFile(acl):
    if not os.path.exists(acl.directory):
        os.makedirs(acl.directory)

    f = open(acl.directory + '/' + acl.file, 'w')
    try:
        acl.toFile(f)
    finally:
        f.close()

reg = inject.instance(Registry)
conn = Connection(reg.getRegistry('dcsys'))
con = conn.get()

try:
    Connection.readOnly(con)
    offices = findOfficesWithEmail(con)
    ant = None
    users = set()
    email = None
    acls = []
    for off in offices:
        id = off['id']
        email = off['email']
        if ant is None or email != ant['email']:
            if ant is not None:
                acls.append(Acl(ant['email'].split('@')[0], users))
                print("grupo: {} usuarios:{}".format(ant['email'].split('@')[0], users))
            users = set()

        for u in getUsers(con, id):
            users.add(u)

        ant = off

    if email is not None:
        acls.append(Acl(email.split('@')[0], users))

    for acl in acls:
        createFile(acl)

finally:
    conn.put(con)
