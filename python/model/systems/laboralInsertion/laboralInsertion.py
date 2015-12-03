# -*- coding: utf-8 -*-
import uuid
import inject
import logging
import base64

from model.systems.files.files import Files
from model.users.users import Users
from model.systems.students.students import Students

import csv

class LaboralInsertion:

    """
        encapsula todo el acceso a datos de insercion laboral
    """
    files = inject.attr(Files)
    users = inject.attr(Users)
    students = inject.attr(Students)

    def download(self, con, url, root):
        with open('{}inscripciones.csv'.format(root), 'w', encoding='utf-8') as r:
            w = csv.writer(r)
            inscriptions = self.findAllInscriptions(con)
            index = 0

            w.writerow(['Fecha de Inscripción',
                'Apellido',
                'Nombre',
                'Sexo',
                'Fecha Nacimiento',
                'Edad',
                'Dni',
                'e-Mail',
                'País',
                'Ciudad de Origen',
                'Ciudad de residencia',
                'Legajo',
                'Viajar',
                'Ingles', 'Portugués', 'Otro',
                'Carrera', 'Cantidad de materias', 'Promedio con aplazos', 'Promedio', 'Pasantía', 'Tiempo Completo', 'Jóvenes Profesionales','Experiencia Laboral'])

            for i in inscriptions:

                userId = i['user_id']
                user = self.users.findById(con, userId)
                ld = self.findByUser(con, userId)
                student = self.students.findById(con, userId)

                logging.debug(student)

                email = self.users.findMail(con, ld['email'])
                cvId = ld['cv']
                cv = self.files.findById(con, ld['cv'])

                english = 'Inglés' in (l['name'] for l in ld['languages'])
                portugues = 'Portugués' in (l['name'] for l in ld['languages'])

                import os
                filename, extension = os.path.splitext(cv['name'])
                cv_name = '{}{}'.format(user['dni'], extension)

                w.writerow([
                 i['creation'],
                 user['lastname'],
                 user['name'],
                 user['genre'],
                 user['birthdate'],
                 '',
                 user['dni'],
                 email['email'] if email else '',
                 user['country'],
                 user['city'],
                 user['residence_city'],
                 student['studentNumber'],
                 i['travel'],

                 'Sí' if english else 'No',
                 'Sí' if portugues else 'No',
                 'No',

                 i['degree'],
                 i['approved'],
                 i['average1'],
                 i['average2'],
                 'Sí' if 'Pasantía' in i['workType'] else 'No',
                 'Sí' if 'Full-Time' in i['workType'] else 'No',
                 'Sí' if 'Programa estudiantes avanzados y jovenes profesionales' in i['workType'] else 'No',

                 i['workExperience'],

                 '{}/cv/{}'.format(url, cv_name)

                 ])

                logging.debug('escribiendo cv : {}'.format(cv))
                #with open('{}{}'.format(root, cv_name), 'wb') as c:

                with open('{}{}'.format(root, cv_name), 'wb') as c:
                    try:
                        if cv['codec'] == 'binary':
                            c.write(bytes(cv['content']))
                        elif cv['codec'] == 'base64':
                            c.write(base64.b64decode(bytes(cv['content'])))
                    except Exception as e:
                        logging.warn('error en cv {}'.format(cv))

                index = index + 1



    def findAllInscriptions(self, con):
        """ obtiene los datos de las inscripciones de los alumnos """
        cur = con.cursor()
        cur.execute('select id, user_id, degree, courses, average1, average2, work_type, reside, travel, work_experience, creation from laboral_insertion.inscriptions')
        inscriptions = []
        for c in cur:
            inscription = {
                'id': c[0],
                'user_id': c[1],
                'degree': c[2],
                'approved': c[3],
                'average1': c[4],
                'average2': c[5],
                'workType': c[6],
                'reside': c[7],
                'travel': c[8],
                'workExperience': c[9],
                'creation': c[10]
            }
            inscriptions.append(inscription)

        return inscriptions

    def findAllInscriptionsByUser(self, con, userId):
        """ obtiene los datos de las inscripciones de los alumnos """
        cur = con.cursor()
        cur.execute('select id, user_id, degree, courses, average1, average2, work_type, reside, travel, work_experience, creation from laboral_insertion.inscriptions where user_id = %s', (userId,))
        inscriptions = []
        for c in cur:
            inscription = {
                'id': c[0],
                'degree': c[2],
                'approved': c[3],
                'average1': c[4],
                'average2': c[5],
                'workType': c[6],
                'reside': c[7],
                'travel': c[8],
                'workExperience': c[9],
                'creation': c[10]
            }
            inscriptions.append(inscription)

        return inscriptions

    def deleteInscriptionById(self, con, iid):
        """ elimina la inscripción con el id determinado """
        cur = con.cursor()
        cur.execute('delete from laboral_insertion.inscriptions where id = %s', (iid,))

    def persistInscriptionByUser(self, con, userId, d):
        """ genera una inscripcion nueva por usuario """
        iid = str(uuid.uuid4())
        cur = con.cursor()
        cur.execute('insert into laboral_insertion.inscriptions (id, user_id, degree, courses, average1, average2, work_type, reside, travel, work_experience) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (
            iid,
            userId,
            d['degree'],
            d['approved'],
            d['average1'],
            d['average2'],
            d['workType'],
            False,
            d['travel'],
            d['workExperience']
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

        cur.execute('select id, accepted_conditions, email, cv from laboral_insertion.users where id = %s', (userId,))
        if cur.rowcount <= 0:
            return None

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

        if 'cv' in d and d['cv'] is not None and d['cv'] is not '' and not self.files.check(con, d['cv']):
            raise Exception('no existe el cv en la base de datos')

        cur = con.cursor()
        cur.execute('select id from laboral_insertion.users where id = %s', (userId,))
        if (cur.rowcount <= 0):
            ldata = []
            sql = 'insert into laboral_insertion.users ('
            values = '('
            if 'accepted_conditions' in d:
                sql = sql + 'accepted_conditions'
                ldata.append(d['accepted_conditions'])
                values = values + "%s"

            if 'email' in d:
                sql = sql + ',email'
                ldata.append(d['email'])
                values = values + ",%s"

            if 'cv' in d:
                sql = sql + ',cv'
                ldata.append(d['cv'])
                values = values + ",%s"

            values = values + ",%s)"
            ldata.append(d['id'])
            sql = sql + ',id) values ' + values
            data = tuple(ldata)

            cur.execute(sql, data)
        else:

            ldata = []
            sql = 'update laboral_insertion.users set accepted_conditions = %s '
            ldata.append(d['accepted_conditions'])

            if 'email' in d:
                sql = sql + ',email = %s'
                ldata.append(d['email'])

            if 'cv' in d:
                sql = sql + ',cv = %s'
                ldata.append(d['cv'])

            sql = sql + ' where id = %s'
            ldata.append(d['id'])

            data = tuple(ldata)
            cur.execute(sql, data)

        cur.execute('delete from laboral_insertion.languages where user_id = %s', (d['id'],))
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
