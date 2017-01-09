# -*- coding: utf-8 -*-
import uuid
from model.dao import SqlDAO
from model.files.entities.file import File

class FileSqlDAO(SqlDAO):

    @classmethod
    def _createSchema(cls, ctx):
        super()._createSchema(ctx)
        cur = ctx.con.cursor()
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

    @classmethod
    def _fromResult(cls, f, r):
        f.id = r['id']
        f.name = r['name']
        f.hash = r['hash']
        f.mimetype = r['mimetype']
        f.codec = r['codec'],
        f.size = r['size'],
        f.created = r['created']
        f.modified = r['modified']
        return f

    @classmethod
    def persist(cls, ctx, f):
        ''' inserta o actualiza un archivo dentro de la base de datos '''
        cur = ctx.con.cursor()
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


    @classmethod
    def findAll(cls, ctx):
        cur = ctx.con.cursor()
        try:
            cur.execute('select id from files.files')
            return [ x['id'] for x in cur ]

        finally:
            cur.close()

    @classmethod
    def findByIds(cls, ctx, ids):
        cur = ctx.con.cursor()
        try:
            cur.execute('select * from files.files where id in %s', (tuple(ids),))
            return [cls._fromResult(File(), x) for x in cur]

        finally:
            cur.close()

    @classmethod
    def findByHash(cls, ctx, hash):
        cur = ctx.con.cursor()
        try:
            cur.execute('select id from files.files where hash = %s', (hash,))
            return [c['id'] for c in cur]

        finally:
            cur.close()

    @classmethod
    def getContentById(cls, ctx, id):
        ''' retorna el contenido del archivo identificado por el id '''
        cur = ctx.con.cursor()
        try:
            cur.execute('select content from files.files where id = %s', (id,))
            if cur.rowcount <= 0:
                return None
            return cur.fetchone()['content']

        finally:
            cur.close()

    @classmethod
    def exists(cls, ctx, id):
        ''' chequea que exista el file cargado en la base '''
        cur = ctx.con.cursor()
        try:
            cur.execute('select 1 from files.files where id = %s', (id,))
            return (cur.rowcount > 0)

        finally:
            cur.close()
