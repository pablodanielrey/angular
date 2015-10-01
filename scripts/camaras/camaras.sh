#!/bin/bash
#$1 = ip de la camara
#$2 = script a correr
#$3 = numero de la camara
#!/bin/bash

pidsExec() {
	pids=''
        for line in `ps -ef|grep openRTSP | grep $1| awk '{print $2 ":" NF}'`;do
                pid=`echo $line | awk  -F ':' '{print $1}'`
		pids="$pids  $pid"
        done
        echo $pids
}

isUp() {
	ping -c 3 $1
	return $?
}


while [ 1 ];do
  # si me responde el ping
  if isUp $1; then
	echo "Is up"
	#si esta levantado el screen
	pids=$(pidsExec $1)
	if [ "$pids" != '' ]; then
		echo "esperando 10 segundos"
		sleep 10
	else
		echo "ejecutando screen"
		/usr/bin/screen -S dc$3 -d -m $2	
	fi
  #si no me response el ping
  else
	echo "Is down"
	pids=$(pidsExec $1)
	if [ "$pids" != '' ]; then
	  echo "ejecutando kill $pids"
	  kill -HUP $pids
	fi
	sleep 1
  fi
done
