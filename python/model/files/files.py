# -*- coding: utf-8 -*-
import uuid
import hashlib


class File:

    def __init__(self):
        self.id = None
        self.name = None
        self.hash = None
        self.content = None
        self.mimetype = None
        self.cocec = None
        self.size = 0
        self.created = None
        self.modified = None

    def _calculateHash(self):
        self.hash = File._calculateHashStatic(self.content)

    @staticmethod
    def _calculateHashStatic(self, content):
        m = hashlib.md5()
        m.update(self.content)
        return m.hexdigest()


class FileDAO:

    @staticmethod
    def _createSchema(con):
        cur = con.cursor()
        try:
            cur.execute('create schema if not exists files')
            cur.execute("""
                create table files.files (
                    id varchar not null primary key,
                    name varchar not null,
                    hash varchar,
                    content bytea,
                    mimetype varchar default 'application/binary',
                    codec varchar default 'base64',
                    size default 0,
                    created timestamptz default now(),
                    modified timestampz default now()
                )
            """)
        finally:
            cur.close()

    @staticmethod
    def _fromResult(r):
        f = File()
        f.id = r['id']
        f.name = r['name']
        f.hash = r['hash']
        f.mimetype = r['mimetype']
        f.codec = r['codec'],
        f.size = r['size'],
        f.created = r['created']
        f.modified = r['modified']
        return f

    @staticmethod
    def persist(con, f):
        ''' inserta o actualiza un archivo dentro de la base de datos '''
        cur = con.cursor()
        if f.id is None:
            f.id = str(uuid.uuid4())
            p = f.__dict__
            #cur.execute('insert into files.files (id, name, content) values (%s,%s,%s)', (id, name, psycopg2.Binary(data)))
            cur.execute('insert into files.files (id, name, hash, mimetype, codec, size, content) '
                        'values (%(id)s, %(name)s, %(hash)s, %(mimetype)s, %(codec)s, %(size)s', p)
        else:
            p = f.__dict__
            #cur.execute('update files.files set (name = %s, content = %s) where id = %s', (name, psycopg2.Binary(data), id))
            cur.execute('select hash from files.files where id = %s', (f.id))
            if cur.fetchone()['hash'] == f.hash:
                ''' el contenido no cambio asi que no lo actualizo '''
                cur.execute('update files.files set (name = %(name)s, mimetype = %(mimetype)s, codec = %(codec)s, size = %(size)s, modified = NOW()) where id = %(id)s', p)
            else:
                cur.execute('update files.files set (name = %(name)s, content = %(content)s, mimetype = %(mimetype)s, hash = %(hash)s, codec = %(codec)s, size = %(size)s, modified = NOW()) where id = %(id)s', p)

        return f.id


    @staticmethod
    def findAll(con):
        cur = con.cursor()
        try:
            cur.execute('select id from files.files')
            ins = [ x['id'] for x in cur ]
            return ins
        finally:
            cur.close()

    @staticmethod
    def findById(con, id):
        cur = con.cursor()
        try:
            cur.execute('select id, name, hash, mimetype, codec, size, created, modified from files.files where id = %s', (id,))
            ins = [ FileDAO._fromResult(x) for x in cur ]
            return ins[0]

        finally:
            cur.close()

    @staticmethod
    def findByHash(con, hash):
        cur = con.cursor()
        try:
            cur.execute('select id, name, hash, mimetype, codec, size, created, modified from files.files where hash = %s', (hash,))
            ins = [ FileDAO._fromResult(x) for x in cur ]
            return ins

        finally:
            cur.close()

    @staticmethod
    def getContent(con, id):
        ''' retorna el contenido del archivo identificado por el id '''
        cur = con.cursor()
        try:
            cur.execute('select content from files.files where id = %s', (id,))
            return r['content']

        finally:
            cur.close()
