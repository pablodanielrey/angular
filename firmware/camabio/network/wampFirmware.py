# -*- coding: utf-8 -*-

import logging, inject

#from autobahn.twisted.wamp import ApplicationSession
from autobahn.asyncio.wamp import ApplicationSession

import asyncio
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

    @coroutine
    def onJoin(self, details):
        logging.debug('session joined')

        self.firmware.start()

        yield from self.register(self.identify_async, 'assistance.firmware.identify')
        yield from self.register(self.enroll_async, 'assistance.firmware.enroll')
        yield from self.register(self.login_async, 'assistance.firmware.login')

        yield from self.register(self.testDate, 'assistance.firmware.testDate')


    def onLeave(self, details):
        logging.debug('session left')
        self.firmware.stop()



    ''' para testear si el datetime se puede serializar '''
    def testDate(self,date):
        logging.info('fecha obtenida : {}'.format(date))
        return date


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

    @coroutine
    def identify_async(self):
        loop = asyncio.get_event_loop()
        yield from loop.run_in_executor(None,self.identify)


    '''
        //////////////////////////////////
        proceso de login mediante credenciales de una persona
        //////////////////////////////////
    '''

    def login(self,dni,password):
        data = self.firmware.login(dni,password)
        self._sendIdentifyEvent(data)

    @coroutine
    def login_async(self,dni,password):
        loop = asyncio.get_event_loop()
        yield from loop.run_in_executor(None,self.login,dni,password)


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


    @coroutine
    def enroll_async(self, dni):
        loop = asyncio.get_event_loop()
        yield from loop.run_in_executor(None,self.enroll,dni)


    '''
        /////////////////////////////////
    '''
