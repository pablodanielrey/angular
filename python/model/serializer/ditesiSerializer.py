
from autobahn.wamp.interfaces import IObjectSerializer, ISerializer
from autobahn.wamp.serializer import Serializer
import six
import dateutil
import dateutil.tz
import importlib
import re
import json

__all__ = [
            'DiTeSiSerializer',
            'DiTeSiObjectSerializer',
            'JSONSerializable'
          ]

class JSONSerializable:

    def __json_serialize__(self):
        d = self.__dict__
        d['__json_module__'] = self.__class__.__module__
        d['__json_class__'] = self.__class__.__name__
        return d


class DiTeSiJsonEncoder(json.JSONEncoder):
    """
        Encoder json para los objetos de tipo JSONSerializable
        integro los metodos aca que sirven para codificar un objeto a json y decodificar json a los objetos
     """

    tz = dateutil.tz.tzlocal()

    def default(self, obj):
        ser = getattr(obj, "__json_serialize__", None)
        if ser is not None:
            return ser()
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            objtz = datetime.datetime.combine(obj, datetime.time()).replace(tzinfo=self.tz)
            return objtz.isoformat()
        return json.JSONEncoder.default(self, obj)

    @staticmethod
    def _object_loads(d):
        for k, v in d.items():
            """
                se matchea en el formato isoformat
                2016-03-19T16:56:26.767543
            """
            if isinstance(v, str) and re.search("\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.\d+", v):
                try:
                    d[k] = dateutil.parser.parse(v)
                except:
                    pass

        instance = None
        if '__json_class__' in d.keys():
            module = importlib.import_module(d['__json_module__'])
            clazz = getattr(module, d['__json_class__'])
            instance = clazz()
            instance.__dict__ = d
        else:
            instance = d
        return instance

def _my_dumps(obj):
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=False, cls=DiTeSiJsonEncoder)

def _my_loads(data):
    return json.loads(data, object_hook=DiTeSiJsonEncoder._object_loads)



class DiTeSiObjectSerializer(object):
    """ una copia del JsonObjectSerializer pero que maneja el tema de las fechas a isodate """

    BINARY = False

    def __init__(self, batched=False):
        """
        Ctor.
        :param batched: Flag that controls whether serializer operates in batched mode.
        :type batched: bool
        """
        self._batched = batched

    def serialize(self, obj):
        """
        Implements :func:`autobahn.wamp.interfaces.IObjectSerializer.serialize`
        """
        s = json.dumps(obj, separators=(',', ':'), ensure_ascii=False, cls=DiTeSiJsonEncoder)
        if isinstance(s, six.text_type):
            s = s.encode('utf8')
        if self._batched:
            return s + b'\30'
        else:
            return s

    def unserialize(self, payload):
        """
        Implements :func:`autobahn.wamp.interfaces.IObjectSerializer.unserialize`
        """
        if self._batched:
            chunks = payload.split(b'\30')[:-1]
        else:
            chunks = [payload]
        if len(chunks) == 0:
            raise Exception("batch format error")
        return [json.loads(data.decode('utf8'), object_hook=DiTeSiJsonEncoder._object_loads) for data in chunks]


class DiTeSiSerializer(Serializer):

    SERIALIZER_ID = "json"
    MIME_TYPE = "application/json"
    RAWSOCKET_SERIALIZER_ID = 2

    def __init__(self, batched=False):
        super().__init__(DiTeSiObjectSerializer(batched=batched))
        if batched:
            self.SERIALIZER_ID = "json.batched"


def register():
    """ reemplazo las funciones usadas por el JsonObjectSerializer del autobahn para serializar usando json """
    from autobahn.wamp import serializer
    serializer._dumps = _my_dumps
    serializer._loads = _my_loads

    #IObjectSerializer.register(DiTeSiObjectSerializer)
    #ISerializer.register(DiTeSiSerializer)
