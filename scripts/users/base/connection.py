# -*- coding: utf-8 -*-
'''
    Implementa todo el codigo relacionado al modelo y las entidades de los usuarios
'''
import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor

pool = psycopg2.pool.ThreadedConnectionPool(10, 20, host='163.10.17.80', database='dcsys', user='dcsys', password='dcsys', cursor_factory=DictCursor)


def getConnection():
    global pool
    return pool.getconn()


def closeConnection(con):
    global pool
    pool.putconn(con)
