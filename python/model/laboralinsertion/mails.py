# -*- coding: utf-8 -*-

import uuid
import inject
import logging

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
