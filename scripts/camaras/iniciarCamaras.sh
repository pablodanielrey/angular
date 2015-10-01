#!/bin/bash
/usr/bin/screen -S c1 -d -m /mnt/camaras/camaras.sh 163.10.17.6 /mnt/camaras/dumpCamara1.sh 1
/usr/bin/screen -S c2 -d -m /mnt/camaras/camaras.sh 163.10.17.7 /mnt/camaras/dumpCamara2.sh 2
/usr/bin/screen -S c3 -d -m /mnt/camaras/camaras.sh 163.10.17.5 /mnt/camaras/dumpCamara3.sh 3
#screen -S dc4 -d -m /mnt/camaras/dumpCamara4.sh

