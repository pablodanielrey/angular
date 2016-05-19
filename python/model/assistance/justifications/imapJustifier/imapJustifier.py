
import inject
import imaplib
import email
import logging
import re
import datetime
import dateutil
from dateutil import parser

from model.registry import Registry
from model.users.users import UserDAO
from model.assistance.justifications.shortDurationJustification import ShortDurationJustificationDAO, ShortDurationJustification
from model.assistance.justifications.medicalBoardJustification import MedicalBoardJustificationDAO, MedicalBoardJustification
from model.assistance.justifications.longDurationJustification import LongDurationJustificationDAO, LongDurationJustification
from model.assistance.justifications.familyAttentionJustification import FamilyAttentionJustificationDAO, FamilyAttentionJustification
from model.assistance.justifications.maternityJustification import MaternityJustificationDAO, MaternityJustification
from model.assistance.justifications.prenatalJustification import PrenatalJustificationDAO, PrenatalJustification

from model.assistance.justifications.imapJustifier.justCreator import JustCreator
from model.assistance.justifications.imapJustifier.shortDurationJustification import ShortDurationCreator
from model.assistance.justifications.imapJustifier.medicalBoardJustification import MedicalBoardCreator
from model.assistance.justifications.imapJustifier.longDurationJustification import LongDurationCreator
from model.assistance.justifications.imapJustifier.familyAttentionJustification import FamilyAttentionCreator
from model.assistance.justifications.imapJustifier.maternityJustification import MaternityCreator
from model.assistance.justifications.imapJustifier.prenatalJustification import PrenatalCreator



class ImapJustifier:

    @staticmethod
    def _processTypeOfLicence(con, text):
        """
            reconoce los siguientes patrones dentro del texto:

            (CUIL/CUIT 27299799099)
            <strong>Número</strong> <em class="large">61621</em>
            <strong>Fecha de solicitud</strong> <em>04/04/2016</em>
            <strong>Fecha</strong> <em>04/04/2016</em>
            <strong>Días de licencia</strong> <em>30</em>
            <strong>Inicio</strong> <em>02/04/2016</em>
            <strong>Imputable al artículo (como no docente)</strong> <em>Corta duración</em>

        """
        dni = None
        start = None
        days = 0
        ttype = None
        number = None

        m = re.search("Imputable al artículo.*<em>(?P<type>.*)</em>.*", text)
        if not m:
            return False
        ttype = m.group('type')

        m = re.search("CUIT\s(?P<cuit>\d*)", text)
        if not m:
            return False
        dni = m.group('cuit')[2:][:-1]

        m = re.search(".*Número.*<em.*>(?P<number>.*)</em>", text)
        if not m:
            return False
        number = m.group('number')

        m = re.search(".*Inicio.*<em>(?P<start>.*)</em>", text)
        if not m:
            return False

        start = parser.parse(m.group('start'),dayfirst=True)


        m = re.search(".*Días de licencia.*<em>(?P<days>\d*)</em>", text)
        if not m:
            return False
        days = int(m.group('days'))



        logging.info('dni {} licencia {} inicio {} cantidad de días {} número {}'.format(dni,ttype,start,days, number))

        for cls in JustCreator.__subclasses__():
            if cls.checkType(ttype):
                cls.create(con, dni, start, days)
                return True

        return False

    @staticmethod
    def loadJustifications(con):
        reg = inject.instance(Registry).getRegistry('imapJustifier')

        host = reg.get('host')
        user = reg.get('user')
        password = reg.get('password')
        folder = reg.get('folder')

        m = imaplib.IMAP4_SSL(host)
        try:
            logging.debug('login {} user {} pass {}'.format(host, user, password))
            rv, data = m.login(user, password)

            rv, mailboxes = m.list()
            if rv != 'OK':
                logging.warn(rv)
                return

            rv, data = m.select(folder)
            if rv != 'OK':
                logging.warn(rv)
                return

            rv, data = m.uid('search', None, 'ALL')
            if rv != 'OK':
                logging.warn(rv)
                return

            mails = data[0].split()
            for mail in mails:
                rv, data = m.uid('fetch', mail, 'fast')
                size = int(data[0].split()[-1][:-1])
                if size >= (1024 * 1024):
                    ''' mas que 1 mega lo ignoro, no lo proceso '''
                    continue

                rv, data = m.uid('fetch', mail, '(RFC822)')
                #logging.debug('procesando {}'.format(mail))
                (ui, body) = data[0]

                try:
                    text = body.decode('utf-8')
                    email_message = email.message_from_string(text)

                    for part in email_message.walk():
                        email_body = None
                        if part.get_content_type() == 'text/plain':
                            """ esta parte de codigo no esta probado ya que siempre envían con html """
                            email_body = part.get_payload(decode=True)

                        elif part.get_content_type() == 'text/html':
                            email_body = part.get_payload(decode=True).decode('utf-8')

                        if ImapJustifier._processTypeOfLicence(con, email_body):
                            logging.info('{} reconocido'.format(mail))

                except TypeError as te:
                    logging.exception(te)
                    pass
                except UnicodeDecodeError as ue:
                    pass
                except Exception as e:
                    logging.exception(e)
                    pass

        finally:
            m.close()
