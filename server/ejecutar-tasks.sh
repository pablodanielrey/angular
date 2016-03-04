#!/bin/bash

##############
#  ejecuta el servidor de python
###########

echo "iniciando sistema"
screen -S a4 -d -m python3 mainUsers.py
screen -S a3 -d -m python3 mainTask.py
screen -S a2 -d -m python3 mainOffice.py
screen -S a1 -d -m python3 mainLogin.py

