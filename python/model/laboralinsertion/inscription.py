# -*- coding: utf-8 -*-
import uuid

class Inscription:

    def __init__(self):
        self.id = None
        self.userId = None
        self.degree = None
        self.workType = None
        self.reside = False
        self.travel = False
        self.workExperience = False
        self.created = None
        self.average1 = 0
        self.average2 = 0
        self.approved = 0

class InscriptionDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create table laboral_insertion.inscriptions (
                    id varchar primary key,
                    user_id varchar not null references laboral_insertion.users (id)
                    reside boolean default false,
                    travel boolean default false,
                    degree varchar not null,
                    approved integer default 0,
                    average1 real default 0.0,
                    average2 real default 0.0,
                    work_type varchar not null,
                    created timestamptz default now(),
                    work_experience boolean default false
                )
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        i = Inscription()
        i.id = r['id']
        i.userId = r['user_id']
        i.degree = r['degree']
        i.workType = r['work_type']
        i.reside = r['reside']
        i.travel = r['travel']
        i.workExperience = r['work_experience']
        i.created = r['created']
        i.average1 = r['average1']
        i.average2 = r['average2']
        i.approved = r['approved']
        return i

    @staticmethod
    def persist(con, inscription):
        ''' un cambio de precondiciones, asi que lo dejo por las dudas '''
        inscription.__dict__['reside'] = False

        ''' crea o actualiza un registro de inscripcion en la base de datos '''
        cur = con.cursor()
        try:
            if inscription.id is None:
                inscription.id = str(uuid.uuid4())
                ins = inscription.__dict__
                cur.execute('insert into laboral_insertion.inscriptions (id, user_id, degree, work_type, reside, travel, work_experience, average1, average2, approved) values '
                            '(%(id)s, %(userId)s, %(degree)s, %(workType)s, %(reside)s, %(travel)s, %(workExperience)s, %(average1)s, %(average2)s, %(approved)s )', ins)
            else:
                cur.execute('update laboral_insertion.inscriptions (user_id = %(userId)s, degree = %(degree)s, work_type = %(workType)s, '
                            'reside = %(reside)s, travel = %(travel)s, average1 = %(average1)s, average2 = %(average2)s, approved = %(approved)s) where id = %(id)s', ins)

        finally:
            cur.close()

    @staticmethod
    def delete(con, id):
        """ elimina la inscripción con el id determinado """
        cur = con.cursor()
        try:
            cur.execute('delete from laboral_insertion.inscriptions where id = %s', (id,))
        finally:
            cur.close()


    @staticmethod
    def findAll(con):
        ''' obtiene todos los ids de todas las inscripciones '''
        cur = con.cursor()
        try:
            cur.execute("select id from laboral_insertion.inscriptions")
            ins = [ x['id'] for x in cur ]
            return ins

        finally:
            cur.close()

    @staticmethod
    def findByUser(con, userId):
        """ obtiene los datos de las inscripciones de los alumnos """
        cur = con.cursor()
        try:
            cur.execute('select id from laboral_insertion.inscriptions where user_id = %s', (userId,))
            ins = [ x['id'] for x in cur ]
            return ins

        finally:
            cur.close()

    @staticmethod
    def findById(con, id):
        ''' obtiene la inscripcion determinada por el id '''
        cur = con.cursor()
        try:
            cur.execute('select * from laboral_insertion.inscriptions where id = %s', (id,))
            if cur.rowcount <= 0:
                return None
            r = cur.fetchone()
            return InscriptionDAO._fromResult(r)

        finally:
            cur.close()
