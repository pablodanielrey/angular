import array
import serial
import camabio
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
DATA Success: Template Record Size + 2 -- Fail:Error code
CKS Check Sum
"""


data = [0x55,0xaa,0x0a,0x01,0x02,0x00,0x01,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x00]

print('abriendo puerto seriel')
ser = serial.Serial("/dev/ttyS1",9600,timeout=5)

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
