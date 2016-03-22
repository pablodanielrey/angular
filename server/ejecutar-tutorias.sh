#!/bin/bash
echo "iniciando sistema"
screen -S a1 -d -m python3 mainLogin.py
screen -S a2 -d -m python3 mainUsers.py
screen -S a3 -d -m python3 mainTutors.py

