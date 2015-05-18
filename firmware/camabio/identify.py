# -*- coding: utf-8 -*-
import sys, logging, time, codecs
import camabio, cserial

logging.getLogger().setLevel(logging.INFO)

if len(sys.argv) <= 1:
    sys.exit(1)

port = sys.argv[1]
cserial.open(port)
try:

    identify = True
    while identify:

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
                    identify = False

                if data == camabio.ERR_ALL_TMPL_EMPTY:
                    logging.warn('no existen huellas en el lector')
                    identify = False

                if data == camabio.ERR_TIME_OUT:
                    logging.warn('timeout')

                if data == camabio.ERR_BAD_QUALITY:
                    logging.warn('mala calidad de la huella')

            elif ret == camabio.ERR_SUCCESS:

                if data == camabio.GD_NEED_RELEASE_FINGER:
                    exit = False
                else:
                    huella = data

            else:
                logging.warn('respuesta desconocida')
                logging.warn(codecs.encode(resp,'hex'))


        if huella:
            logging.info('Huella identificada número : {}'.format(huella))



finally:
    logging.info('cerrando puerto serie')
    cserial.close()
