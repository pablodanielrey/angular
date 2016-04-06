# -*- coding: utf-8 -*-
import uuid
import inject
import logging
import base64

from model.files.files import FileDAO
import model.users.users
from model.users.users import StudentDAO
from model.mail.mail import Mail
from email.mime.text import MIMEText

from model.laboralinsertion.mails import SentDAO, Sent
from model.laboralinsertion.inscription import InscriptionDAO
from model.laboralinsertion.company import CompanyDAO
from model.laboralinsertion.languages import LanguageDAO
from model.laboralinsertion.filters import Filter
from model.laboralinsertion.user import UserDAO, User

import csv


class LaboralInsertion:

    def findAllInscriptions(self, con, filters):
        """ obtiene los datos de las inscripciones de los alumnos """
        ids = InscriptionDAO.findAll(con)
        inscriptions = inscriptionDAO.findById(con, ids)

        ''' aplico los filtros '''
        if len(filters) > 0:
            inscriptions = Filter.apply(con, inscriptions, filters)

        return inscriptions

    def getFilters(self):
        return Filters.getFilters()

    def findAllInscriptionsByUser(self, con, userId):
        """ obtiene los datos de las inscripciones de los alumnos """
        ids = InscriptionDAO.findByUser(con, userId)
        inscriptions = []
        for id in ids:
            inscription = InscriptionDAO.findById(con, id)
            inscriptions.append(inscription)

        return inscriptions

    def deleteInscriptionById(self, con, iid):
        """ elimina la inscripción con el id determinado """
        InscriptionDAO.delete(con, iid)

    def persistInscription(self, con, inscription):
        """ genera una inscripcion nueva por usuario """
        InscriptionDAO.persist(con, inscription)

    def findByUser(self, con, userId):
        """
            obtiene todos los datos referidos a las propiedades de insercion laboral que no sean inscripciones a la bolsa
        """

        languagesIds = LanguageDAO.findByUser(con, userId)
        languages = []
        for id in languagesIds:
            languages.append(LanguageDAO.findById(con, id))

        users = model.laboralinsertion.user.UserDAO.findById(con, userId)
        if len(users) == 0:
            return None
        user = users[0]
        user.languages = languages
        return user

    def persist(self, con, user, languages):
        """ actualiza la información de insercion laboral del usuario """
        UserDAO.persist(con, user)
        LanguageDAO.deleteByUser(con, user.id)
        for l in languages:
            LanguageDAO.persist(con, l)


    def sendMailToCompany(self, con, inscriptions, emails):

        ets = mails.EmailToSend(inscriptions, emails)
        ets.sendMail(con)

        ''' genero los datos del envío en la base '''
        sent = Sent()
        sent.emails = emails
        sent.inscriptions = [i['id'] for i in inscriptions]
        SentDAO.persist(con, sent)
        con.commit()

        return datar


""""

    def persistLaboralInsertionCV(self,con,data):
        if (self.findLaboralInsertionCV(con,data['id'])) == None:
            params = (data['id'],psycopg2.Binary(data['cv']),data['name'])
            cur = con.cursor()
            cur.execute("insert into laboral_insertion.users_cv (id,cv,name) values (%s,%s,%s)",params)
        else:
            params = (psycopg2.Binary(data['cv']),data['name'],data['id'])
            cur = con.cursor()
            cur.execute('update laboral_insertion.users_cv set cv = %s, name = %s where id = %s',params)
"""
