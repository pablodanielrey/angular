
import json
import dateutil, dateutil.tz, dateutil.parser, datetime
from dateutil.tz import tzlocal
import importlib
import re


def serializer_loads(d):

    import inject
    inject.configure_once()

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



class JSONSerializable:

    def __json_serialize__(self):
        d = self.__dict__
        d['__json_module__'] = self.__class__.__module__
        d['__json_class__'] = self.__class__.__name__
        return d

class MySerializer(json.JSONEncoder):

    import inject
    inject.configure_once()
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
