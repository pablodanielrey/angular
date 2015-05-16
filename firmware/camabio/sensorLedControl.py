import array, serial, camabio, sys, codecs, time

if len(sys.argv) <= 1:
    sys.exit(1)


on = int(sys.argv[1])
data = [0x55,0xaa,0x24,0x01,0x02,0x0,on,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x00,0x00]
camabio.setChksum(data)

print('abriendo puerto seriel')
ser = serial.Serial(port="/dev/ttyUSB0",baudrate=115200,timeout=5,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
print(codecs.encode(bytes(data),'hex'))
ser.write(bytes(data))
time.sleep(0.5)
print(codecs.encode(ser.read(24),'hex'))
ser.close()
