#!/bin/bash

##############
#  ejecuta el servidor de python
###########

echo "iniciando sistema"
screen -S a6 -d -m python3 mainOffice.py
screen -S a7 -d -m python3 mainDigesto.py
screen -S a5 -d -m python3 mainFiles.py
screen -S a4 -d -m python3 mainLaboralInsertion.py
screen -S a3 -d -m python3 mainFirmware.py
screen -S a2 -d -m python3 mainLogin.py
screen -S a1 -d -m python3 main.py
