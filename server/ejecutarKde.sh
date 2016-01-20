#!/bin/bash

##############
#  ejecuta el servidor de python
###########

chmod a+wr $(tty)
echo "iniciando sistema"
konsole -e python3 mainAssistance.py
konsole -e python3 mainPositions.py
konsole -e python3 mainUsers.py
konsole -e python3 mainUserMails.py
konsole -e python3 mainIssue.py
konsole -e python3 mainOffice.py
konsole -e python3 mainDigesto.py
konsole -e python3 mainFiles.py
konsole -e python3 mainLaboralInsertion.py
konsole -e python3 mainFirmware.py
konsole -e python3 mainLogin.py
konsole -e python3 main.py
