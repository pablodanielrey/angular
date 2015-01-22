
from datetime import time

class TimeZone:

    def __init__(self):
        self.start = time(0)
        self.startTolerance = timedelta(minutes=15)
        self.end = time(24)
        self.endTolerance = timedelta(minutes=15)
        self.personId = ''

    def checkStart(self,period):
        pass

    def checkEnd(self,period):
        pass
