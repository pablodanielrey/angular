#!/bin/bash

##############
#  ejecuta el servidor de python
###########

echo "iniciando sistema"
screen -S a13 -d -m python3 mainCamaras.py
screen -S a10 -d -m python3 mainUsers.py
screen -S a9 -d -m python3 mainUserMails.py
screen -S a2 -d -m python3 mainLogin.py
screen -S a1 -d -m python3 mainOffices.py
