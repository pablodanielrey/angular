# -*- coding: utf-8 -*-
'''
    Implementa todo el codigo relacionado a la obtención de la conección de la base de datos.
'''
import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor

pool = psycopg2.pool.ThreadedConnectionPool(10, 20, host='127.0.0.1', database='dovecot', user='dovecot', password='tocevod', cursor_factory=DictCursor)


def getConnection():
    global pool
    return pool.getconn()


def closeConnection(con):
    global pool
    pool.putconn(con)
