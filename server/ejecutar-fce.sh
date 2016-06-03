#!/bin/bash

##############
#  ejecuta el servidor de python
###########

echo "iniciando sistema"

screen -S a20 -d -m python3 mainFce.py
screen -S a16 -d -m python3 mainStudents.py
#screen -S a10 -d -m python3 mainUsers.py
#screen -S a5 -d -m python3 mainFiles.py
#screen -S a2 -d -m python3 mainLogin.py
