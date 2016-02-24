# -*- coding: utf-8 -*-

class Inscription:

    def __init__(self):
        self.id = None
        self.user_id = None
        self.degree = None
        self.workType = None
        self.reside = False
        self.travel = False
        self.workExperience = False
        self.created = None


class InscriptionDAO:

    @staticmethod
    def _fromResult(r):
        i = Inscription()
        i.id = r['id']
        i.user_id = r['user_id']
        i.

    @staticmethod
    def persist(con, inscription):
        ''' crea o actualiza un registro de inscripcion en la base de datos '''
        cur = con.cursor()
        try:
            if inscription.id is None:
                inscription.id = str(uuid.uuid4())
                ins = inscription.__dict__
                cur.execute('insert into laboral_insertion.inscriptions (id, user_id, degree, work_type, reside, travel, work_experience) values '
                            '(%(id)s, %(userId)s, %(degree)s, %(workType)s, %(reside)s, %(travel)s, %(workExperience)s)', ins)
            else:
                cur.execute('update laboral_insertion.inscriptions (user_id = %(userId)s, degree = %(degree)s, work_type = %(workType)s, '
                            'reside = %(reside)s, travel = %(travel)s) where id = %(id)s', ins)

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


class Averages:
    ''' Promedios definidos para las carreras de las personas '''

    def __init__(self):
        self.id = None
        self.userId = None
        self.degree = None
        self.average1 = 0
        self.average2 = 0
        self.approved = 0
        self.created = None
