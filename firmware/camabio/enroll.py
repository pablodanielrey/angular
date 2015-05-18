# -*- coding: utf-8 -*-
import sys, logging, time, codecs
import camabio, cserial

logging.getLogger().setLevel(logging.INFO)

if len(sys.argv) <= 1:
    sys.exit(1)


port = sys.argv[1]

cserial.open(port)
try:


    """
        obtengo el id de la siguiente huella disponible
    """
    data = camabio.createPackage(0x0107,0x2,0x0)
    cserial.write(data)
    time.sleep(0.5)
    resp = cserial.readS(24)

    status = camabio.getAttrFromPackage(camabio.RET,resp)
    if status == camabio.ERR_FAIL:
        logging.warn('error en la respuesta')
        sys.exit(1)

    empty = camabio.getAttrFromPackage(camabio.DATA,resp)
    if empty == camabio.ERR_EMPTY_ID_NOEXIST:
        logging.warn('no existe espacio para huellas adicionales')

    logging.info('primera huella a poder utilizar : {}'.format(empty))


    """
        enrolo la huella nueva en el reloj, en la posición libre
    """
    data = camabio.createPackage(0x0103,0x02,empty)
    cserial.write(data)
    time.sleep(0.5)

    fase = 0
    huella = None
    while huella is None:
        resp = cserial.readS(24)

        logging.info(codecs.encode(resp,'hex'))

        err = camabio.getAttrFromPackage(camabio.RET,resp)
        rdata = camabio.getAttrFromPackage(camabio.DATA,resp)
        if err == camabio.ERR_FAIL:
            """ error, proceso el error """
            if rdata == camabio.ERR_INVALID_TMPL_NO:
                logging.warn('error en el número de huella')
                sys.exit(1)

            if rdata == camabio.ERR_TMPL_NOT_EMPTY:
                logging.warn('el número de huella no esta vacío')
                sys.exit(1)

            if rdata == camabio.ERR_TIME_OUT:
                logging.warn('timeout')
                continue

            if rdata == camabio.ERR_BAD_QUALITY:
                logging.warn('mala calidad')
                continue

            if rdata == camabio.ERR_GENERALIZE:
                logging.warn('error generalizando las huellas')
                sys.exit(1)

            if rdata == camabio.ERR_DUPLICATION_ID:
                pos = camabio.getIntFromPackage(camabio.DATA + 2,resp)
                logging.warn('error, huella duplicada en la posición {}'.format(pos))
                sys.exit(1)


            logging.warn('error desconocido')
            logging.warn(codecs.encode(resp,'hex'))
            break

        elif err == camabio.ERR_SUCCESS:

            """ ok es un resultado """
            if rdata == camabio.GD_NEED_FIRST_SWEEP:
                logging.info('Necesita primera huella')
                fase = 1
                continue

            if rdata == camabio.GD_NEED_SECOND_SWEEP:
                logging.info('Necesita segunda huella')
                fase = 2
                continue

            if rdata == camabio.GD_NEED_THIRD_SWEEP:
                logging.info('Necesita tercera huella')
                fase = 3
                continue

            if rdata == camabio.GD_NEED_RELEASE_FINGER:
                logging.info('levante el dedo del lector')
                continue

            huella = rdata

        else:
            logging.warn('estado desconocido')
            logging.warn(codecs.encode(resp,'hex'))
            break


    logging.info('Se ha almacenado correctamente la huella en la posición : {}'.format(huella))

finally:
    cserial.close()
