# -*- coding: utf-8 -*-
import calendar, datetime
from enum import Enum


class Repetition(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4


class Justification:

    def __init__(self):
        self.calendar = calendar.Calendar()

    """ retorna True en el caso que el id pasado como parámetro sea el id de la justificacion específica """
    def isJustification(self,id):
        raise Exception('abstract')


    """ Retorna la cantidad disponible """
    def available(self,con):
        raise Exception('abstract')

    """ Retorna la cantidad máxima data la repetición """
    def availableRep(self,conf,rep):
        raise Exception('abstract')

    """
        retorna la semana del mes a la que pertenece la fecha
        primer día = 1 = lunes
        primer semana = 1
    """
    def _wheekOfMonth(self,date):
        weeksInMonth = self.calendar.monthdayscalendar(date.year,date.month)
        week = 1
        for daysInWeek from weeksInMonth:
            if date.day in daysInWeek:
                return week
            else:
                week = week + 1
        return None




""" ausente con aviso """
class AARestriction(Justification):

    id = 'e0dfcef6-98bb-4624-ae6c-960657a9a741'

    def isJustification(self,id):
        return self.id == id

    def available(self,assistance,con,userId,date):
        """
            no mas de 2 por semana, salvo que sea distinto mes.
            no mas de 2 por mes.
            no mas de 6 por año.
        """

        maxInWeek = 2
        maxInMonth = 2
        maxInYear = 6

        """ busco lo que se tomo """
        dayOfMonth = date.day
        weekOfMonth = self.weekOfMonth(date)

        aproved = assistance.getJustificationRequests(con,userId,self.id,'APROVED')
        sameMonth = 0
        sameYear = 0
        sameWeek = 0
        for a in aproved:
            if date.year == a['begin'].year:
                sameYear = sameYear + 1
                if date.month == a['begin'].month:
                    sameMonth = sameMonth + 1
                    if weekOfMonth == self.weekOfMonth(a['begin']):
                        sameWeek = sameWeek + 1


        if sameYear >= maxInYear:
            return 0

        if sameMonth >= maxInMonth:
            return 0

        if sameWeek >= maxInWeek:
            return 0


        aInYear = maxInYear - sameYear
        aInMonth = maxInMonth - sameMonth
        aInWeek = maxInWeek - sameWeek

        available = min(min(aInYear,aInMonth),aInWeek)
        return available





""" Boletas de salida """
class BSRestriction(JustificationRestriction):

    id = 'fa64fdbd-31b0-42ab-af83-818b3cbecf46'

    def isJustification(self,id):
        return self.id == id

    def available(self,assistance,con,userId,date):
        """
            no mas de 3 horas semanales
            no mas de 3 horas mensuales
        """

        maxInWeek = 2
        maxInMonth = 2

        stock = assistance.getJustificationStock(con,userId,self.id,date)
        if stock = None:
            return 0

        jstock = stock['quantity']
        if jstock <= 0:
            return 0


        """ busco lo que se tomo """
        dayOfMonth = date.day
        weekOfMonth = self.weekOfMonth(date)

        aproved = assistance.getJustificationRequests(con,userId,self.id,'APROVED')
        sameMonth = 0
        sameWeek = 0
        for a in aproved:
            if date.year == a['begin'].year:
                if date.month == a['begin'].month:
                    sameMonth = sameMonth + 1


        if sameMonth >= maxInMonth:
            return 0

        if sameWeek >= maxInWeek:
            return 0

        available = min(min(min(maxInYear - sameYear, jstock), maxInMonth - sameMonth), maxInWeek - sameWeek)
        return available




""" Compensatorio """
class CRestriction(JustificationRestriction):

    id = '48773fd7-8502-4079-8ad5-963618abe725'

    def isJustification(self,id):
        return self.id == id

    def available(self,assistance,con,userId,date):
        """
            mientras tengas en stock se pueden tomar.
        """
        stock = assistance.getJustificationStock(con,userId,self.id)
        if stock = None:
            return 0

        jstock = stock['quantity']
        if jstock <= 0:
            return 0

        return jstock
