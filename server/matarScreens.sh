ps -ef | grep SCREEN | grep -v crossbar | awk '{print()}' | xargs -I{} kill -9 {}
