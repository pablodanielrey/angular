# -*- coding: utf-8 -*-
import uuid
import inject
import logging
import base64

from model.files.files import FileDAO
import model.users.users
from model.users.users import StudentDAO
from model.mail.mail import Mail
from email.mime.text import MIMEText

from model.laboralinsertion.mails import SentDAO, Sent
from model.laboralinsertion.inscription import InscriptionDAO
from model.laboralinsertion.company import CompanyDAO
from model.laboralinsertion.languages import LanguageDAO
from model.laboralinsertion.user import UserDAO, User

import csv


class LaboralInsertion:

    """
        encapsula todo el acceso a datos de insercion laboral
    """
    def __init__(self):
        self.mail = inject.instance(Mail)


    """
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
    """


    def findAllInscriptions(self, con):
        """ obtiene los datos de las inscripciones de los alumnos """
        ids = InscriptionDAO.findAll(con)
        inscriptions = []
        for id in ids:
            inscription = InscriptionDAO.findById(con, id)
            inscriptions.append(inscription)

        return inscriptions

    def findAllInscriptionsByUser(self, con, userId):
        """ obtiene los datos de las inscripciones de los alumnos """
        ids = InscriptionDAO.findByUser(con, userId)
        inscriptions = []
        for id in ids:
            inscription = InscriptionDAO.findById(con, id)
            inscriptions.append(inscription)

        return inscriptions

    def deleteInscriptionById(self, con, iid):
        """ elimina la inscripción con el id determinado """
        InscriptionDAO.delete(con, iid)

    def persistInscription(self, con, inscription):
        """ genera una inscripcion nueva por usuario """
        InscriptionDAO.persist(con, inscription)

    def findByUser(self, con, userId):
        """
            obtiene todos los datos referidos a las propiedades de insercion laboral que no sean inscripciones a la bolsa
        """

        languagesIds = LanguageDAO.findByUser(con, userId)
        languages = []
        for id in languagesIds:
            languages.append(LanguageDAO.findById(con, id))

        users = model.laboralinsertion.user.UserDAO.findById(con, userId)
        if len(users) == 0:
            return None
        user = users[0]
        user.languages = languages
        return user

    def persist(self, con, user, languages):
        """ actualiza la información de insercion laboral del usuario """
        UserDAO.persist(con, user)
        for l in languages:
            LanguageDAO.persist(con, l)


    def sendMailToCompany(self, con, inscriptions, company):
        datar = []
        emails = company.emails

        if emails is None:
            return []

        content = '''
            <html>
            <body>
                <div>
                    A través del presente correo enviamos el listado de candidatos solicitados y
                    sus respectivos CVs.
                    Cualquier inquietud, estamos a disposición.
                    Atte.
                </div>

                <div>
                    Cra. Ma. Paula Beyries

                    Lic. Lucas Tomás Troiano
                    Prosecretario de Inserción Laboral
                </div>

                <div>
                    Prosecretaría de Inserción Laboral
                    Facultad de Ciencias Económicas
                    Oficina 511 - 5to piso
                    Tel: (221) 423-6769/6772 int 117
                    e-mail: insercionlaboral@econo.unlp.edu.ar
                </div>
            </body>
            </html>
        '''

        fss = []
        import csv
        import os
        inscriptionsfile = '/tmp/{}.csv'.format(str(uuid.uuid4()))
        with open(inscriptionsfile, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow(['Dni', 'Nombre', 'Apellido', 'Email'])

            for i in inscriptions:
                data = self.findByUser(con, i['userId'])
                mail = model.users.users.MailDAO.findById(con, data.email)
                if mail is None or len(mail) <= 0:
                    continue

                mail = mail[0]

                if mail.email in datar:
                    continue


                if (data.cv is None):
                    continue
                cvf = FileDAO.findById(con, data.cv)
                cvf.content = FileDAO.getContent(con, cvf.id)
                if cvf.content is None:
                    continue

                ''' decodifico los datos del archivo '''
                filedata = None
                if cvf.codec[0] == 'binary':
                    filedata = bytes(cvf.content)
                elif cvf.codec[0] == 'base64':
                    filedata = base64.b64decode(bytes(cvf.content))

                user = model.users.users.UserDAO.findById(con, i['userId'])
                if user is None:
                    continue

                filename, file_extension = os.path.splitext(cvf.name)
                #fss.append(self.mail.attachFile('{}_{}_{}_{}'.format(user['name'], user['lastname'], user['dni'], file_extension), filedata))
                fss.append(self.mail.attachFile('{}{}'.format(user.dni, file_extension), filedata))

                datar.append(mail.email)
                logging.info('escribiendo fila')
                writer.writerow([user.dni, user.name, user.lastname, mail.email])

        with open(inscriptionsfile, 'r', newline='', encoding='utf-8') as csvfile:
            fss.append(self.mail.attachFile('inscriptos.csv', csvfile.read(), 'application', 'csv'))

        for email in emails:
            logging.info('enviando a {}'.format(email))
            m = self.mail.createMail('insercionlaboral@econo.unlp.edu.ar', email, 'Inscripción en la bolsa de trabajo FCE')
            maux = self.mail.getHtmlPart(content)
            m.attach(maux)
            for f in fss:
                m.attach(f)
            self.mail._sendMail('insercionlaboral@econo.unlp.edu.ar', email, m)

        ''' genero los datos del envío en la base '''
        sent = Sent()
        sent.emails = emails
        sent.inscriptions = [i['id'] for i in inscriptions]
        sent.persist(con)
        con.commit()

        return datar


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
