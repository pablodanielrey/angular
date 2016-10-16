# -*- coding: utf-8 -*-
'''
    Implementa todo el codigo relacionado al modelo y las entidades de los usuarios
'''
import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor
import inject

from model.registry import Registry

import traceback
import logging
logging.basicConfig(format='%(asctime)s, %(stack_info)s, %(thread)s, %(message)s')

class Connection:

    logging = logging.getLogger(__name__)

    @classmethod
    def readOnly(cls, conn):
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    def __init__(self, registry=Registry()):
        self.host = registry.get('host')
        self.database = registry.get('database')
        self.user = registry.get('user')
        self.password = registry.get('password')
        self.pool = psycopg2.pool.ThreadedConnectionPool(1, 50, host=self.host, database=self.database, user=self.user, password=self.password, cursor_factory=DictCursor)

    def get(self):
        self.logging.debug('obteniendo conexion a la base')
        #for line in traceback.format_stack():
        #    self.logging.debug(line.strip())
        return self.pool.getconn()

    def put(self, conn):
        self.logging.debug('retornando la conexion al pool')
        #for line in traceback.format_stack():
        #    self.logging.debug(line.strip())
        self.pool.putconn(conn)

    def __del__(self):
        self.logging.debug('cerrando todas las conexiones a la base')
        self.pool.closeall()
