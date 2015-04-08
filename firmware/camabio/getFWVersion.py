import array
import serial
import camabio

"""
Command Packet
PREFIX 0xAA55
CMD 0x0112
LEN 0
DATA Null
CKS Check Sum

Response Packet
PREFIX 0x55AA
RCM 0x0112
LEN 4
RET ERR_SUCCESS or ERR_FAIL

-- DATA 2byte --
D0 -- Version Major
D1 -- Verison Minor

CKS Check Sum
"""


data = [0x55,0x12,0x01,0x00,0x00,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x00,0x00]
camabio.setChksum(data)

print('abriendo puerto seriel')
ser = serial.Serial("/dev/ttyS1",115200,timeout=5)

print('escribiendo bytes en el puerto serie')
camabio.printArray(data)
bytesToWrite = array.array('B', data).tostring()
ser.write(bytesToWrite);
ser.flush()

print('tratando de leer bytes desde el puerto serie: ')
data2 = ser.read(len(data))
if data2 == None:
    print('No se leyo ningun byte')
else:
    camabio.printHexString(data2)
