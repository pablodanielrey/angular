# -*- coding: utf-8 -*-

import uuid
import inject
import logging

from model.registry import Registry
from model.mail.mail import Mail

import model.laboralinsertion.user
import model.users.users

class EmailToSend:

    reg = inject.attr(Registry).get('LaboralInsertion')
    mailModel = inject.attr(Mail)

    def __init__(self, inscriptionIds, emailsToSend):
        assert isinstance(inscriptionIds, list)
        assert isinstance(emailsToSend, list)

        self.inscriptionIds = inscriptionIds
        self.inscriptions = None
        self.users = None
        self.mails = emailsToSend

    def _clasifyByUser(self, con, users):
        users2 = {}
        for u in users:

            ld = model.laboralinsertion.user.UserDAO.findById(con, u.id)[0]
            email = model.users.users.MailDAO.findById(con, ld.email)[0]

            users2[u.id] = {
                'user': u,
                'data': ld,
                'email': email
            }

        return users2

    def _loadInscriptions(self, con):
        self.inscriptions = InscriptionDAO.findById(con, self.inscriptionIds)

    def _loadUsers(self, con):
        userIds = [ i.userId for i in self.inscriptions ]
        self.users = self._clasifyByUser(con, model.users.users.UserDAO.findById(con, userIds))

    def _generateOds(self):
        import pyoo
        host = reg.get('ooHost')
        port = int(reg.get('ooPort'))
        sheetTemplate = reg.get('sheetTemplate')

        calc = pyoo.Desktop(host, port)
        doc = calc.open_spreadsheet(sheetTemplate)
        try:
            sheet = doc.sheets[0]
            index = 1
            for i in self.inscriptions:
                sheet[index,0] = self.users[i.userId]['user'].lastname
                sheet[index,1] = self.users[i.userId]['user'].name
                sheet[index,2] = self.users[i.userId]['user'].genre
                sheet[index,3] = self.users[i.userId]['user'].getAge()
                sheet[index,4] = self.users[i.userId]['user'].dni
                sheet[index,5] = i.degree
                sheet[index,6] = i.approved
                sheet[index,7] = i.average1
                index = index + 1

            fn = '/tmp/{}.xlsx'.format(str(uuid.uuid4()))
            doc.save(fn, pyoo.FILTER_EXCEL_2007)
            return fn

        finally:
            doc.close()

    def _attachOds(self, parts):
        fn = self._generateOds()
        f = open(fn,'r')
        try:
            content = f.read()
            parts.append(self.mailModel.getFilePart('datos.xlsx', content, content_type='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        finally:
            f.close()


    def _attachContent(self, parts):
        template = reg.get('mailTemplate')
        f = open(template,'r')
        try:
            content = f.read()
            parts.append(self.mailModel.getHtmlPart(content))
        finally:
            f.close()

    def _attachCvs(self, con, parts):
        for u in self.users:
            data = u['data']
            if data.cv is None:
                    continue

            meta = FileDAO.findById(con, data.cv)
            content = FileDAO.getContent(con, meta.id)
            if content is None:
                continue

            filedata = None
            if meta.codec[0] == 'binary':
                filedata = bytes(content)
            elif meta.codec[0] == 'base64':
                filedata = base64.b64decode(bytes(content))

            fn = '{}.pdf'.format(u['user'].dni)
            parts.append(self.mailModel.getFilePart(fn, filedata, content_type='application', subtype='pdf'))


    def sendMail(self, con):

        ''' cargo los datos basicos de la base '''
        self._loadInscriptions(con)
        self._loadUsers(con)

        ''' genero las partes del mail. contenido, planilla y cvs '''
        parts = []
        self._attachContent(con, parts)
        self._attachOds(parts)
        self._attachCvs(con, parts)

        ''' envío un mail a cada uno de los mails listados con el mensaje completo '''
        for mail in self.mails:
            m = self.mailModel.createMail('insercionlaboral@econo.unlp.edu.ar', email, 'Bolsa de trabajo FCE')
            for p in parts:
                m.attach(p)
            self.mailModel._sendMail('insercionlaboral@econo.unlp.edu.ar', mail, m)



class Sent:
    ''' datos de envíos a empresas '''
    def __init__(self):
        self.id = ''
        self.creation = None
        self.inscriptions = []
        self.emails = []

class SentDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create table laboral_insertion.sent (
                    id varchar primary key,
                    creation timestamp default now(),
                    inscriptions varchar[],
                    emails varchar[]
                )
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        s = Sent()
        s.id = r['id']
        s.creation = r['creation']
        s.inscriptions = r['inscriptions']
        s.emails = r['emails']

    @staticmethod
    def persist(con, s):
        ''' inserta un nuevo sent en la base '''
        cur = con.cursor()
        try:
            s.id = str(uuid.uuid4())
            ins = s.__dict__
            cur.execute('insert into laboral_insertion.sent (id, inscriptions, emails) values '
                        '(%(id)s, %(inscriptions)s, %(emails)s)', ins)
            return s.id
        finally:
            cur.close()

    @staticmethod
    def findAll(con):
        ''' obtiene todos los ids de los enviados '''
        cur = con.cursor()
        try:
            cur.execute('select id from laboral_insertion.sent')
            r = [c['id'] for c in cur]
            return r

        finally:
            cur.close()

    @staticmethod
    def findByInscriptionId(con, id):
        ''' obtiene los ids de los Sent que tengan una determinada inscripcion '''
        cur = con.cursor()
        try:
            cur.execute('select id from laboral_insertion.sent where %s = ANY(inscriptions)', (id,))
            r = [s['id'] for s in cur]
            return r

        finally:
            cur.close()

    @staticmethod
    def findById(con, ids=[]):
        ''' retorna las sent que tienen los ids pasados en la lista de parametros '''
        if len(ids) <= 0:
            return []

        cur = con.cursor()
        try:
            cur.execute('select * from laboral_insertion.sent where id in %s', (tuple(ids),))
            cs = [SentDAO._fromResult(c) for c in cur]
            return cs

        finally:
            cur.close()
