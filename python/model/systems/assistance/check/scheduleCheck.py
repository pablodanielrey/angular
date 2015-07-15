import logging,inject
import datetime
from model.systems.assistance.date import Date
from model.systems.assistance.schedule import Schedule
from model.systems.assistance.logs import Logs
from model.systems.assistance.check.check import Check
from model.systems.assistance.justifications.justifications import Justifications

from model.systems.assistance.justifications.A102Justification import A102Justification
from model.systems.assistance.justifications.BCJustification import BCJustification
from model.systems.assistance.justifications.BSJustification import BSJustification
from model.systems.assistance.justifications.ETJustification import ETJustification

'''
Tipo de chequeo SCHEDULE
'''
class ScheduleCheck(Check):

    date = inject.attr(Date)
    schedule = inject.attr(Schedule)
    logs = inject.attr(Logs)
    justificationsTime = A102Justification(), BCJustification(), BSJustification(), ETJustification()
    justificationsReq = inject.attr(Justifications)
    justificationIds = [
        'e0dfcef6-98bb-4624-ae6c-960657a9a741',#Ausente con aviso
        '48773fd7-8502-4079-8ad5-963618abe725',#Compensatorio
        'fa64fdbd-31b0-42ab-af83-818b3cbecf46',#Boleta de Salida
        '4d7bf1d4-9e17-4b95-94ba-4ca81117a4fb',#Art 102
        'b70013e3-389a-46d4-8b98-8e4ab75335d0',#Pre-Exámen
        '76bc064a-e8bf-4aa3-9f51-a3c4483a729a',#Licencia Anual Ordinaria
        '50998530-10dd-4d68-8b4a-a4b7a87f3972',#Resolución 638
        'f9baed8a-a803-4d7f-943e-35c436d5db46',#Licencia Médica Corta Duración
        'a93d3af3-4079-4e93-a891-91d5d3145155',#Licencia Médica Largo Tratamiento
        'b80c8c0e-5311-4ad1-94a7-8d294888d770',#Licencia Médica Atención Familiar
        '478a2e35-51b8-427a-986e-591a9ee449d8',#Justificado por Médico
        'b309ea53-217d-4d63-add5-80c47eb76820',#Cumpleaños
        '0cd276aa-6d6b-4752-abe5-9258dbfd6f09',#Duelo
        'e8019f0e-5a70-4ef3-922c-7c70c2ce0f8b',#Donación de Sangre
        'cb2b4583-2f44-4db0-808c-4e36ee059efe',#Boleta en Comisión
        '70e0951f-d378-44fb-9c43-f402cbfc63c8',#Art
        '3d486aa0-745a-4914-a46d-bc559853d367',#Incumbencias Climáticas
        '5c548eab-b8fc-40be-bb85-ef53d594dca9',#Día del Bibliotecario
        '508a9b3a-e326-4b77-a103-3399cb65f82a',#Asistencia a Congresos/Capacitación - art 97 dec 366
        '7e180d9d-0ef1-48a7-9f3f-26a0170cc2f7',#Entrada Tarde Justificada
        'c32eb2eb-882b-4905-8e8f-c03405cee727',#Justificado Por Autoridad
        'aa41a39e-c20e-4cc4-942c-febe95569499',#Licencia Médica Pre-Natal. Art 106P
        'e249bfce-5af3-4d99-8509-9adc2330700b',#Nacimiento
        '5289eac5-9221-4a09-932c-9f1e3d099a47',#Concurso
        '68bf4c98-984d-4b71-98b0-4165c69d62ce',#Licencia Médica Por Maternidad
        '30a249d5-f90c-4666-aec6-34c53b62a447',#Matrimonio
        '1c14a13c-2358-424f-89d3-d639a9404579',#Licencia Sin Goce De Sueldo
        '3fb52f24-3eff-4ca2-8133-c7a3abfc7262',#Justificado Horario
        'bfaebb07-8d08-4551-b264-85eb4cab6ef1',#Suspensión
        '7747e3ff-bbe2-4f2e-88f7-9cc624a242a9',#Viaje
        'f7464e86-8b9e-4415-b370-b44b624951ca',#Receso de Invierno
        '5ec903fb-ddaf-4b6c-a2e8-929c77d8256f',#Feriado
        '874099dc-42a2-4941-a2e1-17398ba046fc',#Paro
        '6300ad65-537e-41f2-b932-e5a758d22381'#Receso de Verano
    ]

    type = 'SCHEDULE'
    tolerancia = datetime.timedelta(minutes=16)


    def create(self,id,userId,start,cur):
        check = {
            'userId': userId,
            'start':start,
            'end':None,
            'type':self.type
        }
        return check

    def isTypeCheck(self,type):
        return self.type == type

    '''
        return
        fail: {
            'userId':'',
            'date':date,
            'description':'Sin marcación',
            'justifications':[]
        }
        actualDate es aware.
    '''
    def getFails(self, utils, userId, actualDate, con):

        logging.debug('schedule {} {}'.format(userId,actualDate))

        fails = utils.checkSchedule(con,userId,actualDate)
        return fails



    '''
        Obtengo las justificaciones generales para un dia
    '''
    def _findGeneralJustificationsForDate(self,justifications,date):
        justs = []
        for j in justifications:
            logging.debug('chequeando fecha : {} == {}'.format(j['begin'].date(),date.date()))
            if j['begin'].date() == date.date():
                justs.append(j)
        return justs

    '''
        Obtengo las justificaciones
    '''
    def _getJustifications(self,con, userId, start, end):
        justifications = self.justificationsReq.getJustificationRequestsByDate(con,status=['APPROVED'],users=[userId],start=start,end=end)
        just = []

        gjustifications = self.justificationsReq.getGeneralJustificationRequests(con)
        gjusts = self._findGeneralJustificationsForDate(gjustifications, start)
        if len(gjusts) > 0:
            for j in gjusts:
                j['user_id'] = userId
                justifications.append(j)

        for j in justifications:
            if j['justification_id'] in self.justificationIds:
                just.append(j)
        return just


    '''
        Verifica si  hay alguna justificacion que justifique todo el dia
    '''
    def _isJustifiedDay(self,con,date,userId, justifications):

        for j in justifications:
            if 'end' not in j or j['end'] is None:
                return True


    '''
        Verifica si  hay alguna justificacion que justifique un lapso del dia
    '''
    def _isJustifiedTime(self,con,userId,start,end, justifications,minutes):
        for j in justifications:
            for just in self.justificationsTime:
                if just.isJustification(j['justification_id']):
                    return just._isJustifiedTime(start,end,j,minutes,self.tolerancia)
        return False

    def _initDay(self,date):
        # paso el date a formato local y seteo a las 00:00:00:000
        date = self.date.localizeAwareToLocal(date)
        date = date.replace(hour=0,minute=0,second=0,microsecond=0)
        # lo vuelvo a pasar a utc
        return self.date.awareToUtc(date)


    '''
        chequea los schedules contra las workedhours calculadas
    '''
    def checkWorkedHours(self,con,userId,controls):
        fails = []
        minutes = 0

        for sched,wh in controls:

            if sched is None:
                ''' no tiene schedule a controlar '''
                continue

            date = sched['start']

            if (wh is None) or ('start' not in wh and 'end' not in wh):
                date = self._initDay(date)
                justifications = self._getJustifications(con,userId,date,date)

                if self._isJustifiedDay(con,date,userId,justifications):
                    continue

                ''' no tiene nada trabajado!!! '''
                fails.append(
                    {
                        'userId':userId,
                        'date':date,
                        'description':'Sin marcación',
                        'justifications':justifications
                    }
                )

                continue

            ''' obtengo el tiempo trabajado hasta el momento '''
            if 'start' in wh and wh['start'] is not None and 'end' in wh and wh['end'] is not None:
                diff = wh['end'] - wh['start']
                minutes = minutes + (diff.seconds / 60)

            ''' controlo la llegada '''
            if wh['start'] is None:
                # no hay justificacion que justifique este tipo de falla
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Sin entrada'
                    }
                )

            elif wh['start'] > sched['start'] + self.tolerancia:
                justifications = self._getJustifications(con,userId,sched['start'],wh['start'])
                if not self._isJustifiedTime(con,userId,sched['start'],wh['start'],justifications,minutes):
                    fails.append(
                        {
                            'userId':userId,
                            'date': date,
                            'description':'Llegada tardía',
                            'startSchedule':sched['start'],
                            'start':wh['start'],
                            'seconds':(wh['start'] - sched['start']).total_seconds(),
                            'whSeconds':wh['seconds'],
                            'justifications':justifications
                        }
                    )


            ''' controlo la salida '''
            if wh['end'] is None:
                # no hay justificacion que justifique este tipo de falla
                fails.append(
                    {
                        'userId':userId,
                        'date': date,
                        'description':'Sin salida'
                    }
                )

            elif wh['end'] < sched['end'] - self.tolerancia:
                # busco las justificaciones que tenga desde la hora las 00:00
                initDay = self._initDay(wh['start'])
                justifications = self._getJustifications(con,userId,initDay,sched['end'])
                if not self._isJustifiedTime(con,userId,wh['end'],sched['end'],justifications,minutes):
                    fails.append(
                        {
                            'userId':userId,
                            'date': date,
                            'description':'Salida temprana',
                            'endSchedule':sched['end'],
                            'end':wh['end'],
                            'seconds':(sched['end']-wh['end']).total_seconds(),
                            'whSeconds':wh['seconds'],
                            'justifications':justifications
                        }
                    )


        return fails
