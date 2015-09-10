# -*- coding: utf-8 -*-
import uuid
import psycopg2
import inject
import hashlib
import re

from model.config import Config
from model.objectView import ObjectView
from model.mail.mail import Mail

class Users:
    def __init__(self, config=None):
        self.serverConfig = inject.instance(Config)
        self.mail = inject.instance(Mail)

    '''
     ' Enviar email de confirmacion: Define un hash y envia un email de confirmacion al usuario con el hash
     ' @param con Conexion con la base de datos
     ' @param emailId Identificacion del email
     '''
    def sendEmailConfirmation(self, con, emailId):
        email = self.findMail(con, emailId)
        if(email is None):
            raise Exception("Email inexistente")

        hash = hashlib.sha1((email['id'] + email['user_id']).encode('utf-8')).hexdigest()
        email['hash'] = hash

        self.updateMail(con,email)

        From = self.serverConfig.configs['mail_confirm_mail_from']
        subject = self.serverConfig.configs['mail_confirm_mail_subject']
        To = email['email']
        template = self.serverConfig.configs['mail_confirm_mail_template']

        url = self.serverConfig.configs['mail_confirm_mail_url']
        url = re.sub('###HASH###', hash, url)

        replace = [
            ('###URL###',url)
        ]

        self.mail.sendMail(From,[To],subject,replace,html=template)

        return True


    def confirmEmail(self,con,hash):
        email = self.findMailByHash(con, hash)
        if(email is None):
            raise Exception("Email inexistente")

        email['confirmed'] = True
        email['hash'] = None

        self.updateMail(con,email)

        From = self.serverConfig.configs['mail_confirm_mail_from']
        subject = self.serverConfig.configs['mail_confirm_mail_subject']
        To = email['email']
        template = self.serverConfig.configs['mail_confirm_mail_template']

        url = self.serverConfig.configs['mail_mail_confirmed_template']
        url = re.sub('###HASH###', hash, url)

        replace = [
            ('###URL###',url)
        ]

        self.mail.sendMail(From,[To],subject,replace,html=template)


    def createMail(self,con,data):
        if 'confirmed' not in data:
            data['confirmed'] = False

        mail = ObjectView(data)
        mid = str(uuid.uuid4())
        rreq = (mid,mail.user_id,mail.email,mail.confirmed,'')
        cur = con.cursor()
        cur.execute('insert into profile.mails (id,user_id,email,confirmed,hash) values (%s,%s,%s,%s,%s)', rreq)
        return mid

    def findMailByHash(self,con,hash):
        cur = con.cursor()
        cur.execute('select id,user_id,email,confirmed,hash from profile.mails where hash = %s', (hash,))
        data = cur.fetchone()
        if data != None:
            return self.convertMailToDict(data)
        else:
            return None

    def findMail(self,con,id):
        cur = con.cursor()
        cur.execute('select id,user_id,email,confirmed,hash from profile.mails where id = %s', (id,))
        data = cur.fetchone()
        if data != None:
            return self.convertMailToDict(data)
        else:
            return None

    def listMails(self, con, user_id):
        cur = con.cursor()
        cur.execute('select id, user_id, email, confirmed, hash from profile.mails where user_id = %s',(user_id,))
        data = cur.fetchall()
        rdata = []
        for d in data:
            rdata.append(self.convertMailToDict(d))
        return rdata

    def deleteMail(self,con,id):
        cur = con.cursor()
        cur.execute('delete from profile.mails where id = %s', (id,))


    def updateMail(self,con,data):
        if 'hash' not in data:
            data['hash'] = ''
        mail = ObjectView(data)
        rreq = (mail.email, mail.confirmed, mail.hash, mail.id)
        cur = con.cursor()
        cur.execute('update profile.mails set email = %s, confirmed = %s, hash = %s where id = %s', rreq)


    ''' transformo a diccionario las respuestas de psycopg2'''
    def convertMailToDict(self,d):
        rdata = {
                'id':d[0],
                'user_id':d[1],
                'email':d[2],
                'confirmed':d[3],
                'hash':d[4]
            }
        return rdata


    """-------------------------------"""

    def createUser(self,con,data):
        uid = str(uuid.uuid4())
        if 'id' in data and data['id'] is not None:
            uid = data['id']

        rreq = (uid,
                data['dni'],
                data['name'],
                data['lastname'],
                data['city'] if 'city' in data else '',
                data['country'] if 'country' in data else '',
                data['address'] if 'address' in data else '',
                data['genre'] if 'genre' in data else '',
                data['birthdate'] if 'birthdate' in data else None,
                data['residence_city'] if 'residence_city' in data else '',
                data['version'] if 'version' in data else 0)
        cur = con.cursor()
        cur.execute('insert into profile.users (id,dni,name,lastname,city,country,address,genre,birthdate,residence_city,version) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', rreq)
        return uid

    '''
     ' Persistir usuario: En funcion del id del usuario crea o actualiza el usuario
     ' @param user Datos del usuario
     ' @return Id del usuario persistido
     '''
    def updateUser(self,con,user):
        cur = con.cursor()

        ''' si no exite lo creo '''
        userId = None
        if 'id' not in user:
            userId = self.createUser(con,user)
        else:
            userId = user['id']
            cur.execute('select id from profile.users where id = %s',(user['id'],))
            if cur.rowcount <= 0:
                userId = self.createUser(con,user)
            else:
                rreq = (user['dni'],user['name'],user['lastname'],user['city'],user['country'],user['address'],user['genre'],user['birthdate'],user['residence_city'], user['version'], user['id'])
                cur.execute('update profile.users set dni = %s, name = %s, lastname = %s, city = %s, country = %s, address = %s, genre = %s, birthdate = %s, residence_city = %s, version = %s where id = %s', rreq)
                if cur.rowcount <= 0:
                    raise Exception()


        #actualizar telefonos del usuario
        cur.execute('delete from profile.telephones where user_id = %s', (userId,))

        if 'telephones' in user:
            for i, v in enumerate(user['telephones']):
                 telephone_id = str(uuid.uuid4())
                 rreq = (telephone_id, user['id'], v["number"], v["type"])
                 cur.execute('INSERT INTO profile.telephones (id, user_id, number, type) VALUES (%s, %s, %s, %s);', rreq)

        return userId


    def findUserByDni(self,con,dni):
        cur = con.cursor()
        cur.execute('select id,dni,name,lastname,city,country,address,genre,birthdate,residence_city,version from profile.users where dni = %s', (dni,))
        data = cur.fetchone()

        if data != None:
            return self.convertUserToDict(data)
        else:
            return None

    def findUser(self,con,id):
        cur = con.cursor()
        cur.execute('select id,dni,name,lastname,city,country,address,genre,birthdate,residence_city,version from profile.users where id = %s', (id,))
        if cur.rowcount <= 0:
            return None

        dataUser = cur.fetchone()
        rdataUser = self.convertUserToDict(dataUser);
        cur.execute('SELECT id, number, type FROM profile.telephones WHERE user_id = %s',(dataUser[0],))
        dataTelephones = cur.fetchall()
        rdataTelephones = []
        for dataTelephone in dataTelephones:
            rdataTelephones.append(self.convertTelephoneToDict(dataTelephone))
        rdataUser["telephones"] = rdataTelephones
        return rdataUser


    def listUsers(self, con):
        cur = con.cursor()
        cur.execute('select id,dni,name,lastname,city,country,address,genre,birthdate,residence_city,version from profile.users')
        data = cur.fetchall()
        rdata = []
        for d in data:
            rdata.append(self.convertUserToDict(d))
        return rdata

    '''
     ' Listar ids de usuarios
     ' @param con Conexion con la base de datos
     ' @return Lista de ids de usuarios
     '''
    def listUsersIds(self, con):
        cur = con.cursor()
        cur.execute('select id from profile.users')
        data = cur.fetchall()
        rdata = []
        for d in data:
            rdata.append(d[0])
        return rdata


    ''' retorna true en el caso de que el usuario pasado como parámetro tenga una version mayor al de la base '''
    def needSync(self,con,user):
        id = user['id']

        cur = con.cursor()
        cur.execute('select version from profile.users where id = %s',(id,))
        if cur.rowcount <= 0:
            return True

        version = cur.fetchone()[0]
        return user['version'] > version



    ''' transformo a diccionario las respuestas de psycopg2'''
    def convertUserToDict(self,d):
        rdata = {
                'id':d[0],
                'dni':d[1],
                'name':d[2],
                'lastname':d[3],
                'city':d[4],
                'country':d[5],
                'address':d[6],
                'genre':d[7],
                'birthdate':d[8],
                'residence_city':d[9],
                'version':d[10]
            }
        return rdata

    ''' transformo a telefonos las respuestas de psycopg2'''
    def convertTelephoneToDict(self,d):
        rdata = {
                'id':d[0],
                'number':d[1],
                'type':d[2]
            }
        return rdata
