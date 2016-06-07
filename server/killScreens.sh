ps -ef | grep SCREEN | grep -v crossbar | awk '{print($2)}' | xargs -I {} kill {}
