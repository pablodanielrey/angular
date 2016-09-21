from autobahn.wamp.interfaces import IObjectSerializer, ISerializer
from autobahn.wamp.serializer import Serializer
import six
import dateutil
import dateutil.tz
import datetime
import importlib
import re
import json

__all__ = [
            'JSONSerializable'
          ]

class JSONSerializable:

    def __json_serialize__(self):
        d = self.__dict__
        d['__json_module__'] = self.__class__.__module__
        d['__json_class__'] = self.__class__.__name__
        return d


class JsonEncoder(json.JSONEncoder):
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
    try:
        a = json.dumps(obj, separators=(',', ':'), ensure_ascii=False, cls=JsonEncoder)
        return a
    except Exception as e:
        print(e)
        raise e

def _my_loads(data):
    try:
        return json.loads(data, object_hook=JsonEncoder._object_loads)
    except Exception as e:
        print(e)
        raise e

def register():
    """ reemplazo las funciones usadas por el JsonObjectSerializer del autobahn para serializar usando json """
    from autobahn.wamp import serializer
    serializer._dumps = _my_dumps
    serializer._loads = _my_loads
