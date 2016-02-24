# -*- coding: utf-8 -*-

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
    def findAll(con):
        ''' obtiene todos los ids de todas las inscripciones '''
        cur = con.cursor()
        try:
            cur.execute('select id from laboral_insertion.inscriptions')
            ins = [ x['id'] for x in cur ]
            return ins

        finally:
            cur.close()

    @staticmethod
    def findById(con):
        ''' obtiene la inscripcion determinada por el id '''
        cur = con.cursor()
        try:
            cur.execute('select * from laboral_insertion.inscriptions')
            ins = [ InscriptionDAO._fromResult(x) for x in cur ]
            return ins

        finally:
            cur.close()
