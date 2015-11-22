#!/bin/bash
for  i in /mnt/camaras/*_camara4.m4v;
do
	mv $i /mnt/camaras/comprimir/
done
DATE=`date +%Y-%m-%d_%H-%M-%S`
#openRTSP -v -b 400000 rtsp://163.10.56.40:554/video.h264 | tee /gluster/camaras/$DATE"_camara4.m4v" | cat - > /mnt/camaras/$DATE"_camara4.m4v"
openRTSP -v -b 400000 rtsp://163.10.56.40:554/video.h264 | cat - > /mnt/camaras/$DATE"_camara4.m4v"
