import ldap
import ldap.modlist as modlist
import psycopg2
import sys
import re
import uuid
import base64

#user = sys.argv[1]
#passw = sys.argv[2]
user = ''
passw = ''
host = ''

def modifyUser(l,dni,name,lastname,username,password,email,result):
	
	print "Modificar usuario"
	
	(dn,attrs) = result[0] 
	
	exist = False
	for object in attrs['objectClass']:
		if (not exist) and (object == 'gosaMailAccount'):
			exist = True
	if not exist:
		attrs['objectClass'].append('gosaMailAccount')
	
	exist = False
	for uid in attrs['uid']:
		if uid == dni:
			exist = True
	if not exist:
		attrs['uid'].append(dni)
	
	mod_attrs = [(ldap.MOD_REPLACE,'userPassword',password),
			(ldap.MOD_REPLACE,'mail',email),
			(ldap.MOD_REPLACE,'sn', lastname),
			(ldap.MOD_REPLACE,'givenName', name),
			(ldap.MOD_REPLACE,'homeDirectory', '/home/' + username),
			(ldap.MOD_REPLACE,'cn', name + " " + lastname),			
			(ldap.MOD_REPLACE,'mail', email),
			(ldap.MOD_REPLACE,'objectClass',attrs['objectClass']),
			(ldap.MOD_REPLACE,'gosaMailServer','smtp'),
			(ldap.MOD_REPLACE,'uid', attrs['uid']),
			(ldap.MOD_REPLACE,'gosaMailDeliveryMode','[L]')]

        l.modify_s(dn,mod_attrs)         
          

def getUser(l,dni,username):
	result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(uid=" + dni + ")",["dn","objectClass","uid"])
	if (result != None) and (len(result) > 0):
        	return result

	result = l.search_s("dc=econo",ldap.SCOPE_SUBTREE,"(uid=" + username +")",["dn","objectClass","uid"])
    	if (result != None) and (len(result) > 0):
        	return result
	      
	return None

def createUser(l,dni,name,lastname,username,password,email):
	
	print "Creando usuario"

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

    	mod_attrs = [('sn', lastname),
		 ('givenName', name),
		 ('cn', name + " " + lastname),
		 ('uid', [username, dni]),
		 ('homeDirectory', '/home/' + username),
		 ('loginShell', '/bin/bash'),
 		 ('mail', email),
		 ('uidNumber', uidN),
		 ('gidNumber', gid),
		 ('userPassword',password),
		 ('gosaMailServer','smtp'),
		 ('shadowLastChange','14659'),
		 ('gosaMailDeliveryMode','[L]'),
		 ('objectClass', ['top','person','organizationalPerson','inetOrgPerson','posixAccount','shadowAccount','gosaMailAccount'])
	]

    	dn = "uid=" + username + ",ou=people,dc=econo"
    	l.add_s(dn,mod_attrs)



try :

	l = ldap.initialize("ldap://163.10.17.121:389")
	l.protocol_version = ldap.VERSION3
	l.simple_bind_s(user,passw)

    	db = psycopg2.connect(host=host, user="dcsys", password= "dcsys", dbname="dcsys")
    	cursor = db.cursor()

    	sql = "select dni,name,lastname,username,password,u.id from mail.users mu inner join profile.users u on (u.id = mu.id) inner join credentials.user_password up on (u.id = up.user_id)"
    	cursor.execute(sql)
    	result = cursor.fetchall()

    	for row in result:
		dni = row[0]
		
		print "Sincronizando usuario con dni:" + dni
		
		name = row[1]
		lastname = row[2]
		username = row[3]
		password = row[4]
		id = row[5]

		sqlMail = "select email from profile.users u inner join profile.mails um on (u.id = um.user_id) where u.id = '" + id + "'"
		cursor.execute(sqlMail)
		emailsResult = cursor.fetchall()
		mailEcono = ''
		for mail in emailsResult:
			if 'econo.unlp.edu.ar' in mail[0]:
				mailEcono = mail[0]

		result = getUser(l,dni,username) 
		if (result != None):
			modifyUser(l,dni,name,lastname,username,password,mailEcono,result)
		else:
			createUser(l,dni,name,lastname,username,password,mailEcono)
	  
	l.unbind_s()
    	cursor.close()
    	db.close()

except (ldap.LDAPError,psycopg2.Error) as e :
        print e
