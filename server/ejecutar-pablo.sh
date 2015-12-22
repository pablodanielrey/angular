#!/bin/bash

##############
#  ejecuta el servidor de python
###########

#chmod a+wr $(tty)
#DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
#cd $DIR/../environment/node1
#echo "iniciando crossbar"
#screen -S crossbar -d -m ../pypy-2.6-linux_x86_64-portable/bin/crossbar start
#sleep 60s
#cd $DIR
echo "iniciando sistema"
screen -S a14 -d -m python3 mainStudents.py
screen -S a13 -d -m python3 mainIngreso.py
#screen -S a12 -d -m python3 mainAssistance.py
#screen -S a11 -d -m python3 mainPositions.py
screen -S a10 -d -m python3 mainUsers.py
#screen -S a9 -d -m python3 mainUserMails.py
#screen -S a8 -d -m python3 mainIssue.py
#screen -S a6 -d -m python3 mainOffice.py
#screen -S a7 -d -m python3 mainDigesto.py
screen -S a5 -d -m python3 mainFiles.py
#screen -S a4 -d -m python3 mainLaboralInsertion.py
#screen -S a3 -d -m python3 mainFirmware.py
screen -S a2 -d -m python3 mainLogin.py
screen -S a1 -d -m python3 main.py
