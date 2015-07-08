# -*- coding: utf-8 -*-

import sys
sys.path.append('../../../python')

import inject, logging
import psycopg2

from model.config import Config

""" configuro el injector con las variables apropiadas """
def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)

def getDb():
    global config
    return psycopg2.connect(host=config.configs['database_host'], dbname=config.configs['database_database'], user=config.configs['database_user'], password=config.configs['database_password'])



from model.users.users import Users
from model.credentials.credentials import UserPassword



if __name__ == '__main__':

    conn = getDb()
    try:
        users = inject.instance(Users)
        us = users.listUsers(conn)
        for u in us:
            logging.info(u)

        ''' conn.commit() '''

    finally:
        conn.close()
