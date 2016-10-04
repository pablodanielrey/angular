#!/bin/bash
echo "iniciando sistema"
screen -S a14 -d -m python3 mainStudents.py
screen -S a10 -d -m python3 mainUsers.py
screen -S a5 -d -m python3 mainFiles.py
screen -S a4 -d -m python3 mainLaboralInsertion.py
screen -S a2 -d -m python3 mainLogin.py

