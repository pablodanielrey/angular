ps -ef | grep Main.py | grep -v grep | awk '{print($2)}' | xargs -I {} kill -9 {}

