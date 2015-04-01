# -*- coding: utf-8 -*-
import calendar, datetime, logging

from enum import Enum


class Repetition(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4


"""
    Clase base de todas las justificaciones
"""
class Justification:

    def __init__(self):
        self.calendar = calendar.Calendar()

    """ retorna True en el caso que el id pasado como parámetro sea el id de la justificacion específica """
    def isJustification(self,id):
        raise Exception('abstract')


    """ Retorna la cantidad disponible """
    def available(self,justifications,con,userId,date):
        raise Exception('abstract')

    """ Retorna la cantidad máxima data la repetición """
    def availableRep(self,rep,userId,date):
        raise Exception('abstract')

    """
        retorna la semana del mes a la que pertenece la fecha
        primer día = 1 = lunes
        primer semana = 1
    """
    def _weekOfMonth(self,date):
        if isinstance(date,datetime.datetime):
            date = date.date()

        weeksInMonth = self.calendar.monthdatescalendar(date.year,date.month)
        week = 1
        for daysInWeek in weeksInMonth:
            if date in daysInWeek:
                return week
            else:
                week = week + 1
        raise Exception('No se encotró la fecha en e calendario de este año')


    """ retorna si la semana a la que pertenece la fecha, esta completa en el mes de la fecha o tiene días dentro del proximo mes """
    def _weekChangesMonth(self,date):
        if isinstance(date,datetime.datetime):
            date = date.date()

        weeksInMonth = self.calendar.monthdatescalendar(date.year,date.month)
        for week in weeksInMonth:
            if date in week:
                for d in week:
                    if d.month != date.month:
                        return True
                return False
        raise Exception('No se encotró la fecha en el calendario de ese año')


    """ retorna las dates que ocurren el mismo mes que date """
    def _filterInSameMonth(self,date,dates):
        datesR = []
        for d in dates:
            if d.month == date.month:
                datesR.append(d)
        return datesR


    """ retorna las dates que estan dentro de la misma semana que date """
    def _filterInSameWeek(self,date,dates):
        if isinstance(date,datetime.datetime):
            date = date.date()

        weeksInMonth = self.calendar.monthdatescalendar(date.year,date.month)
        for week in weeksInMonth:
            if date in week:
                datesR = []
                for d in dates:
                    if d in week:
                        datesR.append(d)
                return datesR
        raise Exception('No se encontró la fecha dentro del calendario del año de esa fecha')





"""
    Compensatorio
    no existe limite salvo el stock que se tenga
"""
class CJustification(Justification):

    id = '48773fd7-8502-4079-8ad5-963618abe725'

    def isJustification(self,id):
        return self.id == id


    def available(self,justifications,con,userId,date):
        cur = con.cursor()
        cur.execute('select stock from assistance.justifications_stock where justification_id = %s and user_id = %s',(self.id,userId))
        if cur.rowcount <= 0:
            return 0

        return cur.fetchone()[0]


    def availableRep(self,rep,userId,date):
        return None





"""
    Licencia Anual Ordinaria
    no tiene límite, solo el stock actual.
"""
class LAOJustification(Justification):

    id = '76bc064a-e8bf-4aa3-9f51-a3c4483a729a'

    def isJustification(self,id):
        return self.id == id


    def available(self,justifications,con,userId,date):
        cur = con.cursor()
        cur.execute('select stock from assistance.justifications_stock where justification_id = %s and user_id = %s',(self.id,userId))
        if cur.rowcount <= 0:
            return 0

        return cur.fetchone()[0]


    def availableRep(self,rep,userId,date):
        return None





"""
    Ausente con aviso
    anuales 6
    mensuales 2
    semanales 2, salvo que dentro de la semana cambie de mes, en ese caso 4
"""
class AAJustification(Justification):

    id = 'e0dfcef6-98bb-4624-ae6c-960657a9a741'

    def isJustification(self,id):
        return self.id == id

    """
        Retorna las disponibles para tomarse en la fecha date
    """
    def available(self,justifications,con,userId,date):

        justStatus = justifications._getJustificationsInStatus(con,['PENDING','APROVED'])
        if len(justStatus) <= 0:
            return self.availableRep(Repetition.WEEKLY,userId,date)

        justIds = tuple(justStatus.keys())

        cur = con.cursor()
        req = (self.id, userId, justIds, date)
        cur.execute('select jbegin from assistance.justifications_requests where justification_id = %s and user_id = %s and id in %s and extract(year from jbegin) = extract(year from %s)',req)
        inYear = cur.rowcount
        if inYear <= 0:
            return self.availableRep(Repetition.WEEKLY,userId,date)
        else:
            availableInYear = self.availableRep(Repetition.YEARLY,userId,date)
            if availableInYear <= inYear:
                return 0

            datesC = cur.fetchall()
            dates = map(lambda x: x[0],datesC)

            sameMonth = self._filterInSameMonth(date,dates)
            availableInMonth = self.availableRep(Repetition.MONTHLY,userId,date)
            if availableInMonth <= len(sameMonth):
                return 0

            sameWeek = self._filterInSameWeek(date,dates)
            availableInWeek = self.availableRep(Repetition.WEEKLY,userId,date)
            if availableInWeek <= len(sameWeek):
                return 0

            available = min(min((availableInYear - inYear), availableInMonth - len(sameMonth)), availableInWeek - len(sameWeek))
            return available



    """ retorna las disponibles por restricciones en la fecha date """
    def availableRep(self,rep,userId,date):
        if rep is Repetition.WEEKLY:
            if self._weekChangesMonth(date):
                return 4
            else:
                return 2

        if rep is Repetition.MONTHLY:
            return 2

        if rep is Repetition.YEARLY:
            return 6

        return None





"""
    Boletas de salida - restricciones en horas.
    anuales 36 horas
    mensuales 3 horas
    semanales 3 horas
    diario 3 horas
"""
class BSJustification(Justification):

    id = 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'

    def isJustification(self,id):
        return self.id == id

    """
        Retorna los segundos disponibles para tomarse en la fecha date
    """
    def available(self,justifications,con,userId,date):

        justStatus = justifications._getJustificationsInStatus(con,['PENDING','APROVED'])
        if len(justStatus) <= 0:
            return self.availableRep(Repetition.MONTHLY,userId,date)

        justIds = tuple(justStatus.keys())

        cur = con.cursor()
        req = (self.id, userId, justIds, date, date)
        cur.execute('select jbegin,jend from assistance.justifications_requests where justification_id = %s and user_id = %s and id in %s and extract(year from jbegin) = extract(year from %s) and extract(month from jbegin) = extract(month from %s)',req)
        if cur.rowcount <= 0:
            return self.availableRep(Repetition.MONTHLY,userId,date)

        datesC = cur.fetchall()
        seconds = 0
        for d in datesC:
            seconds = seconds + (d[1]-d[0]).total_seconds()

        available = self.availableRep(Repetition.MONTHLY,userId,date) - seconds
        return available



    """ retorna las disponibles por restricciones en la fecha date """
    def availableRep(self,rep,userId,date):
        if rep is Repetition.YEARLY:
            return (13 - date.month) * datetime.timedelta(hours=3)

        return datetime.timedelta(hours=3).total_seconds()
