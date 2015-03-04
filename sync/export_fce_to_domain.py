import ldap
import ldap.modlist as modlist
import psycopg2
import sys
import re
import uuid
import base64
import hashlib

user = sys.argv[1]
passw = sys.argv[2]
host = '127.0.0.1'

def modifyUser(l,dni,name,lastname,username,password,result):

	print "Modificando usuario"

	(dn,attrs) = result[0]

	if 'gidNumber' in attrs:
		gidNumber = attrs['gidNumber'][0]
	else:
		print "Error, no posee gidNumber el usuario " + username
		exit(1)

	if 'uidNumber' in attrs:
		uidNumber = attrs['uidNumber'][0]
	else:
		print "Error, no posee uidNumber el usuario " + username
		exit(1)

	sambaSID = 'S-1-5-21-69815507-558479685-3467165442-' + uidNumber
    	sambaGroupSID = 'S-1-5-21-69815507-558479685-3467165442-' + gidNumber


	exist = False
	for object in attrs['objectClass']:
		if (not exist) and (object == 'sambaSamAccount'):
			exist = True
	if not exist:
		attrs['objectClass'].append('sambaSamAccount')

	exist = False
	for uid in attrs['uid']:
		if uid == dni:
			exist = True
	if not exist:
		attrs['uid'].append(dni)


    	nt_password = hashlib.new( 'md4', password.encode('utf-16le')).digest().encode('hex').upper( )

	mod_attrs = [(ldap.MOD_REPLACE,'givenName',name),
		(ldap.MOD_REPLACE,'cn',name + " " + lastname),
		(ldap.MOD_REPLACE,'sn', lastname),
		(ldap.MOD_REPLACE,'userPassword',password),
		(ldap.MOD_REPLACE,'homeDirectory', '/home/' + username),
		(ldap.MOD_REPLACE,'loginShell', '/bin/bash'),

		(ldap.MOD_REPLACE,'sambaSID',sambaSID),
		(ldap.MOD_REPLACE,'sambaPrimaryGroupSID',sambaGroupSID),
		(ldap.MOD_REPLACE,'sambaPwdCanChange','1'),
		(ldap.MOD_REPLACE,'sambaPwdLastSet','1328708656'),
		(ldap.MOD_REPLACE,'sambaBadPasswordCount','0'),
		(ldap.MOD_REPLACE,'sambaBadPasswordTime','0'),
		(ldap.MOD_REPLACE,'sambaLMPassword',''),
		(ldap.MOD_REPLACE,'sambaNTPassword',nt_password),
		(ldap.MOD_REPLACE,'sambaDomainName','ECONO'),
		(ldap.MOD_REPLACE,'sambaAcctFlags','[UX          ]'),
		(ldap.MOD_REPLACE,'objectClass',attrs['objectClass']),
		(ldap.MOD_REPLACE,'uid', attrs['uid'])]

        l.modify_s(dn,mod_attrs)


def getUser(l,dni,username):
	result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(uid=" + dni + ")",["dn","uidNumber","gidNumber","objectClass","uid"])
	if (result != None) and (len(result) > 0):
        	return result

	result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(uid=" + username +")",["dn","uidNumber","gidNumber","objectClass","uid"])
    	if (result != None) and (len(result) > 0):
        	return result

	return None

def createUser(l,dni,name,lastname,username,password):

	print "Creando Usuario nuevo"

	result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(uid=" + dni + ")",["dn"])
	if (result != None) and (len(result) > 0):
		mod_attrs = [(ldap.MOD_REPLACE,'userPassword',password)]
        	dn = "uid=" + dni + ",ou=people,dc=econo"
        	l.modify_s(dn,mod_attrs)
        	exit(0)

	result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(uid=" + username +")",["dn"])
    	if (result != None) and (len(result) > 0):
        	mod_attrs = [(ldap.MOD_REPLACE,'userPassword',password)]
        	dn = "uid=" + username + ",ou=people,dc=econo"
        	l.modify_s(dn,mod_attrs)
        	exit(0)



	result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(|(gidNumber=*)(uidNumber=*))",["gidNumber",'uidNumber'])
    	lastNumber = 0

    	if result != None:
      		for dn,n in result:
          		if 'gidNumber' in n:
            			num = int(n['gidNumber'][0])
            			if lastNumber < num:
              				lastNumber = num
          		if 'uidNumber' in n:
            			num = int(n['uidNumber'][0])
            			if lastNumber < num:
              				lastNumber = num


	uidN = str(lastNumber + 1)
    	gid = str(lastNumber + 2)
    	sambaSID = 'S-1-5-21-69815507-558479685-3467165442-' + uidN
    	sambaGroupSID = 'S-1-5-21-69815507-558479685-3467165442-' + gid



    	nt_password = hashlib.new( 'md4', password.encode('utf-16le')).digest().encode('hex').upper( )

    	mod_attrs = [('sn', lastname),
		 ('givenName', name),
		 ('cn', name + " " + lastname),
		 ('uid', [username, dni]),
		 ('userPassword',password),
		 ('homeDirectory', '/home/' + username),
		 ('loginShell', '/bin/bash'),

		 ('uidNumber', uidN),
		 ('gidNumber', gid),

 		 ('sambaSID',sambaSID),
		 ('sambaPrimaryGroupSID',sambaGroupSID),
		 ('sambaLMPassword',''),
		 ('sambaNTPassword',nt_password),
		 ('sambaPwdLastSet','1328708656'),
		 ('sambaDomainName','ECONO'),
		 ('sambaPwdCanChange','1'),
		 ('sambaBadPasswordCount','0'),
		 ('sambaBadPasswordTime','0'),
		 ('sambaAcctFlags','[UX          ]'),
		 ('shadowLastChange','14659'),
		 ('objectClass', ['top','person','organizationalPerson','inetOrgPerson','posixAccount','shadowAccount','sambaSamAccount'])
    ]


    	dn = "uid=" + username + ",ou=people,dc=econo"
    	l.add_s(dn,mod_attrs)

try :

	l = ldap.initialize("ldap://127.0.0.1:3389")
	l.protocol_version = ldap.VERSION3
	l.simple_bind_s(user,passw)

    	db = psycopg2.connect(host=host, user="dcsys", password= "dcsys", dbname="dcsys")
    	cursor = db.cursor()

    	sql = "select dni,name,lastname,password,u.id from domain.users du inner join profile.users u on (u.id = du.id) inner join credentials.user_password up on (u.id = up.user_id)"
    	cursor.execute(sql)
    	result = cursor.fetchall()

    	for row in result:
		dni = row[0]
		name = row[1]
		lastname = row[2]
		password = row[3]
		id = row[4]
		username = (name + "." + lastname).lower()

		result = getUser(l,dni,username)
		if (result == None) :
			createUser(l,dni,name,lastname,username,password)
		else :
			modifyUser(l,dni,name,lastname,username,password,result)

	l.unbind_s()
    	cursor.close()
    	db.close()

except (ldap.LDAPError,psycopg2.Error) as e :
        print e
