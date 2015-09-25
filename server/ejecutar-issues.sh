#!/bin/bash

##############
#  ejecuta el servidor de python
###########

echo "iniciando sistema"
screen -S a10 -d -m python3 mainUsers.py
screen -S a8 -d -m python3 mainIssue.py
screen -S a6 -d -m python3 mainOffice.py
screen -S a2 -d -m python3 mainLogin.py
screen -S a1 -d -m python3 main.py
