
import logging
import datetime

from model.users.users import UserDAO
from model.assistance.justifications.status import Status
from model.assistance.justifications.imapJustifier.justCreator import JustCreator
from model.assistance.justifications.shortDurationJustification import ShortDurationJustification

class ShortDurationCreator(JustCreator):

    def checkType(ttype):
        return 'Corta duración' == ttype

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

        just = ShortDurationJustification.findByUserId(con, [uid], start.date(), (start + datetime.timedelta(days = days)).date())
        if len(just) > 0:
            logging.warn('ya esta justificado {} para {}'.format(uid, start))
            for j in just:
                assert j.getStatus() is not None
                if (j.getStatus().status != Status.APPROVED):
                    j.changeStatus(con, Status.APPROVED, j.ownerId)
                    return True
            return False

        s = ShortDurationJustification(start, days, uid, uid)
        s.persist(con)

        return True
