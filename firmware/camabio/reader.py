# -*- coding: utf-8 -*-
import cserial, camabio
import time, codecs, logging
import inject

from threading import Semaphore

import model
from model.config import Config



"""
    Reader nulo
    usado cuando se desactiva el reader en la config
"""
class Reader:

    def start(self):
        pass

    def stop(self):
        pass

    def identify(self):
        return None

    def enroll(self, need_first=None, need_second=None, need_third=None, need_release=None):
        return (None,None)




class FirmwareReader(Reader):

    config = inject.attr(Config)


    def __init__(self):

        """ passing the baton """
        self.entry = Semaphore(1)
        self.e = Semaphore(0)
        self.ne = 0
        self.de = 0

        self.i = Semaphore(0)
        self.ni = 0
        self.di = 0


    def start(self):
        port = self.config.configs['reader_port']
        cserial.open(port)

    def stop(self):
        cserial.close()


    """
        retorna un número de huella disponible para poder usar en el lector.
        None = error o no existe huella disponible
    """
    def getEmptyId(self):
        data = camabio.createPackage(0x0107,0x2,0x0)
        cserial.write(data)
        time.sleep(0.5)
        resp = cserial.readS(24)

        status = camabio.getAttrFromPackage(camabio.RET,resp)
        if status == camabio.ERR_FAIL:
            logging.warn('error en la respuesta')
            return None

        empty = camabio.getAttrFromPackage(camabio.DATA,resp)
        if empty == camabio.ERR_EMPTY_ID_NOEXIST:
            logging.warn('no existe espacio para huellas adicionales')
            return None

        return empty


    """
        retorna (number,template) el contenido del template y el numero de huella donde se encuentra en el lector
        None = error o no encuentra la huella
    """
    def readTemplate(self,id):
        data = camabio.createPackage(0x10a,0x2,id)
        cserial.write(data)

        time.sleep(0.5)
        resp = cserial.readS(24)
        logging.debug(resp)
        size = camabio.getAttrFromPackage(camabio.DATA,resp)

        time.sleep(0.5)
        rtmpl = cserial.readS(10 + size)
        logging.debug(rtmpl)

        r = camabio.extractResponseDataPackage(rtmpl)
        if r['PREFIX'] != 0x5aa5:
            return (None,None)

        if r['RCM'] != 0x10a:
            return (None,None)

        """ extraigo el contenido del paquete de datos """
        number = int.from_bytes(r['DATA'][0:2],byteorder='little')
        template = r['DATA'][2:]

        if (len(template) != (size - 2)):
            return (None,None)

        return (number,template)



    """
        el SIGNAL de la técnica passing the baton
    """
    def _signal(self):

        if self.de > 0 and self.di == 0:
            self.de = self.de - 1
            self.e.release()

        elif self.di > 0 and self.de == 0:
            self.di = self.di - 1
            self.i.release()

        elif self.di > 0 and self.de > 0:
            self.de = self.de - 1
            self.e.release()

        else:
            self.entry.release()



    """
        identifica la huella de una persona
    """
    def identify(self):

        """ <await (ne == 0 and ni == 0) ni = ni + 1> """
        self.entry.acquire()
        if (self.ne > 0 or self.ni > 0 or self.nc > 0):
            self.di = self.di + 1
            self.entry.release()
            logging.debug('identify esperando')
            self.i.acquire()
        self.ni = self.ni + 1
        self._signal()

        logging.debug('identify')
        try:
            data = camabio.createPackage(0x102,0,0)
            cserial.write(data)
            time.sleep(0.5)

            huella = None
            exit = False
            while not exit:
                resp = cserial.readS(24)
                ret = camabio.getAttrFromPackage(camabio.RET,resp)
                data = camabio.getAttrFromPackage(camabio.DATA,resp)
                exit = True

                if ret == camabio.ERR_FAIL:
                    if data == camabio.ERR_IDENTIFY:
                        logging.warn('no existe ninguna persona con esa huella')

                    if data == camabio.ERR_ALL_TMPL_EMPTY:
                        logging.warn('no existen huellas en el lector')

                    if data == camabio.ERR_TIME_OUT:
                        logging.warn('timeout')

                    if data == camabio.ERR_BAD_QUALITY:
                        logging.warn('mala calidad de la huella')

                    if data == camabio.ERR_FP_CANCEL:
                        logging.warn('identificación cancelada')

                elif ret == camabio.ERR_SUCCESS:

                    if data == camabio.GD_NEED_RELEASE_FINGER:
                        exit = False
                    else:
                        huella = data

                else:
                    logging.warn('respuesta desconocida')
                    logging.warn(codecs.encode(resp,'hex'))

            return huella

        finally:
            self.entry.acquire()
            self.ni = self.ni - 1
            self._signal()



    """
        retorna la (huella,template) despues de haber sido enrolada en el lector
        huella = número asignado dentro del lector a la huella
        template = template de la huella
    """
    def enroll(self, need_first=None, need_second=None, need_third=None, need_release=None):

        canceled = False

        """   <await (ne == 0 and ni == 0) ne = ne + 1> """
        self.entry.acquire()
        if (self.ne > 0 or self.de > 0):
            logging.debug('ya existe en ejecución/espera un enrolado')
            self._signal()
            return

        elif (self.ni > 0):
            self.de = self.de + 1
            self.entry.release()
            logging.debug('enroll esperando')

            """ disparo un cancel """
            canceled = True
            data = camabio.createPackage(0x130,0,0)
            cserial.write(data)

            self.e.acquire()

        self.ne = self.ne + 1
        self._signal()


        if canceled:
            resp = cserial.readS(24)
            ret = camabio.getAttrFromPackage(camabio.RET,resp)
            if ret != camabio.ERR_SUCCESS:
                logging.warn('se cancelo {} pero se leyo del serie {}'.format(self.status,codecs.encode(resp,'hex')))

        logging.debug('enroll')
        try:
            empty = self.getEmptyId()
            data = camabio.createPackage(0x0103,0x02,empty)
            cserial.write(data)

            time.sleep(0.5)

            fase = 0
            huella = None
            while huella is None:
                resp = cserial.readS(24)

                logging.debug(codecs.encode(resp,'hex'))

                err = camabio.getAttrFromPackage(camabio.RET,resp)
                rdata = camabio.getAttrFromPackage(camabio.DATA,resp)
                if err == camabio.ERR_FAIL:
                    """ error, proceso el error """
                    if rdata == camabio.ERR_INVALID_TMPL_NO:
                        logging.warn('error en el número de huella')
                        return (None,None)

                    if rdata == camabio.ERR_TMPL_NOT_EMPTY:
                        logging.warn('el número de huella no esta vacío')
                        return (None,None)

                    if rdata == camabio.ERR_TIME_OUT:
                        logging.warn('timeout')
                        continue

                    if rdata == camabio.ERR_BAD_QUALITY:
                        logging.warn('mala calidad')
                        continue

                    if rdata == camabio.ERR_GENERALIZE:
                        logging.warn('error generalizando las huellas')
                        return (None,None)

                    if rdata == camabio.ERR_DUPLICATION_ID:
                        pos = camabio.getIntFromPackage(camabio.DATA + 2,resp)
                        logging.warn('error, huella duplicada en la posición {}'.format(pos))
                        return (None,None)

                    if rdata == camabio.ERR_FP_CANCEL:
                        logging.warn('Se ha cancelado el comando de enrolado')
                        return (None,None)

                    logging.warn('error desconocido')
                    logging.warn(codecs.encode(resp,'hex'))
                    return (None,None)

                elif err == camabio.ERR_SUCCESS:

                    """ ok es un resultado """
                    if rdata == camabio.GD_NEED_FIRST_SWEEP:
                        if need_first:
                            need_first()
                        logging.debug('Necesita primera huella')
                        fase = 1
                        continue

                    if rdata == camabio.GD_NEED_SECOND_SWEEP:
                        if need_second:
                            need_second()
                        logging.debug('Necesita segunda huella')
                        fase = 2
                        continue

                    if rdata == camabio.GD_NEED_THIRD_SWEEP:
                        if need_third:
                            need_third()
                        logging.debug('Necesita tercera huella')
                        fase = 3
                        continue

                    if rdata == camabio.GD_NEED_RELEASE_FINGER:
                        if need_release:
                            need_release()
                        logging.debug('levante el dedo del lector')
                        continue

                    huella = rdata

                else:
                    logging.warn('estado desconocido')
                    logging.warn(codecs.encode(resp,'hex'))
                    return (None,None)

            if huella is None:
                return (None,None)

            (number,template) = self.readTemplate(huella)
            return (huella,template)

        finally:
            self.entry.acquire()
            self.ne = self.ne - 1
            self._signal()


"""
    el provider del reader
"""
def getReader():
    config = inject.instance(Config)
    if config.configs['reader_enable']:
        return inject.instance(FirmwareReader)
    else:
        return inject.instance(Reader)
