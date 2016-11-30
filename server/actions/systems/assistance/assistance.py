# -*- coding: utf-8 -*-
import inject
import json
import re
import logging
import psycopg2
from dateutil.parser import parse
import pytz

from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import threads

import autobahn
import wamp

from model.assistance.logs import Log
from model.assistance.schedules import Schedule, ScheduleHistory
from model.assistance.utils import Utils
from model.assistance.assistance import AssistanceModel

from model.users.users import User

######## para activar exportación a LibreOffice #############
## from actions.systems.assistance.exportOO import ExportModel
####### para activar la exportación a google spreadsheets #############
from actions.systems.assistance.exportG import ExportModel

logging.getLogger().setLevel(logging.INFO)


class Assistance(wamp.SystemComponentSession):

    #exportModel = None
    exportModel = ExportModel
    assistanceModel = inject.attr(AssistanceModel)
    timezone = pytz.timezone('America/Argentina/Buenos_Aires')
    conn = wamp.getConnectionManager()

    def getRegisterOptions(self):
        return autobahn.wamp.RegisterOptions(details_arg='details')

    def _parseDate(self, strDate):
        ########################
        # ver como lo corregimos para que lo maneje wamp al tema del date.
        # tambien el docker parece no setear el timezone.
        date = parse(strDate)
        ldate = Utils._localizeUtc(date).astimezone(self.timezone)
        return ldate

    def _getLogs(self, initDate, endDate, initHours, endHours, details):
        iDate = self._parseDate(initDate)
        eDate = self._parseDate(endDate)
        iHours = self._parseDate(initHours)
        eHours = self._parseDate(endHours)
        con = self.conn.get()
        try:
            logs = Log.findByDateRange(con, iDate, eDate, iHours, eHours)
            return logs
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('assistance.get_logs')
    @inlineCallbacks
    def getLogs(self, initDate, endDate, initHours, endHours, details):
        r = yield threads.deferToThread(self._getLogs, initDate, endDate, initHours, endHours, details)
        returnValue(r)

    def _getStatistics(self, initDate, endDate, userIds, officeIds, initTime, endTime, details):
        iDate = None if initDate is None else self._parseDate(initDate)
        eDate = None if endDate is None else  self._parseDate(endDate)
        iTime = None if initTime is None else  self._parseDate(initTime)
        eTime = None if endTime is None else  self._parseDate(endTime)

        con = self.conn.get()
        try:
            logging.info('calculando estadisticas')
            statistics = self.assistanceModel.getStatisticsData(con, userIds, iDate, eDate, officeIds, iTime, eTime)
            logging.info(statistics)
            return statistics
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('assistance.get_statistics')
    @inlineCallbacks
    def getStatistics(self, initDate, endDate, userIds, officeIds, initTime, endTime, details):
        r = yield threads.deferToThread(self._getStatistics, initDate, endDate, userIds, officeIds, initTime, endTime, details)
        returnValue(r)

    def _setWorkedNote(self, userId, date, text, details):
        if (userId is None or date is None):
            return None

        con = self.conn.get()
        try:
            date = self._parseDate(date).date()
            wp = self.assistanceModel.setWorkedNote(con, userId, date, text)
            con.commit()
            return wp
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('assistance.set_worked_note')
    @inlineCallbacks
    def setWorkedNote(self, userId, date, text, details):
        r = yield threads.deferToThread(self._setWorkedNote,userId, date, text, details)
        returnValue(r)


    def _searchUsers(self, regex, details):
        con = self.conn.get()
        try:
            return User.search(con, regex)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('assistance.search_users')
    @inlineCallbacks
    def searchUsers(self, regex, details):
        r = yield threads.deferToThread(self._searchUsers, regex, details)
        returnValue(r)


    ############################# SCHEDULES #######################################

    def _findSchedulesWeek(self, userId, date, actualWeek, details):
        con = self.conn.get()
        try:
            logging.info("Buscando schedules para la semana")
            date = self._parseDate(date).date()
            scheds = Schedule.findByUserIdInWeek(con, userId, date, actualWeek)
            schedules = []
            for key in scheds:
                data = [{'date': key, 'schedule': sc} for sc in scheds[key]]
                schedules.extend([ data if len(data) > 0 else [{'date': key, 'schedule': None}]][0])
            return schedules
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('assistance.find_schedules_week')
    @inlineCallbacks
    def findSchedulesWeek(self, userId, date, actualWeek, details):
        r = yield threads.deferToThread(self._findSchedulesWeek, userId, date, actualWeek, details)
        returnValue(r)


    def _persistScheduleWeek(self, userId, date, schedules, details):
        con = self.conn.get()
        try:
            logging.info("guardando schedules vigente a partir del: {}".format(date))
            date = self._parseDate(date).date()
            id = AssistanceModel.persistScheduleWeek(con, userId, date, schedules)
            con.commit()
            return id
        finally:
            self.conn.put(con)

    '''
        guarda el horario semanal
        date: dia de vigencia
        schedules: [{date: date, weekday: 0-6, start: datetime, end: datetime}]
    '''
    @autobahn.wamp.register('assistance.persist_schedule_week')
    @inlineCallbacks
    def persistScheduleWeek(self, userId, date, schedules, details):
        id = yield threads.deferToThread(self._persistScheduleWeek, userId, date, schedules, details)
        self.publish('assistance.add_schedules_event', id)
        returnValue(id)



    def _persistScheduleHours(self, userId, date, schedules, details):
        con = self.conn.get()
        try:
            logging.info("guardando schedules vigente a partir del: {}".format(date))
            date = self._parseDate(date).date()
            id = AssistanceModel.persistScheduleHours(con, userId, date, schedules)
            con.commit()
            return id
        finally:
            self.conn.put(con)

    '''
        guarda el horario semanal en formato de horas
        date: dia de vigencia
        schedules: [{date: date, weekday: 0-6, start: datetime, hours: int}]
    '''
    @autobahn.wamp.register('assistance.persist_schedule_hours')
    @inlineCallbacks
    def persistScheduleHours(self, userId, date, schedules, details):
        id = yield threads.deferToThread(self._persistScheduleHours, userId, date, schedules, details)
        self.publish('assistance.add_schedules_event', id)
        returnValue(id)


    def _persistScheduleSpecial(self, userId, schedules, details):
        con = self.conn.get()
        try:
            id = AssistanceModel.persistScheduleSpecial(con, userId, schedules)
            con.commit()
            return id
        finally:
            self.conn.put(con)


    '''
        guarda un horario especial
        schedules: [{start: datetime, end: datetime}]
    '''
    @autobahn.wamp.register('assistance.persist_schedule_special')
    @inlineCallbacks
    def persistScheduleSpecial(self, userId, schedules, details):
        id = yield threads.deferToThread(self._persistScheduleSpecial, userId, schedules, details)
        self.publish('assistance.add_schedules_event', id)
        logging.info("horario especial guardado id: {}".format(id))
        returnValue(id)



    def _findAllSchedules(self, userId, details):
        con = self.conn.get()
        try:
            return ScheduleHistory.findByUserId(con, userId)
        finally:
            self.conn.put(con)

    '''
        retorna el history de horarios de un usuario
    '''
    @autobahn.wamp.register('assistance.find_all_schedules')
    @inlineCallbacks
    def findAllSchedules(self, userId, details):
        r = yield threads.deferToThread(self._findAllSchedules, userId, details)
        returnValue(r)


    def _findSchedHistoryByIds(self, ids, details):
        con = self.conn.get()
        try:
            return ScheduleHistory.findById(con, ids)
        finally:
            self.conn.put(con)

    '''
        busca el historial de horarios por id
    '''
    @autobahn.wamp.register('assistance.find_sched_history_by_ids')
    @inlineCallbacks
    def findSchedHistoryByIds(self, ids, details):
        r = yield threads.deferToThread(self._findSchedHistoryByIds, ids, details)
        returnValue(r)


    def _findScheduleByIds(self, ids, details):
        con = self.conn.get()
        try:
            return Schedule.findById(con, ids)
        finally:
            self.conn.put(con)

    '''
        busca los schedules por id
    '''
    @autobahn.wamp.register('assistance.find_schedule_by_ids')
    @inlineCallbacks
    def findScheduleByIds(self, ids, details):
        r = yield threads.deferToThread(self._findScheduleByIds, ids, details)
        returnValue(r)


    def _removeScheduleHistory(self, sched, details):
        con = self.conn.get()
        try:
            id = sched.delete(con)
            con.commit()
            return id
        finally:
            self.conn.put(con)

    '''
        elimina el schedule
    '''
    @autobahn.wamp.register('assistance.remove_schedule_history')
    @inlineCallbacks
    def removeScheduleHistory(self, sched, details):
        id = yield threads.deferToThread(self._removeScheduleHistory, sched, details)
        self.publish('assistance.remove_schedules_event', id)
        logging.info("historial eliminado: {}".format(id))
        returnValue(id)

    ############################# EXPORTACIONES #######################################

    @inlineCallbacks
    def _exportLogs(self, initDate, endDate, initHours, endHours, details):
        ###### HACK HORRIBLE!!! ver como se mejora de una forma eficiente #################
        ownerId = details.caller_authid
        ###################################################

        logs = self._getLogs(initDate, endDate, initHours, endHours, details)
        userIds = [l.userId for l in logs if l.userId is not None]
        usersData = yield self.call('users.find_by_id', userIds)
        r = self.exportModel.exportLogs(ownerId, logs, usersData)
        returnValue(r)

    @autobahn.wamp.register('assistance.export_logs')
    @inlineCallbacks
    def exportLogs(self, initDate, endDate, initHours, endHours, details):
        r = yield self._exportLogs( initDate, endDate, initHours, endHours, details)
        #r = yield threads.deferToThread(self._exportStatistics, initDate, endDate, userIds, officeIds, initTime, endTime, details)
        returnValue(r)

    @inlineCallbacks
    def _exportStatistics(self,  initDate, endDate, userIds, officeIds, initTime, endTime, details):
        ###### HACK HORRIBLE!!! ver como se mejora de una forma eficiente #################
        ownerId = details.caller_authid
        ###################################################

        stats = self._getStatistics( initDate, endDate, userIds, officeIds, initTime, endTime, details)
        userIds = [s.userId for s in stats if s.userId is not None]
        usersData = yield self.call('users.find_by_id', userIds)
        r = self.exportModel.exportStatistics(ownerId, stats, usersData)
        returnValue(r)

    @autobahn.wamp.register('assistance.export_statistics')
    @inlineCallbacks
    def exportStatistics(self, initDate, endDate, userIds, officeIds, initTime, endTime, details):
        r = yield self._exportStatistics(initDate, endDate, userIds, officeIds, initTime, endTime, details)
        #r = yield threads.deferToThread(self._exportStatistics, initDate, endDate, userIds, officeIds, initTime, endTime, details)
        returnValue(r)
