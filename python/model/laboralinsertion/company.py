# -*- coding: utf-8 -*-
"""
    create table laboral_insertion.companies (
        id varchar primary key,
        name varchar not null,
        address varchar,
        telephones varchar[],
        emails varchar[]
    )
"""
import uuid
import inject
import logging


class Company:
    ''' datos de una empresa de insercion laboral '''
    def __init__(self):
        self.name = ''
        self.address = ''
        self.telephones = []
        self.emails = []
        self.cuit = ''


class CompanyDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create table laboral_insertion.companies (
                    id varchar primary key,
                    name varchar not null,
                    address varchar,
                    telephones varchar[],
                    emails varchar[]
                )
            """)
        finally:
            cur.close()
            
    @staticmethod
    def _loadFrom(r):
        ''' carga los datos desde el resultado pasad por parametro '''
        c = Company()
        c.name = r['name']
        c.address = r['address']
        c.telephones = r['telephones']
        c.emails = r['emails']
        return c

    @staticmethod
    def findById(con, id):
        ''' obtiene una Company dada el id '''
        cur = con.cursor()
        try:
            cur.execute('select * from laboral_insertion.companies where id = %s', (id,))
            if cur.rowcount <= 0:
                return None
            r = cur.fetchone()
            return Company._loadFrom(r)

        finally:
            cur.close()

    @staticmethod
    def findAll(con):
        ''' obtiene todos los ids de las companies '''
        cur = con.cursor()
        try:
            cur.execute('select id from laboral_insertion.companies')
            r = [c['id'] for c in cur]
            return r

        finally:
            cur.close()

    @staticmethod
    def findById(con, ids=[]):
        ''' retorna las companías que tienen los ids pasados en la lista de parametros '''
        if len(ids) <= 0:
            return []

        cur = con.cursor()
        try:
            cur.execute('select * from laboral_insertion.companies where id in %s', (tuple(ids),))
            cs = [Company._loadFrom(c) for c in cur]
            return cs

        finally:
            cur.close()
