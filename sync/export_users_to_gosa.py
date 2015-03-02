import ldap
import ldap.modlist as modlist
import psycopg2
import sys
import re
import uuid
import base64

user = sys.argv[1]
passw = sys.argv[2]
host = '127.0.0.1'

def createUser(l,dni,name,lastname,username,password,email):
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


    	mod_attrs = [('sn', lastname),
		 ('givenName', name),
		 ('cn', name + " " + lastname),
		 ('uid', [username, dni]),
		 ('homeDirectory', '/home/' + username),
		 ('loginShell', '/bin/bash'),
		 ('uidNumber', uidN),
		 ('gidNumber', gid),
 		 ('mail', email),
 		 ('sambaSID',sambaSID),
		 ('sambaPrimaryGroupSID',sambaGroupSID),
		 ('sambaLMPassword',''),
		 ('sambaNTPassword',''),
		 ('sambaPwdCanChange','1'),
		 ('sambaAcctFlags','[UX          ]'),
		 ('userPassword',password),
		 ('shadowLastChange','14659'),
		 ('gosaMailServer','smtp'),
		 ('gosaMailDeliveryMode','[L]'),
		 ('objectClass', ['top','person','organizationalPerson','inetOrgPerson','posixAccount','shadowAccount','sambaSamAccount','gosaMailAccount'])
    ]


    	dn = "uid=" + username + ",ou=people,dc=econo"
    	l.add_s(dn,mod_attrs)

try :

	l = ldap.initialize("ldap://127.0.0.1:3389")
	l.protocol_version = ldap.VERSION3
	l.simple_bind_s(user,passw)

    	db = psycopg2.connect(host=host, user="dcsys", password= "dcsys", dbname="dcsys")
    	cursor = db.cursor()

    	sql = "select dni,name,lastname,password,u.id from mail.users mu full outer join domain.users du on (mu.id = du.id) inner join profile.users u on (u.id = du.id) inner join credentials.user_password up on (u.id = up.user_id)"
    	cursor.execute(sql)
    	result = cursor.fetchall()

    	for row in result:
	  dni = row[0]
	  name = row[1]
	  lastname = row[2]
	  password = row[3]
	  id = row[4]
	  username = (name + "." + lastname).lower()

	  sqlMail = "select email from users u inner join user_mails um on (u.id = um.user_id) where u.id = '" + id + "'"
	  cursor.execute(sqlMail)
	  emailsResult = cursor.fetchall()
	  mailEcono = ''
	  for mail in emailsResult:
	    if 'econo.unlp.edu.ar' in mail[0]:
	      mailEcono = mail[0]

	  print "Email econo:%s"%mailEcono
	  createUser(l,dni,name,lastname,username,password,mailEcono)

	l.unbind_s()
    	cursor.close()
    	db.close()

except (ldap.LDAPError,psycopg2.Error) as e :
        print e
