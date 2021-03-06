import sys
sys.path.append('../')

import serial
import time
import codecs
import camabio
import sys
import cserial

"""
Command Packet
PREFIX 0xAA55
CMD 0x0107
LEN 0
DATA Null
CKS Check Sum

Response Packet
PREFIX 0x55AA
RCM 0x0107
LEN 4
RET ERR_SUCCESS or ERR_FAIL
DATA 2byte Success: template No. that can be utilized. Fail: ERR_EMPTY_ID_NOEXIST
CKS Check Sum
"""

if len(sys.argv) <= 1:
    sys.exit(1)


port = sys.argv[1]

data = [0x55,0xaa,0x07,0x01,0x00,0x00,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x00]
camabio.setChksum(data)

cserial.writeAndRead(port,data)
