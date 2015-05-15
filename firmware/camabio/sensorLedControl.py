import array, serial, camabio, sys, codecs, time

if len(sys.argv) <= 1:
    sys.exit(1)


on = int(sys.argv[1])
data = [0x55,0xaa,0x24,0x01,0x02,0x0,on,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x00,0x00]
camabio.setChksum(data)

print('abriendo puerto seriel')
ser = serial.Serial(port="/dev/ttyUSB0",baudrate=9600,timeout=5,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
ser.flush()
print(bytes(data))
ser.write(bytes(data));
time.sleep(1)
data2 = ser.read(ser.inWaiting())
if data2 == None:
    print('No se leyo ningun byte')
else:
    print(data2)
ser.close()
