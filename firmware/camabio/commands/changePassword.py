# -*- coding: utf-8 -*-

import sys
sys.path.append('../../../python')

import inject, logging
import psycopg2

from model.config import Config

''' configuro el injector con las variables apropiadas '''
def config_injector(binder):
    binder.bind(Config,Config('firmware-config.cfg'))

inject.configure(config_injector)
config = inject.instance(Config)

def getDb():
    global config
    return psycopg2.connect(host=config.configs['database_host'], dbname=config.configs['database_database'], user=config.configs['database_user'], password=config.configs['database_password'])

logging.getLogger().setLevel(logging.INFO)


from model.users.users import Users
from model.credentials.credentials import UserPassword



if __name__ == '__main__':

    if (len(sys.argv) < 3):
        logging.warn('python3 {} dni clave'.format(sys.argv[0]))
        sys.exit(1)

    dni = sys.argv[1]
    password = sys.argv[2]

    conn = getDb()
    try:
        users = inject.instance(Users)
        user = users.findUserByDni(conn,dni)
        if not user:
            logging.warn('No existe ese usuario')
            sys.exit(1)

        logging.info(user)
        userId = user['id']

        creds = {
            'user_id':userId,
            'password':password,
            'username':dni
        }
        userPassword = inject.instance(UserPassword)

        ud = userPassword.findUserPassword(conn,creds)
        if ud:
            userPassword.updateUserPassword(conn,creds)
        else:
            userPassword.createUserPassword(conn,creds)

        conn.commit()

        ''' busco nuevamente la info '''
        ud = userPassword.findUserPassword(conn,creds)
        logging.info(ud)


    finally:
        conn.close()
