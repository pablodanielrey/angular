# -*- coding: utf-8 -*-
import json
import datetime
import itertools

from threading import Timer, Lock


""" combiner([ABC],[DEF]) -->  AD BE CF """
def combiner(list1,list2):
    return itertools.zip_longest(list1,list2,fillvalue=None)


""" grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx """
def grouper(n, iterable, fillvalue=None):
    return itertools.zip_longest(*[iter(iterable)]*n, fillvalue=fillvalue)



class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)



"""
    ejecución periódica de tareas.
    códgio básico sacado de stackoverflow. me parece mejor usar Celery pero por ahora no tengo
    tiempo, asi que lo voy a realizar con esto.
    referencias : http://stackoverflow.com/questions/2398661/schedule-a-repeating-event-in-python-3
"""

class Periodic(object):
    """
    A periodic task running in threading.Timers
    """

    def __init__(self, interval, function, *args, **kwargs):
        self._lock = Lock()
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self._stopped = True
        if kwargs.pop('autostart', True):
            self.start()

    def start(self, from_run=False):
        self._lock.acquire()
        if from_run or self._stopped:
            self._stopped = False
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self._lock.release()

    def _run(self):
        self.start(from_run=True)
        self.function(*self.args, **self.kwargs)

    def stop(self):
        self._lock.acquire()
        self._stopped = True
        self._timer.cancel()
        self._lock.release()
        
        
        
class Tools(object):

   
    @staticmethod
    def concat(value, connectNoEmpty, connectEmpty = None, connectCond = None):
      if not value:
        return ''
	
      if not connectEmpty:
        connect = connectNoEmpty
      else:
        connect = connectEmpty if not connectCond else connectNoEmpty
		
      return connect + " " + value
        
