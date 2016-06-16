import cserial, camabio
import codecs, time, codecs
import sys

"""
Command Packet
PREFIX 0xAA55
CMD 0x010A
LEN 2
DATA Template No.
CKS Check Sum

Response Packet
PREFIX 0x55AA
RCM 0x010A
LEN 4
RET ERR_SUCCESS or ERR_FAIL
DATA Success: Template Record Size + 2 -- Fail:Error code -- ERR_INVALID_TMPL_NO o ERR_TMPL_EMPTY
CKS Check Sum
"""


if len(sys.argv) <= 2:
    sys.exit(1)

port = sys.argv[1]
tmpl = int(sys.argv[2])

"""
data = [0x55,0xaa,0x0a,0x01,0x02,0x00,0x01,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x00]
"""
data = camabio.createPackage(0x10a,0x2,tmpl)

cserial.open(port)
try:
    cserial.write(data)
    time.sleep(0.5)
    resp = cserial.readS(24)
    time.sleep(0.5)

    size = camabio.getAttrFromPackage(camabio.DATA,resp)
    size = size - 2

    tmpl = cserial.readS(2 + 2 + 2 + 2 + 2 + size + 2)

    print('r : {}'.format(codecs.encode(resp,'hex')))
    print('t : {}'.format(camabio.getIntFromPackage(8,resp)))
    print('tmpl : {}, len : {}'.format(codecs.encode(tmpl,'hex'),len(tmpl)))
    print('tmplate : {}'.format(codecs.encode(tmpl[10:10+size],'hex')))

finally:
    cserial.close()
