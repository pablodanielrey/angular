#!/bin/bash

##############
#  ejecuta el servidor de python
###########

chmod a+wr $(tty)
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR/../environment/node1
echo "iniciando crossbar"
screen -S crossbar -d -m ../pypy-2.6-linux_x86_64-portable/bin/crossbar start
sleep 60s
cd $DIR
echo "iniciando sistema"
screen -S a5 -d -m python3 mainOffice.py
screen -S a4 -d -m python3 mainDigesto.py
screen -S a3 -d -m python3 mainFirmware.py
screen -S a2 -d -m python3 mainLogin.py
screen -S a1 -d -m python3 Main.py
#su cubie -c "screen -S a2 -d -m python3 mainFirmware.py"
#su cubie -c "screen -S a3 -d -m python3 mainSync.py"
#su cubie -c "screen -S a1 -d -m python3 main.py"
