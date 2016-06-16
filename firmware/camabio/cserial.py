# -*- coding: utf-8 -*-
import serial, codecs, time

port = None

def writeAndRead(port,data):
  ser = serial.Serial(port=port,baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
  ser.flush()
  print(codecs.encode(bytes(data),'hex'))
  ser.write(bytes(data))
  time.sleep(0.5)
  response = ser.read(24)
  print(codecs.encode(response,'hex'))
  ser.close()
  return response


def open(p):
    global port
    port = serial.Serial(port=p,baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
    port.flush()

def close():
    global port
    if port:
        port.close()
        port = None


def write(data):
    global port
    port.write(bytes(data))

def readS(size):
    global port
    return port.read(size)

def read():
    global port
    return port.read(port.inWaiting())
