# -*- coding: utf-8 -*-
import cserial, camabio
import time, codecs, logging

class Firmware:

    def __init__(self,port):
        self.port = port


    def start(self):
        cserial.open(self.port)

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
        retorna la (huella,template) despues de haber sido enrolada en el lector
        huella = número asignado dentro del lector a la huella
        template = template de la huella
    """
    def enroll(self):
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


                logging.warn('error desconocido')
                logging.warn(codecs.encode(resp,'hex'))
                return (None,None)

            elif err == camabio.ERR_SUCCESS:

                """ ok es un resultado """
                if rdata == camabio.GD_NEED_FIRST_SWEEP:
                    logging.debug('Necesita primera huella')
                    fase = 1
                    continue

                if rdata == camabio.GD_NEED_SECOND_SWEEP:
                    logging.debug('Necesita segunda huella')
                    fase = 2
                    continue

                if rdata == camabio.GD_NEED_THIRD_SWEEP:
                    logging.debug('Necesita tercera huella')
                    fase = 3
                    continue

                if rdata == camabio.GD_NEED_RELEASE_FINGER:
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
