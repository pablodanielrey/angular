# -*- coding: utf-8 -*-
import json
import re
import datetime
import jsonpickle

"""
class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)


class DateTimeDecoder(json.JSONDecoder):
    '''
        decodifica una fecha en formato iso
        2016-01-0717:54:20.928462
    '''

    def __init__(self):
        super().__init__()
        self.format = re.compile('^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d*$')

    def decode(self, str):
        if self.re.match(str):
            d = datetime.datetime.strptime(str, "%Y-%m-%dT%H:%M:%S")
            return d
        else:
            return super.decode(str)
"""


class Serializer:

    @staticmethod
    def dumps(obj):
        ''' return json.dumps(obj, cls=DateTimeEncoder) '''
        return jsonpickle.encode(obj)

    @staticmethod
    def loads(str):
        ''' json.loads(str, cls=DateTimeDecoder) '''
        return jsonpickle.decode(str)
