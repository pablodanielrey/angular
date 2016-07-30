"""
    Se definen métodos y propiedades comunes a todas las clases wamp
"""
import inject
inject.configure_once()

from model.registry import Registry
from model.connection.connection import Connection

reg = inject.instance(Registry)
crossbar = reg.getRegistry('crossbar')
system_user = crossbar.get('system_user')
system_password = crossbar.get('system_password')
conn = None


def getWampCredentials():
    global system_user, system_password
    return {'username': system_user, 'password': system_password}

def getConnectionManager():
    global conn
    if conn == None:
        conn = Connection(crossbar)
    return conn
