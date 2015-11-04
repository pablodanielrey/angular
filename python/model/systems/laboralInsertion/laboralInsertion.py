# -*- coding: utf-8 -*-
import uuid
import inject

from model.systems.files.files import Files


class LaboralInsertion:
    """
        encapsula todo el acceso a datos de insercion laboral
    """
    files = inject.attr(Files)

    def findAllInscriptionsByUser(self, con, userId):
        """ obtiene los datos de las inscripciones de los alumnos """
        cur = con.cursor()
        cur.execute('select id, user_id, degree, courses, average1, average2, work_type, reside, travel from laboral_insertion.inscriptions where user_id = %s', (userId,))
        inscriptions = []
        for c in cur:
            inscription = {
                'id': c[0],
                'degree': c[2],
                'courses': c[3],
                'average1': c[4],
                'average2': c[5],
                'workType': c[6],
                'reside': c[7],
                'travel': c[8]
            }
            inscriptions.append(inscription)

        return inscriptions

    def deleteInscriptionById(self, con, iid):
        """ elimina la inscripción con el id determinado """
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.inscriptions where id = %s', (iid))

    def persistInscriptionByUser(self, con, userId, d):
        """ genera una inscripcion nueva por usuario """
        iid = str(uuid.uuid4())
        cur = con.cursor()
        cur.execute('insert into laboral_insertion.inscriptions (id, user_id, degree, courses, average1, average2, work_type, reside, travel) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)', (
            iid,
            userId,
            d['degree'],
            d['courses'],
            d['average1'],
            d['average2'],
            d['work_type'],
            False,
            d['travel']
        ))

    def findByUser(self, con, userId):
        """
            obtiene todos los datos referidos a las propiedades de insercion laboral que no sean inscripciones a la bolsa
        """

        cur = con.cursor()
        cur.execute('select id, user_id, name, level from laboral_insertion.languages where user_id = %s', (userId,))
        languages = []
        for c in cur:
            language = {
                'id': c[0],
                'name': c[2],
                'level': c[3]
            }
            languages.append(language)

        cur.execute('select id, accepted_conditions, email, cv from laboral_insertion.users where userid = %s', (userId,))
        r = cur.fetchone()
        ldata = {
            'id': userId,
            'accepted_conditions': r[1],
            'email': r[2],
            'languages': languages,
            'cv': r[3]
        }
        return ldata

    def persist(self, con, d):
        """ actualiza la información de insercion laboral del usuario """

        userId = d['id']

        if not self.files.check(con, d['cv']):
            raise Exception('no existe el cv en la base de datos')

        data = (d['accepted_conditions'], d['email'], d['cv'], d['id'])
        cur = con.cursor()
        cur.execute('select id from laboral_insertion.users where userid = %s', (userId,))
        if (cur.rowcount <= 0):
            cur.execute('insert into laboral_insertion.users (id, accepted_conditions, email, cv) values (%s,%s,%s,%s)', data)
        else:
            cur.execute('update laboral_insertion.users set accepted_conditions = %s, email = %s, cv = %s where id = %s', data)

        cur.execute('delete from laboral_insertion.languages where user_id = %s', d['id'])
        languages = d['languages']
        for l in languages:
            lid = str(uuid.uuid4())
            cur.execute('insert into laboral_insertion.languages (id, user_id, name, level) values (%s,%s,%s,%s)', (lid, userId, l['name'], l['level']))


""""

    def persistLaboralInsertionCV(self,con,data):
        if (self.findLaboralInsertionCV(con,data['id'])) == None:
            params = (data['id'],psycopg2.Binary(data['cv']),data['name'])
            cur = con.cursor()
            cur.execute("insert into laboral_insertion.users_cv (id,cv,name) values (%s,%s,%s)",params)
        else:
            params = (psycopg2.Binary(data['cv']),data['name'],data['id'])
            cur = con.cursor()
            cur.execute('update laboral_insertion.users_cv set cv = %s, name = %s where id = %s',params)
"""
