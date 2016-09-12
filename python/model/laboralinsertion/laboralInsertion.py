# -*- coding: utf-8 -*-
"""
    Implementa le modelo de insercion laboral.


    configuración para el registry.cfg

    [LaboralInsertion]
    ooHost = localhost
    ooPort = 2002
    sheetTemplate = ../python/model/laboralinsertion/template/template_send.ods
    mailTemplate = ../python/model/laboralinsertion/template/template_send.html

"""


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
from model.laboralinsertion.mails import EmailToSend

import csv


class LaboralInsertion:

    def findAllInscriptions(self, con, filters):
        """ obtiene los datos de las inscripciones de los alumnos """
        ids = InscriptionDAO.findAll(con)
        inscriptions = InscriptionDAO.findById(con, ids)

        """ elimino las inscripciones eliminadas """
        inscriptions2 = [ i for i in inscriptions if i.deleted == False ]

        ''' aplico los filtros '''
        if len(filters) > 0:
            inscriptions2 = Filter.apply(con, inscriptions2, filters)

        return inscriptions2

    def getFilters(self):
        return Filters.getFilters()

    def findAllInscriptionsByUser(self, con, userId):
        """ obtiene los datos de las inscripciones de los alumnos """
        ids = InscriptionDAO.findByUser(con, userId)
        inscriptions = InscriptionDAO.findById(con, ids)
        inscriptions2 = [ i for i in inscriptions if i.deleted == False ]
        return inscriptions2

    def deleteInscriptionById(self, con, iid):
        """ elimina la inscripción con el id determinado """
        InscriptionDAO.delete(con, iid)

    def persistInscription(self, con, inscription):
        """ genera una inscripcion nueva por usuario """
        InscriptionDAO.persist(con, inscription)

    def checkInscription(self, con, id):
        InscriptionDAO.checkInscription(con, id)

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
        logging.info(user.__dict__)
        UserDAO.persist(con, user)
        LanguageDAO.deleteByUser(con, user.id)
        for l in languages:
            LanguageDAO.persist(con, l)

    def sendMailToCompany(self, con, inscriptionIds, emails):

        ets = EmailToSend(inscriptionIds, emails)
        sentEmails = ets.sendMail(con)

        ''' genero los datos del envío en la base '''
        sent = Sent()
        sent.emails = emails
        sent.inscriptions = inscriptionIds
        SentDAO.persist(con, sent)
        con.commit()

        return sentEmails
