# -*- coding: utf-8 -*-
import uuid
import inject
import logging
from model.serializer.utils import MySerializer, JSONSerializable


class Contact(JSONSerializable):
    ''' datos de los contactos de la empresa '''
    def __init__(self):
        self.name = ''
        self.email = ''
        self.telephone = ''
        self.companyId = ''
        self.id = ''

class ContactDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create table laboral_insertion.contacts (
                    id varchar primary key,
                    name varchar,
                    email varchar,
                    telephone varchar,
                    company_id varchar not null references laboral_insertion.companies (id)
                )
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        c = Contact()
        c.id = r['id']
        c.name = r['name']
        c.email = r['email']
        c.telephone = r['telephone']
        c.companyId = r['company_id']
        return c

    @staticmethod
    def findById(con, ids):
        ''' obtiene el contacto identificado por el id '''
        assert ids is not None
        assert isinstance(ids, list)

        if len(ids) <= 0:
            return []

        cur = con.cursor()
        try:
            cur.execute('select * from laboral_insertion.contacts where id in %s', (tuple(ids),))
            if cur.rowcount <= 0:
                return []
            contacts = []
            for contact in cur:
                c = ContactDAO._fromResult(contact)
                contacts.append(c)
            return contacts

        finally:
            cur.close()

    @staticmethod
    def findByCompany(con, cId):
        ''' obtiene los ids de los contactos que posee la empresa con id igual a cId '''
        assert cId is not None
        cur = con.cursor()
        try:
            cur.execute('select id from laboral_insertion.contacts where company_id = %s', (cId,))
            ids = [ x['id'] for x in cur ]
            return ids
        finally:
            cur.close()

    @staticmethod
    def persist(con, contact):
        if contact is None:
            return

        cur = con.cursor()
        try:
            contact.id = str(uuid.uuid4())
            ins = contact.__dict__
            cur.execute('insert into laboral_insertion.contacts (id, name, email, telephone, company_id) values  '
                        '(%(id)s, %(name)s, %(email)s, %(telephone)s, %(companyId)s)', ins)

        finally:
            cur.close()


    @staticmethod
    def delete(con, ids):
        ''' elimina todos los contactos que esten en ids '''
        assert ids is not None
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('delete from laboral_insertion.contacts where id in %s', (tuple(ids),))
        finally:
            cur.close()

    @staticmethod
    def deleteByCompany(con, cId):
        if cId is None:
            return

        ids = ContactDAO.findByCompany(con, cId)
        if len(ids) <= 0:
            return
        ContactDAO.delete(con, ids)


class Company(JSONSerializable):
    ''' datos de una empresa de insercion laboral '''
    def __init__(self):
        self.name = ''
        self.detail = ''
        self.cuit = ''
        self.teacher = ''
        self.manager = ''
        self.address = ''
        self.id = ''
        self.contacts = []
        self.beginCM = None
        self.endCM = None

class CompanyDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute("""
                create table laboral_insertion.companies (
                    id varchar primary key,
                    name varchar not null,
                    detail varchar,
                    cuit varchar not null,
                    teacher varchar,
                    manager varchar,
                    address varchar,
                    begincm timestamptz default now(),
                    endcm timestamptz default now(),
                )
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        ''' carga los datos desde el resultado pasad por parametro '''
        c = Company()
        c.id = r["id"]
        c.name = r['name']
        c.detail = r['detail']
        c.cuit = r['cuit']
        c.teacher = r['teacher']
        c.manager = r['manager']
        c.address = r['address']
        c.beginCM = r['begincm']
        c.endCM = r['endcm']
        return c

    @staticmethod
    def findById(con, ids):
        ''' obtiene las empresas que esten en ids '''
        assert ids is not None
        assert isinstance(ids, list)

        if len(ids) <= 0:
            return []

        cur = con.cursor()
        try:
            cur.execute('select * from laboral_insertion.companies where id in %s', (tuple(ids),))
            if cur.rowcount <= 0:
                return []

            if cur.rowcount <= 0:
                return []

            companies = []
            for c in cur:
                company = CompanyDAO._fromResult(c)
                contactIds = ContactDAO.findByCompany(con, company.id)
                company.contacts = ContactDAO.findById(con, contactIds)
                companies.append(company)
            return companies

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
    def delete(con, ids):
        ''' elimina todas las compañias que esten en ids '''
        assert ids is not None
        assert isinstance(ids, list)

        cur = con.cursor()
        try:
            cur.execute('delete from laboral_insertion.companies where id in %s', (tuple(ids),))
        finally:
            cur.close()

    @staticmethod
    def verifyData(company):
        if not hasattr(company, 'address'):
            company.address = ''

    @staticmethod
    def persist(con, company):
        if company is None:
            return None

        cur = con.cursor()

        try:
            if not hasattr(company, 'id'):
                CompanyDAO.verifyData(company)
                company.id = str(uuid.uuid4())
                ins = company.__dict__
                cur.execute('insert into laboral_insertion.companies (id, name, detail, cuit, teacher, manager, address, beginCM, endCM) values ('
                            '%(id)s, %(name)s, %(detail)s, %(cuit)s, %(teacher)s, %(manager)s, %(address)s, %(beginCM)s, %(endCM)s)', ins)
            else:
                params = company.__dict__
                cur.execute('update laboral_insertion.companies set name = %(name)s, detail = %(detail)s, cuit = %(cuit)s, teacher = %(teacher)s, '
                            'manager = %(manager)s, address = %(address)s, beginCM = %(beginCM)s, endCM = %(endCM)s where id = %(id)s', params)

                ContactDAO.deleteByCompany(con, contact.id)

            for c in company.contacts:
                c.companyId = company.id
                ContactDAO.persist(con, c)

            return company.id

        finally:
            cur.close()
