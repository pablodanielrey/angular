# -*- coding: utf-8 -*-

import logging, inject

#from autobahn.twisted.wamp import ApplicationSession
from autobahn.asyncio.wamp import ApplicationSession

from asyncio import coroutine

from firmware import Firmware




'''
    Clase que da acceso mediante wamp a los métodos del firmware
'''
class WampFirmware(ApplicationSession):

    def __init__(self,config=None):
        logging.debug('instanciando WampFirmware')
        ApplicationSession.__init__(self, config)
        self.firmware = inject.instance(Firmware)

    '''
    como referencia tambien se puede sobreeescribir el onConnect
    def onConnect(self):
        logging.debug('transport connected')
        self.join(self.config.realm)
    '''


    def onJoin(self, details):
        logging.debug('session joined')

        self.firmware.start()

        self.register(self.identify, 'assistance.firmware.identify')
        self.register(self.enroll, 'assistance.firmware.enroll')
        self.register(self.login, 'assistance.firmware.login')


    def onLeave(self, details):
        logging.debug('session left')
        self.firmware.stop()





    '''
        ///////////////
        evento de identificación de una persona para otros componentes del sistema
        /////////////
    '''

    def _sendIdentifyEvent(self, data):
        if data:
            (log,user,sid,roles) = data

            ''' publico el evento de identificación '''
            msg = {
                'log':log,
                'user':user,
                'sid':sid
            }
            if roles:
                msg['profile'] = 'admin'

            self.publish('assistance.firmware.identify',msg)

        else:
            msg = {
                'error':'Credenciales Incorrectas'
            }
            self.publish('assistance.firmware.identify',msg)




    '''
        //////////////////////////////////
        proceso de identificación de una persona -- llamado normalmente por un bulce en main
        //////////////////////////////////
    '''
    def identify(self):
        data = self.firmware.identify()
        self._sendIdentifyEvent(data)
        return data

    '''
        //////////////////////////////////
        proceso de login mediante credenciales de una persona
        //////////////////////////////////
    '''

    def login(self,dni,password):
        data = self.firmware.login(dni,password)
        self._sendIdentifyEvent(data)


    '''
        //////////////////////////////////
        proceso de enrolado de una persona
        //////////////////////////////////
    '''


    def _enroll_need_first(self):
        self.publish('assistance.firmware.enroll_need_finger',1)

    def _enroll_need_second(self):
        self.publish('assistance.firmware.enroll_need_finger',2)

    def _enroll_need_third(self):
        self.publish('assistance.firmware.enroll_need_finger',3)

    def _enroll_need_release(self):
        self.publish('assistance.firmware.enroll_show_message','Levante el dedo')

    def _enroll_error(self,msg):
        self.publish('assistance.firmware.enroll_error',msg)

    def _enroll_fatal_error(self,msg):
        self.publish('assistance.firmware.enroll_fatal_error',msg)


    def enroll(self,dni):
        self.firmware.enroll(
                dni,
                self._enroll_need_first,
                self._enroll_need_second,
                self._enroll_need_third,
                self._enroll_need_release,
                self._enroll_error,
                self._enroll_fatal_error
            )


    '''
        /////////////////////////////////
    '''
