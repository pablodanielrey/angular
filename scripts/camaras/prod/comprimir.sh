#!/bin/bash
for i in /mnt/camaras/comprimir/*.m4v;
do
	f=$(basename $i)
	/mnt/camaras/ffmpeg/ffmpeg -i $i -c:v libvpx -crf 10 -b:v 1M /gluster/camaras/comprimidos/$f.webm
	mv $i /mnt/camaras/comprimidos/
done
