
#!/bin/bash

# referencias
#http://crossbar.io/docs/Installation-on-Linux/

#
# IMPORTANTE!!!!
# hay que remover la libreria gmp que usa ghc - el compilador de haskell. si no tira error el pycrypto al instalarse
# sudo apt-get remove libgmp3-dev libgmp-dev
#

# seteo el entorno de ejecución para crossbar.io

sudo apt-get install build-essential libssl-dev libffi-dev libreadline-dev libbz2-dev libsqlite3-dev libncurses5-dev

# descargo una distribución portable de pypy
wget https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-2.6-linux_x86_64-portable.tar.bz2
tar xvjf pypy-2.6-linux_x86_64-portable.tar.bz2

# instalo el pip dentro de esa pypy
wget https://bootstrap.pypa.io/get-pip.py
./pypy-2.6-linux_x86_64-portable/bin/pypy get-pip.py

# instalo usando pip el crossbar.io
./pypy-2.6-linux_x86_64-portable/bin/pip install crossbar[tls,msgpack,manhole,system]

# puedo cheqeuar la version de crossbar instalada
./pypy-2.6-linux_x86_64-portable/bin/crossbar version

# para crear un crossbar sin app ni nada se puede hacer :
./pypy-2.6-linux_x86_64-portable/bin/crossbar init

# en node1 ya existe una instancia de crossbar pelada con realm configurada
