# -*- coding: utf-8 -*-
import sys, logging, time
import camabio, cserial


if len(sys.argv) <= 1:
    sys.exit(1)


port = sys.argv[1]

cserial.open(port)



"""
    obtengo el id de la siguiente huella disponible
"""
cmd = 0x0107
data = camabio.createPackage(0x0107,0x2,0x0)
cserial.write(data)
time.sleep(0.5)
resp = cserial.readS(24)

status = camabio.getAttrFromPackage(camabio.RET,resp)
if status == camabio.ERR_FAIL:
    cserial.close()
    logging.warn('error en la respuesta')
    sys.exit(1)

empty = camabio.getAttrFromPackage(camabio.DATA,resp)
if empty == camabio.ERR_EMPTY_ID_NOEXIST:
    logging.warn('no existe espacio para huellas adicionales')


print('primera huella a poder utilizar : {}'.format(empty))

cserial.close()
