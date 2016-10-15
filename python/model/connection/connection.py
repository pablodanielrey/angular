# -*- coding: utf-8 -*-
'''
    Implementa todo el codigo relacionado al modelo y las entidades de los usuarios
'''
import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor
import logging
import inject

from model.registry import Registry



class Connection:

    def __init__(self, registry=Registry()):
        self.host = registry.get('host')
        self.database = registry.get('database')
        self.user = registry.get('user')
        self.password = registry.get('password')
        self.pool = psycopg2.pool.ThreadedConnectionPool(1, 50, host=self.host, database=self.database, user=self.user, password=self.password, cursor_factory=DictCursor)

    def get(self):
        logging.debug('obteniendo conexion a la base')
        return self.pool.getconn()

    def put(self, conn):
        logging.debug('retornando la conexion al pool')
        self.pool.putconn(conn)

    def __del__(self):
        logging.debug('cerrando todas las conexiones a la base')
        self.pool.closeall()
