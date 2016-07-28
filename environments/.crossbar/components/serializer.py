"""
    Código que cambia las funciones _dumps y _loads usadas en el serializer de json de autobahn.
    así se puede usar otro encoder
    La creación del componente es solamente para lograr el crossbar importe y ejecute este código.
    el componente en si no hace nada.
"""

from autobahn.twisted.wamp import ApplicationSession
from twisted.internet.defer import inlineCallbacks
from twisted.python import log

from model.serializer import ditesiSerializer

ditesiSerializer.register()

class RegisterSerializers(ApplicationSession):
    pass
