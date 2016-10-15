"""
    Se definen métodos y propiedades comunes a todas las clases wamp
"""
import inject
inject.configure_once()

import logging

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


"""
    Se define un componente que puede ser cargado por corssbar.io en la config.
    Las clases componentes deben extender de SystemComponentSession
    existen 2 opciones para registrar los métodos dentro de wamp.
    1 - usando decoradores wamp

        @autobahn.wamp.register
        @autobahn.wamp.subscribe

    2 - reimplementado el método : getWampComponents() que retorna una lista de instancias que tienen
    métodos decorados como en el punto 1.

    Las credenciales para conectarse a la realm de crossbar la obtienen usando :

        wamp.getWampCredentials()

        que necesita una sección dentro de registry.cfg

        [crossbar]
        system_user = system
        system_password = password
        host = 127.0.0.1
        database = dcsys
        user = dcsys
        password = dcsys



    config de crossbar ejemplo :
        "components": [
                {
                    "id": "lp1",
                    "type": "class",
                    "classname": "mySystem.MyComponent",
                    "realm": "public",
                    "extra": {
                        "parametro1": "valor1"
                    },
                    "transport": {
                        "type": "websocket",
                        "endpoint": {
                            "type": "tcp",
                            "host": "127.0.0.1",
                            "port": 8080
                        },
                        "url": "ws://localhost:8080"
                    }
                }
        ]


"""
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
import autobahn

from model.login.login import Login

class SystemComponentSession(ApplicationSession):

    def getLogger(self):
        return logging.getLogger('{}.{}'.format(self.__module__ self.__class__.__name__))

    def getUserId(self, con, details):
        wampSessionId = details.caller
        username = details.caller_authid
        return Login.getUserIdByUsername(con, username)

    def getRegisterOptions(self):
        """
            debe retorar un objeto del tipo autobahn.wamp.RegisterOptions
        """
        return None

    def getWampComponents(self):
        """
            Retorna instancias de clases que tienen decorados usando
            @autobahn.wamp.register
            los métodos que necesitan exportar mediante Wamp
            Por defecto se retorna ella misma
        """
        return [self]

    def onConnect(self):
        username = getWampCredentials()['username']
        self.join(self.config.realm, ["ticket"], username)

    def onChallenge(self, challenge):
        if challenge.method == 'ticket':
            return getWampCredentials()['password']
        else:
            raise Exception('Invalid auth method {}'.format(challenge.method))

    @inlineCallbacks
    def onJoin(self, details):
        for o in self.getWampComponents():
            results = yield self.register(o, options=self.getRegisterOptions())
            results = yield self.subscribe(o)
