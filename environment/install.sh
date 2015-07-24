
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



# para instalar en cubieboard usando cubian tengo el siguiente history

sudo apt-get install python-pip
sudo apt-get install python2.7-dev
pip install --update six
sudo pip install --upgrade twisted
pip install --upgrade requests
sudo pip install crossbar[all]

########################################################
####### LO SIGUIENTE NO FUNCIONO!!!! ###################

#para hacer funcionar la serializacion de datetime
###
sudo apt-get install libsnappy-dev
sudo pip install autobahn[twisted,accelerate,compress,serialization]

apt-get install gcc-4.9 g++-4.9
#hay que cambiar el link simbolico del compilador de gcc
sudo rm /usr/bin/arm-linux-gnueabihf-gcc
sudo ln -s /usr/bin/gcc-4.9 /usr/bin/arm-linux-gnueabihf-gcc

sudo pip3 install autobahn[asyncio,accelerate,compress,serialization]
#############################################################################
#############################################################################

# el problema de la fecha se soluciona simplemente configurando un class encoder en json.
# se debe editar el archivo serializer.py de autobahn.
# ej:

nano /usr/local/lib/python3.4/dist-packages/autobahn/wamp/serializer.py

y dejar para que la parte de importación del json sea algo parecido a esto :



..... codigo de importación de ujson .....

except ImportError:
# fallback to stdlib implementation
##
  import json
  import datetime

  class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
      if isinstance(obj, datetime.datetime):
        return obj.isoformat()

      if isinstance(obj, datetime.date):
        return obj.isoformat()

      return json.JSONEncoder.default(self, obj)

  _json = json

  _loads = json.loads

  def _dumps(obj):
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=False, cls=DateTimeEncoder)

..... mas codigo de importacion de mpack ...
