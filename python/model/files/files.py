# -*- coding: utf-8 -*-
import uuid
import hashlib
from model.dao import DAO

from model.serializer import JSONSerializable

class File(JSONSerializable):

    def __init__(self):
        self.id = None
        self.name = None
        self.hash = None
        self.content = None
        self.mimetype = None
        self.codec = None
        self.size = 0
        self.created = None
        self.modified = None

    def _calculateHash(self):
        self.hash = File._calculateHashStatic(self.content)

    def getContent(self, con):
        return self.getContentById(con, self.id)

    @staticmethod
    def _calculateHashStatic(content):
        m = hashlib.md5()
        m.update(content.encode('utf8'))
        return m.hexdigest()

    @classmethod
    def findById(cls, con, id):
        return FileDAO.findById(con, id)

    @classmethod
    def getContentById(cls, con, id):
        return FileDAO.getContent(con, id)


class FileDAO(DAO):

    @classmethod
    def _createSchema(cls, con):
        super()._createSchema(con)
        cur = con.cursor()
        try:
            sql = """
              CREATE SCHEMA IF NOT EXISTS files;

              CREATE TABLE IF NOT EXISTS files.files (
                  id VARCHAR NOT NULL PRIMARY KEY,
                  name VARCHAR NOT NULL,
                  hash VARCHAR,
                  content BYTEA,
                  mimetype VARCHAR DEFAULT 'application/binary',
                  codec VARCHAR DEFAULT 'base64',
                  size BIGINT DEFAULT 0,
                  created TIMESTAMPTZ DEFAULT now(),
                  modified TIMESTAMPTZ DEFAULT now()
              );
            """

            cur.execute(sql)
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
                        'values (%(id)s, %(name)s, %(hash)s, %(mimetype)s, %(codec)s, %(size)s, %(content)s)', p)
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
            if cur.rowcount <= 0:
                return None
            return cur.fetchone()['content']

        finally:
            cur.close()

    @staticmethod
    def check(con, id):
        ''' chequea que exista el file cargado en la base '''
        cur = con.cursor()
        try:
            cur.execute('select id from files.files where id = %s', (id,))
            return (cur.rowcount > 0)

        finally:
            cur.close()
