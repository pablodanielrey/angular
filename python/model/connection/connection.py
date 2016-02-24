# -*- coding: utf-8 -*-
'''
    Implementa todo el codigo relacionado al modelo y las entidades de los usuarios
'''
import psycopg2
from psycopg2 import pool
from psycopg2.extras import DictCursor
import inject

from registry import Registry



class Connection:

    registry = inject.attr(Registry)

    def __init__(self):
        self.name = '{}.{}'.format(self.__class__.__module__, self.__class__.__name__)
        self.host = self.registry.get(self.name, 'host')
        self.database = self.registry.get(self.name, 'database')
        self.user = self.registry.get(self.name, 'user')
        self.password = self.registry.get(self.name, 'password')
        self.pool = psycopg2.pool.ThreadedConnectionPool(10, 20, host=self.host, database=self.database, user=self.user, password=self.password, cursor_factory=DictCursor)

    def get(self):
        return self.pool.getconn()

    def put(self, conn):
        self.pool.putconn(conn)
