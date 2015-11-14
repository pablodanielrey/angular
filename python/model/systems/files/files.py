# -*- coding: utf-8 -*-
import psycopg2
import uuid
import logging


class Files:

    '''
    create schema files
    create table files.files (
        id varchar not null primary key,
        name varchar not null,
        hash varchar,
        content text,
        created timestamptz default now()
    )
    '''

    '''
        Crea o actualiza un documento dentro de la base
    '''
    def persist(self, con, id, name, mimetype, codec, data):
        size = len(data) if data is not None else 0
        cur = con.cursor()
        if id is None:
            id = str(uuid.uuid4())
            #cur.execute('insert into files.files (id, name, content) values (%s,%s,%s)', (id, name, psycopg2.Binary(data)))
            cur.execute('insert into files.files (id, name, mimetype, codec, size, content) values (%s,%s,%s,%s,%s,%s)', (id, name, mimetype, codec, size, data))
        else:
            #cur.execute('update files.files set (name = %s, content = %s) where id = %s', (name, psycopg2.Binary(data), id))
            cur.execute('update files.files set (name = %s, content = %s, mimetype = %s, codec = %s, size = %s) where id = %s', (name, data, mimetype, codec, size, id))
        return id

    def findAllIds(self, con):
        cur = con.cursor()
        cur.execute('select id from files.files')
        if cur.rowcount <= 0:
            return []

        ids = []
        for c in cur:
            ids.append(c[0])
        return ids

    def check(self, con, id):
        """ chequea si existe un archivo con ese id """
        cur = con.cursor()
        cur.execute('select id from files.files where id = %s', (id,))
        return cur.rowcount > 0

    def findById(self, con, id):
        cur = con.cursor()
        cur.execute('select id, name, mimetype, codec, size, created, content from files.files where id = %s', (id,))
        if cur.rowcount <= 0:
            return None

        for d in cur:
            return {
                'id': d[0],
                'name': d[1],
                'mimetype': d[2],
                'codec': d[3],
                'size': d[4],
                'created': d[5],
                'content': d[6]
            }

    def findMetaDataById(self, con, id):
        cur = con.cursor()
        cur.execute('select id, name, mimetype, codec, size, created from files.files where id = %s', (id,))
        if cur.rowcount <= 0:
            return None

        for d in cur:
            return {
                'id': d[0],
                'name': d[1],
                'mimetype': d[2],
                'codec': d[3],
                'size': d[4],
                'created': d[5]
            }

    def search(self, con, text):
        '''
            falta implementar
        '''

    def remove(self, con, id):
        '''
            falta implementar
        '''
