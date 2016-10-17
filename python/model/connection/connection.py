# -*- coding: utf-8 -*-
'''
    Implementa todo el codigo relacionado al modelo y las entidades de los usuarios
'''
import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor
import inject

from model.registry import Registry


import logging
logging.basicConfig(format='%(asctime)s, %(stack_info)s, %(thread)s, %(message)s')
logging.getLogger().setLevel(logging.DEBUG)

import cProfile
def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return profiled_func

import traceback
def do_traceback(func):
    logging.basicConfig(format='%(asctime)s, %(stack_info)s, %(thread)s, %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)
    def tracebacked_func(*args, **kwargs):
        for line in traceback.format_stack():
            logging.info(line.strip())
        r = func(*args, **kwargs)
        return r
    return tracebacked_func


class Connection:

    logging = logging.getLogger(__name__)

    @classmethod
    def readOnly(cls, conn):
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    def __init__(self, registry=Registry()):

        self.logging.setLevel(logging.DEBUG)

        self.host = registry.get('host')
        self.database = registry.get('database')
        self.user = registry.get('user')
        self.password = registry.get('password')
        self.pool = psycopg2.pool.ThreadedConnectionPool(1, 50, host=self.host, database=self.database, user=self.user, password=self.password, cursor_factory=DictCursor)

    @do_traceback
    def get(self):
        self.logging.debug('obteniendo conexion a la base')
        return self.pool.getconn()

    @do_traceback
    def put(self, conn):
        self.logging.debug('retornando la conexion al pool')
        self.pool.putconn(conn)

    def __del__(self):
        self.logging.debug('cerrando todas las conexiones a la base')
        self.pool.closeall()
