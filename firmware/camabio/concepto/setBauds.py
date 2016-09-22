import array
import serial
import camabio
import sys
import time

"""
	 * 1 - 9600
	 * 2 - 19200
	 * 3 - 38400
	 * 4 - 57600
	 * 5 - 115200 (por defecto)
"""

if len(sys.argv) <= 1:
	sys.exit(1)

bauds = int(sys.argv[1])
data = [0x55,0xaa,0x14,0x01,0x02,0x0,bauds,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x00,0x00]
camabio.setChksum(data)

ser = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,timeout=5,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
ser.flush()
print('escribiendo bytes en el puerto serie')
ser.write(bytes(data));
time.sleep(1)
print(ser.read(ser.inWaiting()))
ser.close()
