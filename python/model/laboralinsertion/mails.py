# -*- coding: utf-8 -*-
"""
    create table laboral_insertion.sent (
        id varchar primary key,
        creation timestamp default now(),
        inscriptions varchar[],
        emails varchar[]
    )
"""
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

    def persist(self, con):
        ''' inserta un nuevo sent en la base '''
        cur = con.cursor()
        try:
            self.id = str(uuid.uuid4())
            cur.execute('insert into laboral_insertion.sent (id, inscriptions, emails) values (%(id)s, %(inscriptions)s, %(emails)s)', self.__dict__)
            return self.id
        finally:
            cur.close()

    @staticmethod
    def loadFrom(r):
        ''' carga los datos desde el resultado pasad por parametro '''
        c = Sent()
        c.id = r['id']
        c.creation = r['creation']
        c.inscriptions = r['inscriptions']
        c.emails = r['emails']
        return c

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
            cs = [Sent.loadFrom(c) for c in cur]
            return cs

        finally:
            cur.close()
