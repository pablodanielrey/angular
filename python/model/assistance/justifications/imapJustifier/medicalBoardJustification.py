
import logging
import datetime

from model.users.users import UserDAO
from model.assistance.justifications.imapJustifier.justCreator import JustCreator
from model.assistance.justifications.medicalBoardJustification import MedicalBoardJustification

class MedicalBoardCreator(JustCreator):

    def checkType(ttype):
        return 'Junta médica' == ttype

    def create(con, dni, start, days):
        ####
        #### aca hay que ver si se saca del registry el dni de una persona responsable del sistema de asistencia para ponerlo como userId.
        #### por ahora uso el mismo que el ownerId.
        ####

        user = UserDAO.findByDni(con, dni)
        if user is None:
            logging.warn('No existe usuario {}'.format(dni))
            return False

        uid, v = user
        assert uid is not None

        just = MedicalBoardJustification.findByUserId(con, [uid], start, start + datetime.timedelta(days = days))
        if len(just) > 0:
            ''' ya esta justificado con una de corta duración para ese día aunque sea asi que las ignoro '''
            logging.warn('ya esta justificado {} para {}'.format(uid, start))
            return False

        s = MedicalBoardJustification(uid, uid, start, days)
        s.persist(con)

        return True
