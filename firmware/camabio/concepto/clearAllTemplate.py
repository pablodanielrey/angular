import camabio, cserial
import sys, time, logging

"""
Command Packet
PREFIX 0xAA55
CMD 0x0106
LEN 0
DATA Null
CKS Check Sum

Response Packet
PREFIX 0x55AA
RCM 0x0106
LEN 4
RET ERR_SUCCESS or ERR_FAIL
DATA 2byte Success:Total number of deleted template Fail:Error code
CKS Check Sum
"""

"""
data = [0x55,0xaa,0x06,0x01,0x00,0x00,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x00]
"""


if len(sys.argv) <= 1:
    sys.exit(1)

port = sys.argv[1]

cserial.open(port)
data = camabio.createPackage(0x106,0x0,0x0)
cserial.write(data)
time.sleep(0.5)
resp = cserial.readS(24)

ret = camabio.getAttrFromPackage(camabio.RET,resp)
data = camabio.getAttrFromPackage(camabio.DATA,resp)

print('ret : {}, data : {}'.format(ret,data))

cserial.close()
