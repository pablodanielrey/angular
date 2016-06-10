#!/bin/bash

##############
#  ejecuta el servidor de python
###########

echo "iniciando sistema"
screen -S user -d -m python3 mainUsers.py
screen -S issue -d -m python3 mainIssue.py
screen -S office -d -m python3 mainOffice.py
screen -S login -d -m python3 mainLogin.py

