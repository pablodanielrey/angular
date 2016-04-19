import logging
import os
from os import listdir
from os.path import isfile, join

import unittest
import inject
inject.configure()

import sys
sys.path.append('../../../python')


from model.registry import Registry
from model.connection.connection import Connection


from model.files.files import FileDAO

from model.users.users import UserDAO
from model.users.users import UserPasswordDAO
from model.users.users import MailDAO
from model.users.users import StudentDAO


from model.assistance.logs import LogDAO
from model.assistance.schedules import ScheduleDAO
#from model.assistance.statics import StaticsDAO

from model.assistance.justifications.status import StatusDAO
from model.assistance.justifications.art102Justification import Art102JustificationDAO
from model.assistance.justifications.artJustification import ARTJustificationDAO
from model.assistance.justifications.authorityJustification import AuthorityJustificationDAO
from model.assistance.justifications.birthdayJustification import BirthdayJustificationDAO
from model.assistance.justifications.bloodDonationJustification import BloodDonationJustificationDAO
from model.assistance.justifications.compensatoryJustification import CompensatoryJustificationDAO
from model.assistance.justifications.evaluationJustification import EvaluationJustificationDAO
from model.assistance.justifications.familyAttentionJustification import FamilyAttentionJustificationDAO
from model.assistance.justifications.holidayJustification import HolidayJustificationDAO
from model.assistance.justifications.informedAbsenceJustification import InformedAbsenceJustificationDAO
from model.assistance.justifications.lateArrivalJustification import LateArrivalJustificationDAO
from model.assistance.justifications.leaveWithoutSalaryJustification import LeaveWithoutSalaryJustificationDAO
from model.assistance.justifications.librarianDayJustification import LibrarianDayJustificationDAO
from model.assistance.justifications.longDurationJustification import LongDurationJustificationDAO
from model.assistance.justifications.marriageJustification import MarriageJustificationAbstractDAO
from model.assistance.justifications.maternityJustification import MaternityJustificationDAO
from model.assistance.justifications.medicalBoardJustification import MedicalBoardJustificationDAO
from model.assistance.justifications.medicalCertificateJustification import MedicalCertificateJustificationDAO
from model.assistance.justifications.mourningJustification import MourningJustificationDAO
from model.assistance.justifications.outTicketJustification import OutTicketJustificationDAO
from model.assistance.justifications.paternityJustification import PaternityJustificationDAO
from model.assistance.justifications.preExamJustification import PreExamJustificationDAO
from model.assistance.justifications.prenatalJustification import PrenatalJustificationDAO
from model.assistance.justifications.resolution638Justification import Resolution638JustificationDAO
from model.assistance.justifications.scheduleJustification import ScheduleJustificationDAO
from model.assistance.justifications.shortDurationJustification import ShortDurationJustificationDAO
from model.assistance.justifications.strikeJustification import StrikeJustificationDAO
from model.assistance.justifications.summerBreakJustification import SummerBreakJustificationDAO
from model.assistance.justifications.suspensionJustification import SuspensionJustificationDAO
from model.assistance.justifications.taskJustification import TaskJustificationDAO
from model.assistance.justifications.trainingJustification import TrainingJustificationDAO
from model.assistance.justifications.travelJustification import TravelJustificationDAO
from model.assistance.justifications.weatherJustification import WeatherJustificationDAO
from model.assistance.justifications.winterBreakJustification import WinterBreakJustificationDAO


class TestConnection(unittest.TestCase):

  def test_drop_database(self):
    try:
      logging.debug('drop database')
      
      reg = inject.instance(Registry)
      
      registrySection = reg.getRegistry('dcsys2')

      conn = Connection(registrySection)
         
      con = conn.get()
      try:
          cur = con.cursor()
          
          try:
              sql = """
                  DROP SCHEMA IF EXISTS assistance CASCADE;
                  DROP SCHEMA IF EXISTS credentials CASCADE;
                  DROP SCHEMA IF EXISTS students CASCADE;
                  DROP SCHEMA IF EXISTS profile CASCADE;
                  DROP SCHEMA IF EXISTS files CASCADE;

                  """
              cur.execute(sql)
              con.commit()

          except Exception as e:
              con.rollback()  
              raise e
                   
          finally:
              cur.close()
      finally:
          conn.put(con)              
    except Exception as e:
      print(str(e))    

          
  def test_create_database(self):
    try:
      logging.debug('create database')
      reg = inject.instance(Registry)
      
      registrySection = reg.getRegistry('dcsys2')

      conn = Connection(registrySection)
      
      con = conn.get()
      
      FileDAO._createSchema(con)
      UserDAO._createSchema(con)
      UserPasswordDAO._createSchema(con)
      MailDAO._createSchema(con)
      StudentDAO._createSchema(con)

      LogDAO._createSchema(con)
      ScheduleDAO._createSchema(con)

      StatusDAO._createSchema(con)      

      Art102JustificationDAO._createSchema(con)      
      ARTJustificationDAO._createSchema(con)
      AuthorityJustificationDAO._createSchema(con)
      BirthdayJustificationDAO._createSchema(con)
      BloodDonationJustificationDAO._createSchema(con)
      CompensatoryJustificationDAO._createSchema(con)
      EvaluationJustificationDAO._createSchema(con)
      FamilyAttentionJustificationDAO._createSchema(con)
      HolidayJustificationDAO._createSchema(con)
      InformedAbsenceJustificationDAO._createSchema(con)
      LateArrivalJustificationDAO._createSchema(con)
      LeaveWithoutSalaryJustificationDAO._createSchema(con)
      LibrarianDayJustificationDAO._createSchema(con)
      LongDurationJustificationDAO._createSchema(con)
      MarriageJustificationAbstractDAO._createSchema(con)
      MaternityJustificationDAO._createSchema(con)
      MedicalBoardJustificationDAO._createSchema(con)
      MedicalCertificateJustificationDAO._createSchema(con)
      MourningJustificationDAO._createSchema(con)
      OutTicketJustificationDAO._createSchema(con)
      PaternityJustificationDAO._createSchema(con)
      PreExamJustificationDAO._createSchema(con)
      PrenatalJustificationDAO._createSchema(con)
      Resolution638JustificationDAO._createSchema(con)
      ScheduleJustificationDAO._createSchema(con)
      ShortDurationJustificationDAO._createSchema(con)      
      StrikeJustificationDAO._createSchema(con)      
      SummerBreakJustificationDAO._createSchema(con)
      SuspensionJustificationDAO._createSchema(con)
      TaskJustificationDAO._createSchema(con)
      TrainingJustificationDAO._createSchema(con)
      TravelJustificationDAO._createSchema(con)
      WeatherJustificationDAO._createSchema(con)
      WinterBreakJustificationDAO._createSchema(con)
      
      con.commit()

      #UserDAO.findByDni(con, "31073351")
           
      #uid, v = UserDAO.findByDni(con, "31073351")
      
      #print("uid"  + uid)
      #print("value"  + v)

      
      


      
    except Exception as e:
      print(str(e))


  

if __name__ == '__main__':
    unittest.main()
