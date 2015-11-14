# -*- coding: utf-8 -*-
import calendar, datetime, logging, uuid
from enum import Enum

from model.systems.assistance.justifications.exceptions import *


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

    ''' retorna True si la justificacion justifica la falla en la entrada, por defecto, todos retornan False '''
    def _isJustifiedTimeStart(self,sched,whs,justification,tolerancia, date = None):
        return False

    ''' retorna True si la justificacion justifica la falla en la salida, por defecto, todos retornan False '''
    def _isJustifiedTimeEnd(self,sched,whs, justification, tolerancia, date = None):
        return False

    ''' retorna True si justifica la falla por un periodo de tiempo, por defecto, todos retornan False '''
    def _isJustifiedTime(self,justification,start,end):
        return False

    ''' retorna True si la justificacion justifica la falla para todo el dia, por defecto, todos retornan False '''
    def _isJustifiedDay(self,date):
        return False

    """
        retorna la cantidad de justificaciones que se tienen disponibles dentro de un período de tiempo.
        si period = None entonces tiene en cuenta todos los períodos y toma el mínimo.
        period = 'MONTH|YEAR|WEEK'
    """
    def available(self,utils,con,userId,date,period):
        raise Exception('abstract')

    """ inicializa un pedido en estado pendiente de una justificación en las fechas indicadas """
    def requestJustification(self,utils,con,userId,begin,end,status):
        raise Exception('abstract')


    """ actualiza el estado del pedido de la justificacion al estado status """
    def updateJustificationRequestStatus(self,utils,con,userId,reqId,status):
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
