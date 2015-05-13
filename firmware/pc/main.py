# -*- coding: utf-8 -*-

import serial

#ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)


def getHex2Bytes(h):
    return h.to_bytes(2,byteorder='little')


cmd = getHex2Bytes(0xaa55) + getHex2Bytes(0x124)

print('{}'.format(cmd))
