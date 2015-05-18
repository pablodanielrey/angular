# -*- coding: utf-8 -*-
import codecs


ERR_SUCCESS = 0x00
ERR_FAIL = 0x01
ERR_VERIFY = 0x11
ERR_IDENTIFY = 0x12
ERR_TMPL_EMPTY = 0x13
ERR_TMPL_NOT_EMPTY = 0x14
ERR_ALL_TMPL_EMPTY = 0x015
ERR_EMPTY_ID_NOEXIST = 0x16
ERR_BROKEN_ID_NOEXIST = 0x017
ERR_INVALID_TMPL_DATA = 0x18
ERR_DUPLICATION_ID = 0x19
ERR_BAD_QUALITY = 0x21
ERR_TIME_OUT = 0x23
ERR_NOT_AUTHORIZED = 0x24
ERR_GENERALIZE = 0x30
ERR_FP_CANCEL = 0x41
ERR_INTERNAL = 0x50
ERR_MEMORY = 0x51
ERR_EXCEPTION = 0x52
ERR_INVALID_TMPL_NO = 0x60
ERR_INVALID_SEC_VAL = 0x61
ERR_INVALID_TIME_OUT = 0x62
ERR_INVALID_BAUDRATE = 0x63
ERR_DEVICE_ID_EMPTY = 0x64
ERR_INVALID_DUP_VAL = 0x65
ERR_INVALID_PARAM = 0x70
ERR_NO_RELEASE = 0x71
GD_DOWNLOAD_SUCCESS = 0xa1
GD_NEED_FIRST_SWEEP = 0xfff1
GD_NEED_SECOND_SWEEP = 0xfff2
GD_NEED_THIRD_SWEEP = 0xfff3
GD_NEED_RELEASE_FINGER = 0xfff4
GD_DETECT_FINGER = 0x01
GD_NO_DETECT_FINGER = 0x00
GD_TEMPLATE_NOT_EMPTY = 0x01
GD_TEMPLATE_EMPTY = 0x00




""" calcula el checksum en el paquete de datos """
def calcChksum(data):
    sum = 0
    for i in range(len(data) - 2):
        sum = (sum + data[i]) & 0xffff
    return sum

""" setea el checksum en el paquete de datos """
def setChksum(data):
    sum = calcChksum(data)
    data[len(data) - 2] = (sum & 0xff)
    data[len(data) - 1] = ((sum & 0xff00) >> 8)


""" chequea que el chksum del paquete este ok """
def verifyChksum(data):
    sum = calcChksum(data)
    l = len(data)
    sump = ((data[l - 1] << 8) + data[l - 2])
    return (sum == sump)



def getHex2(h):
    return h.to_bytes(2,byteorder='little')

"""
    genera el paquete de comando.
    toma los datos como enteros, en hex o en base10
    ej :
    createPackage(0x10a,0x2,datos)
"""
def createPackage(cmd,l,d):
    pref = getHex2(0xaa55)
    cmd = getHex2(cmd)
    l = getHex2(l)
    d = int(d).to_bytes(2,byteorder='little')
    data = pref + cmd + l + d
    data = list(data) + [0 for _ in range(24 - len(data))]
    setChksum(data)
    return data



def getIntFromPackage(i,data):
    t = data[i:i+2]
    n = int.from_bytes(t,byteorder='little')
    return n


"""
    ej:
        getAttrFromPackage(CMD,pkg) --> 0x010a
"""
PREFIX = 0
CMD = 2
LEN = 4
PARAM = 6
CHKSUM = 22

def getAttrFromPackage(att,data):
    return getIntFromPackage(att,data)


def printPackage(data):
    print('prefix {}, cmd {}, len {}, param {}, chksum {}'.format(
        hex(getAttrFromPackage(PREFIX,data)),
        hex(getAttrFromPackage(CMD,data)),
        hex(getAttrFromPackage(LEN,data)),
        getAttrFromPackage(PARAM,data),
        hex(getAttrFromPackage(CHKSUM,data)))
    )
