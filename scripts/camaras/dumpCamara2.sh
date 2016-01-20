#!/bin/bash
for  i in /mnt/camaras/*_camara2.m4v;
do
	mv $i /mnt/camaras/comprimir/
done
DATE=`date +%Y-%m-%d_%H-%M-%S`
#openRTSP -v -f 25 -b 400000 rtsp://163.10.56.202:554/video.mp4 | tee /gluster/camaras/$DATE"_camara2.m4v" | cat - > /mnt/camaras/$DATE"_camara2.m4v"
openRTSP -v -f 15 -t -b 400000 rtsp://163.10.17.7:554/video.h264 | cat - > /mnt/camaras/$DATE"_camara2.m4v"

