
class WpStatistics:

    def __init__(self, userId):
        self.userId = userId
        self.secondsToWork = 0              # total que deberia trabajar
        self.secondsWorked = 0              # total trabajado
        self.secondsLate = 0                # total de llegadas tarde
        self.countLate = 0                  # cantidad de llegadas tarde
        self.secondsEarly = 0               # total de salidas tempranas
        self.countEarly = 0                 # cantidad de salidas tempranas

    def updateStatistic(self, start, end, hourStart, hourEnd):

        if end is not None and start is not None:
            self.secondsToWork = self.secondsToWork + (end - start).total_seconds()

        if hourStart is not None and hourEnd is not None:
            self.secondsWorked = self.secondsWorked + (hourEnd - hourStart).total_seconds()

        if hourStart is not None and start is not None and hourStart > start:
            self.secondsLate = self.secondsLate + (hourStart - start).total_seconds()
            self.countLate = self.countLate + 1

        if hourEnd is not None and end is not None and end > hourEnd:
            self.secondsEarly = self.secondsEarly + (end - hourEnd).total_seconds()
            self.countEarly = self.countEarly + 1    
