# -*- coding: utf-8 -*-

import serial


ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
