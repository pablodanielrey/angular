import array
import serial
import camabio

data = [0x55,0xaa,0x30,0x01,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x30,0x01]
camabio.setChksum(data)

print('abriendo puerto seriel')
ser = serial.Serial(port="/dev/ttyUSB0",baudrate=9600,timeout=5,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

print('escribiendo bytes en el puerto serie')
camabio.printArray(data)
setBauds = array.array('B', data).tostring()
ser.write(setBauds);
ser.flush()

print('tratando de leer bytes desde el puerto serie: ')
data2 = ser.read(len(data))
if data2 == None:
    print('No se leyo ningun byte')
else:
    camabio.printHexString(data2)
