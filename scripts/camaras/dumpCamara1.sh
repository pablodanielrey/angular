#!/bin/bash
for  i in /mnt/camaras/*_camara1.m4v;
do
	mv $i /mnt/camaras/comprimir/
done
DATE=`date +%Y-%m-%d_%H-%M-%S`
#openRTSP -v -b 400000 rtsp://163.10.17.6:554/video.h264 | tee /gluster/camaras/$DATE"_camara1.m4v" | cat - > /mnt/camaras/$DATE"_camara1.m4v"
FILE=$DATE"_camara1.m4v"
ln -s /mnt/camaras/$FILE /mnt/camaras/vivo/camara1.mp4
openRTSP -v -f 15 -t -b 400000 rtsp://163.10.17.6:554/video.h264 | cat - > /mnt/camaras/$FILE

