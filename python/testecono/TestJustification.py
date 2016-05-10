# -*- coding: utf-8 -*-
import logging
import unittest
import sys
sys.path.append('../../python')

from random import randint

import datetime
from dateutil.tz import tzlocal

from testecono.TestEcono import TestEcono
from testecono.TestUser import TestUser

from model.assistance.justifications import *

class TestJustification(TestEcono):
    justificationDAO = None
    justificationEntity = None

    def setUp(self):
        super().setUp()
        try:
            con = self.connection.get()
            try:
                self.justificationDAO._createSchema(con)
                self.user_id, self.user = TestUser.defineUserAndPersist(con)
                self.owner_id, self.owner = TestUser.defineUserAndPersist(con)
                con.commit()

            finally:
                self.connection.put(con)

        except Exception as e:
            logging.exception(e)




    def assertEqualStatus(self, status, status2):
        self.assertEqual(status.id, status2.id)
        self.assertEqual(status.justificationId, status2.justificationId)
        self.assertEqual(status.status, status2.status)
        self.assertEqual(status.userId, status2.userId)
        self.assertEqual(status.date, status2.date)
        self.assertEqual(status.created, status2.created)


    def assertEqualJustification(self, justification, justification2):
        self.assertEqual(justification.id, justification2.id)
        self.assertEqual(justification.userId, justification2.userId)
        self.assertEqual(justification.ownerId, justification2.ownerId)
        self.assertEqualStatus(justification.status, justification2.status)


    def assertEqualJustificationFindById(self, con, justification, justificationId):
        justs = justification.findById(con, [justificationId])
        self.assertIsNotNone(justs)
        self.assertEqual(len(justs), 1)
        self.assertEqualJustification(justification, justs[0])



    def test_persist(self):
        con = self.connection.get()
        try:
            ##### insertar #####
            j = self.newInstance()
            j.persist(con)
            con.commit()
            self.assertEqualJustificationFindById(con, j, j.id)

            ##### cambiar estado #####
            state = j.getStatus()
            state.changeStatus(con, j, 2, self.owner_id)
            con.commit()
            self.assertEqualJustificationFindById(con, j, j.id)

        finally:
            self.connection.put(con)


    def test_find_by_id(self):
        con = self.connection.get()
        try:
            j = self.newInstance()
            j.persist(con)
            con.commit()

            justs = j.findById(con,[j.id])
            self.assertIsNotNone(justs)
            self.assertEqual(len(justs), 1)
            self.assertEqualJustification(j, justs[0])

            justs = j.findById(con, ["not_exists"])
            self.assertEqual(justs, [])

        finally:
            self.connection.put(con)






class TestJustificationSingle(TestJustification):
    def assertEqualJustification(self, justification, justification2):
        super().assertEqualJustification(justification, justification2)
        #self.assertEqual(justification.date, justification2.date) #TODO no funciona hay que modificar el codigo de justification

    def test_find_by_user_id(self):
        con = self.connection.get()
        try:
            j = self.newInstance()
            j.persist(con)
            con.commit()

            start = datetime.datetime.combine(j.date, datetime.time.min) - datetime.timedelta(days=1)
            end = datetime.datetime.combine(j.date, datetime.time.min) + datetime.timedelta(days=1)
            usersId = [j.userId]

            justs = j.findByUserId(con, usersId, start, end)

            ids = []
            for just in justs:
                ids.append(just.id)

            self.assertIn(j.id, ids)

            for just in justs:
                if just.id == j.id:
                    self.assertEqualJustification(just, j)

        finally:
            self.connection.put(con)

class TestJustificationRanged(TestJustification):
    def assertEqualJustification(self, justification, justification2):
        super().assertEqualJustification(justification, justification2)
        self.assertEqual(justification.start, justification2.start)
        self.assertEqual(justification.end, justification2.end)

    def test_find_by_user_id(self):
        con = self.connection.get()
        try:
            j = self.newInstance()
            j.persist(con)
            con.commit()

            start = datetime.datetime.combine(j.start, datetime.time.min) - datetime.timedelta(days=1)
            end = datetime.datetime.combine(j.end, datetime.time.min) + datetime.timedelta(days=1)
            usersId = [j.userId]

            justs = j.findByUserId(con, usersId, start, end)

            ids = []
            for just in justs:
                ids.append(just.id)

            self.assertIn(j.id, ids)

            for just in justs:
                if just.id == j.id:
                    self.assertEqualJustification(just, j)

        finally:
            self.connection.put(con)


class TestJustificationRangedTime(TestJustification):
    def assertEqualJustification(self, justification, justification2):
        super().assertEqualJustification(justification, justification2)
        self.assertEqual(justification.start, justification2.start)
        self.assertEqual(justification.end, justification2.end)

    def test_find_by_user_id(self):
        con = self.connection.get()
        try:
            j = self.newInstance()
            j.persist(con)
            con.commit()

            start = datetime.datetime.combine(j.start, datetime.time.min) - datetime.timedelta(days=1)
            end = datetime.datetime.combine(j.end, datetime.time.min) + datetime.timedelta(days=1)
            usersId = [j.userId]

            justs = j.findByUserId(con, usersId, start, end)
            ids = []
            for just in justs:
                ids.append(just.id)

            self.assertIn(j.id, ids)

            for just in justs:
                if just.id == j.id:
                    self.assertEqualJustification(just, j)

        finally:
            self.connection.put(con)

class TestJustificationArt102(TestJustificationSingle):
    justificationDAO = Art102JustificationDAO

    def newInstance(self):
        j = Art102Justification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j


class TestJustificationArt(TestJustificationRanged):
    justificationDAO = ARTJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = ARTJustification(self.user_id, self.owner_id, now, days)

        return j


class TestJustificationAuthority(TestJustificationSingle):
    justificationDAO = AuthorityJustificationDAO

    def newInstance(self):
        j = AuthorityJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j



class TestJustificationBirthday(TestJustificationSingle):
    justificationDAO = BirthdayJustificationDAO

    def newInstance(self):
        j = BirthdayJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j


class TestJustificationBloodDonation(TestJustificationSingle):
    justificationDAO = BloodDonationJustificationDAO

    def newInstance(self):
        j = BloodDonationJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j





class TestJustificationCompensatory(TestJustificationSingle):
    justificationDAO = CompensatoryJustificationDAO

    def newInstance(self):
        j = CompensatoryJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j



class TestJustificationEvaluation(TestJustificationSingle):
    justificationDAO = EvaluationJustificationDAO

    def newInstance(self):
        j = EvaluationJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j

class TestJustificationFamilyAttention(TestJustificationRanged):
    justificationDAO = FamilyAttentionJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = FamilyAttentionJustification(self.user_id, self.owner_id, now, days)

        return j


class TestJustificationHoliday(TestJustificationSingle):
    justificationDAO = HolidayJustificationDAO

    def newInstance(self):
        j = HolidayJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j


class TestJustificationInformedAbsence(TestJustificationSingle):
    justificationDAO = InformedAbsenceJustificationDAO

    def newInstance(self):
        j = InformedAbsenceJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j


class TestJustificationLateArrival(TestJustificationSingle):
    justificationDAO = LateArrivalJustificationDAO

    def newInstance(self):
        j = LateArrivalJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j


class TestJustificationLeaveWithoutSalary(TestJustificationRanged):
    justificationDAO = LeaveWithoutSalaryJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = LeaveWithoutSalaryJustification(self.user_id, self.owner_id, now, days)

        return j


class TestJustificationLibrarianDay(TestJustificationSingle):
    justificationDAO = LibrarianDayJustificationDAO

    def newInstance(self):
        j = LibrarianDayJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j


class TestJustificationLongDuration(TestJustificationRanged):
    justificationDAO = LongDurationJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = LongDurationJustification(self.user_id, self.owner_id, now, days)

        return j


class TestJustificationMarriage(TestJustificationRanged):
    justificationDAO = MarriageJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = MarriageJustification(self.user_id, self.owner_id, now, days)

        return j

class TestJustificationMaternity(TestJustificationRanged):
    justificationDAO = MaternityJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = MaternityJustification(self.user_id, self.owner_id, now, days)

        return j

class TestJustificationMedicalBoard(TestJustificationRanged):
    justificationDAO = MedicalBoardJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = MedicalBoardJustification(self.user_id, self.owner_id, now, days)

        return j


##### MEDICAL CERTIFICATE #####
class TestJustificationMedicalCertificate(TestJustificationRanged):
    justificationDAO = MedicalCertificateJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = MedicalCertificateJustification(self.user_id, self.owner_id, now, days)

        return j

##### MOURNING FIRST GRADE #####
class TestJustificationMourningFirstGrade(TestJustificationRanged):
    justificationDAO = MourningFirstGradeJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = MourningFirstGradeJustification(self.user_id, self.owner_id, now, days)

        return j


##### MOURNING SECOND GRADE #####
class TestJustificationMourningSecondGrade(TestJustificationRanged):
    justificationDAO = MourningSecondGradeJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = MourningSecondGradeJustification(self.user_id, self.owner_id, now, days)

        return j


##### MOURNING RELATIVE #####
class TestJustificationMourningRelative(TestJustificationRanged):
    justificationDAO = MourningRelativeJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = MourningRelativeJustification(self.user_id, self.owner_id, now, days)

        return j


##### OUT TICKET WITH RETURN  #####
class TestJustificationOutTicketWithReturn(TestJustificationRangedTime):
    justificationDAO = OutTicketWithReturnJustificationDAO

    def newInstance(self):
        start = datetime.datetime.now(dateutil.tz.tzlocal())
        end = datetime.datetime.now(dateutil.tz.tzlocal())
        j = OutTicketWithReturnJustification(start, end, self.user_id, self.owner_id)

        return j


##### OUT TICKET WITHOUT RETURN #####
class TestJustificationOutTicketWithoutReturn(TestJustificationRangedTime):
    justificationDAO = OutTicketWithoutReturnJustificationDAO

    def newInstance(self):
        start = datetime.datetime.now(dateutil.tz.tzlocal())
        end = datetime.datetime.now(dateutil.tz.tzlocal())
        j = OutTicketWithoutReturnJustification(start, end, self.user_id, self.owner_id)

        return j


##### PATERNITY #####
class TestJustificationPaternity(TestJustificationRanged):
    justificationDAO = PaternityJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = PaternityJustification(self.user_id, self.owner_id, now, days)

        return j


##### SCHOOL PREEXAM #####
class TestJustificationSchoolPreExam(TestJustificationRanged):
    justificationDAO = SchoolPreExamJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = SchoolPreExamJustification(self.user_id, self.owner_id, now, days)

        return j


##### UNIVERSITY PREEXAM #####
class TestJustificationUniversityPreExam(TestJustificationRanged):
    justificationDAO = UniversityPreExamJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = UniversityPreExamJustification(self.user_id, self.owner_id, now, days)

        return j


##### PRENATAL #####
class TestJustificationPrenatal(TestJustificationRanged):
    justificationDAO = PrenatalJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = PrenatalJustification(self.user_id, self.owner_id, now, days)

        return j


##### RESOLUTION 638 #####
class TestJustificationResolution638(TestJustificationRanged):
    justificationDAO = Resolution638JustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = Resolution638Justification(self.user_id, self.owner_id, now, days)

        return j


##### SCHEDULE #####
class TestJustificationSchedule(TestJustificationSingle):
    justificationDAO = ScheduleJustificationDAO

    def newInstance(self):
        j = ScheduleJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j


##### SHORT DURATION #####
class TestJustificationShortDuration(TestJustificationRanged):
    justificationDAO = ShortDurationJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = ShortDurationJustification(self.user_id, self.owner_id, now, days)

        return j


##### STRIKE #####
class TestJustificationStrike(TestJustificationSingle):
    justificationDAO = StrikeJustificationDAO

    def newInstance(self):
        j = StrikeJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j


##### SUMMER BREAKE #####
class TestJustificationSummerBreake(TestJustificationRanged):
    justificationDAO = SummerBreakJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = SummerBreakJustification(self.user_id, self.owner_id, now, days)

        return j



##### SUSPENSION #####
class TestJustificationSuspension(TestJustificationRanged):
    justificationDAO = SuspensionJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = SuspensionJustification(self.user_id, self.owner_id, now, days)

        return j


##### TASK WITH RETURN #####
class TestJustificationTaskWithReturn(TestJustificationRangedTime):
    justificationDAO = TaskWithReturnJustificationDAO

    def newInstance(self):
        start = datetime.datetime.now(dateutil.tz.tzlocal())
        end = datetime.datetime.now(dateutil.tz.tzlocal())
        j = TaskWithReturnJustification(start, end, self.user_id, self.owner_id)

        return j


##### TASK WITHOUT RETURN #####
class TestJustificationTaskWithoutReturn(TestJustificationRangedTime):
    justificationDAO = TaskWithoutReturnJustificationDAO

    def newInstance(self):
        start = datetime.datetime.now(dateutil.tz.tzlocal())
        end = datetime.datetime.now(dateutil.tz.tzlocal())
        j = TaskWithoutReturnJustification(start, end, self.user_id, self.owner_id)

        return j


##### TRAINING #####
class TestJustificationTraining(TestJustificationSingle):
    justificationDAO = TrainingJustificationDAO

    def newInstance(self):
        j = TrainingJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j


##### TRAVEL #####
class TestJustificationTravel(TestJustificationRanged):
    justificationDAO = TravelJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = TravelJustification(self.user_id, self.owner_id, now, days)

        return j


##### WEATHER #####
class TestJustificationWeather(TestJustificationSingle):
    justificationDAO = WeatherJustificationDAO

    def newInstance(self):
        j = WeatherJustification(datetime.datetime.now(), self.user_id, self.owner_id)

        return j


##### WINTER BREAK #####
class TestJustificationWinterBreak(TestJustificationRanged):
    justificationDAO = WinterBreakJustificationDAO

    def newInstance(self):
        now = datetime.datetime.now().date()
        days = randint(1,60)
        j = WinterBreakJustification(self.user_id, self.owner_id, now, days)

        return j
