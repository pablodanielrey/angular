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


screen -S mainUsers -d -m python3 mainUsers.py
screen -S mainSileg -d -m python3 mainSileg.py
