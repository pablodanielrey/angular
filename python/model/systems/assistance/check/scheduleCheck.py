import logging
import inject
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

from model.systems.assistance.justifications.AAJustification import AAJustification
from model.systems.assistance.justifications.ARTJustification import ARTJustification
from model.systems.assistance.justifications.AUTJustification import AUTJustification
from model.systems.assistance.justifications.BJustification import BJustification
from model.systems.assistance.justifications.BloodDonationJustification import BloodDonationJustification
from model.systems.assistance.justifications.CCJustification import CCJustification
from model.systems.assistance.justifications.CJustification import CJustification
from model.systems.assistance.justifications.CONJustification import CONJustification
from model.systems.assistance.justifications.CumpJustification import CumpJustification
from model.systems.assistance.justifications.HolidayJustification import HolidayJustification
from model.systems.assistance.justifications.ICJustification import ICJustification
from model.systems.assistance.justifications.INVJustification import INVJustification
from model.systems.assistance.justifications.JMJustification import JMJustification
from model.systems.assistance.justifications.LAOJustification import LAOJustification
from model.systems.assistance.justifications.LMAFJustification import LMAFJustification
from model.systems.assistance.justifications.LMCDJustification import LMCDJustification
from model.systems.assistance.justifications.LMLTJustification import LMLTJustification
from model.systems.assistance.justifications.MATJustification import MATJustification
from model.systems.assistance.justifications.MourningJustification import MourningJustification
from model.systems.assistance.justifications.NACJustification import NACJustification
from model.systems.assistance.justifications.ParoJustification import ParoJustification
from model.systems.assistance.justifications.PEJustification import PEJustification
from model.systems.assistance.justifications.PONJustification import PONJustification
from model.systems.assistance.justifications.PRNJustification import PRNJustification
from model.systems.assistance.justifications.R638Justification import R638Justification
from model.systems.assistance.justifications.SGSJustification import SGSJustification
from model.systems.assistance.justifications.SUSJustification import SUSJustification
from model.systems.assistance.justifications.VJEJustification import VJEJustification

'''
Tipo de chequeo SCHEDULE
'''
class ScheduleCheck(Check):

    date = inject.attr(Date)
    schedule = inject.attr(Schedule)
    logs = inject.attr(Logs)
    justificationsTime = [A102Justification(), BCJustification(), BSJustification(), ETJustification()]
    justificationsDay = [
        AAJustification(),
        ARTJustification(),
        AUTJustification(),
        BJustification(),
        BloodDonationJustification(),
        CCJustification(),
        CJustification(),
        CONJustification(),
        CumpJustification(),
        HolidayJustification(),
        ICJustification(),
        INVJustification(),
        JMJustification(),
        LAOJustification(),
        LMAFJustification(),
        LMCDJustification(),
        LMLTJustification(),
        MATJustification(),
        MourningJustification(),
        NACJustification(),
        ParoJustification(),
        PEJustification(),
        PONJustification(),
        PRNJustification(),
        R638Justification(),
        SGSJustification(),
        SUSJustification(),
        VJEJustification()
    ]
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
        Retorna las fallas
        @param utils Clase ScheduleCheck
        @param userId Identificacion de usuario
        @param actualDate Fecha para la cual se chequearan las fallas
        @param 
        @return
            fail: {
                'userId':'',
                'date':date,
                'description':'Sin marcación',
                'justifications':[]
            }
        actualDate es aware.
    
    def getFails(self, utils, userId, actualDate, con):
        fails = utils.checkSchedule(con,userId,actualDate)
        return fails
    '''


    '''
        Obtengo las justificaciones generales para un dia
    '''
    def _findGeneralJustificationsForDate(self,justifications,date):
        justs = []
        for j in justifications:

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
            for just in self.justificationsDay:
                if just.isJustification(j['justification_id']):
                    return just._isJustifiedDay(date)
        return False


    '''
        Verifica si  hay alguna justificacion que justifique la falla en la entrada
        @param justifications Lista de justificaciones
        @param sched Schedule correspondiente al dia de chequeo
        @param whs Horas trabajadas correspondientes al dia de chequeo
        @param fail Falla correspondiente al dia de chequeo
        @param isLastSchedule Flag para indicar que es el ultimo schedule que se esta chequeando de la lista de schedules
        @param date Dia de chequeo
    '''
    def _isJustifiedTimeStart(self,justifications,sched,whs,fail,isFirstSchedule, date):
        if not isFirstSchedule or fail['whAnt'] is not None:
            start = sched.getStart(date) if fail['whAnt'] is None else fail['whAnt']['end']
            end = fail['wh']['start']
            return self._isJustifiedTime(justifications,start,end)
        for j in justifications:
            for just in self.justificationsTime:
                if just.isJustification(j['justification_id']):
                    return just._isJustifiedTimeStart(sched,whs,j,self.tolerancia, date)


        return False




    '''
        Verifica si  hay alguna justificacion que justifique la falla en la salida
        @param justifications Lista de justificaciones
        @param sched Schedule correspondiente al dia de chequeo
        @param whs Horas trabajadas correspondientes al dia de chequeo
        @param fail Falla correspondiente al dia de chequeo
        @param isLastSchedule Flag para indicar que es el ultimo schedule que se esta chequeando de la lista de schedules
        @param date Dia de chequeo
    '''
    def _isJustifiedTimeEnd(self, justifications, sched, whs, fail, isLastSchedule, date):
        if isLastSchedule and fail['whNext'] is None:
            for j in justifications:
                for just in self.justificationsTime:
                    if just.isJustification(j['justification_id']):
                        return just._isJustifiedTimeEnd(sched,whs,j,self.tolerancia, date)
        else:
            start = fail["wh"]["end"]
            end = sched.getEnd(date) if fail['whNext'] is None else fail['whNext']['start']

            return self._isJustifiedTime(justifications,start,end)

        return False


    '''
       Verificar si esta justificado el intervalo de tiempo
       @param justifications Justificaciones del usuario
       @param start Timestamp de inicio
       @param end Timestamp final
    '''
    def _isJustifiedTime(self,justifications,start,end):
        for j in justifications:
            for just in self.justificationsTime:
                if just.isJustification(j['justification_id']):
                    return just._isJustifiedTime(j,start,end)
        return False


    def _initDay(self,date):
        # paso el date a formato local y seteo a las 00:00:00:000
        date = self.date.localizeAwareToLocal(date)
        date = date.replace(hour=0,minute=0,second=0,microsecond=0)
        # lo vuelvo a pasar a utc
        return self.date.awareToUtc(date)


    '''
    ---------------- FALTA IMPLEMENTAR ----------------------
    '''
    
    """
       Combinar justificaciones y controles
       @param controls Controles Combinacion entre schedules y worked hours
       @param justifications Justificaciones
       @param date Fecha de referencia para la combinacion
    """
    def _combinerJustifications(self, controls, justifications, date):

        #ordenar justificaciones por fecha de inicio
        justifications = sorted(justifications, key=lambda j: j['begin'])
        
        """
        #elimino las justificaciones generales
        js = []
        for j in justifications:
            for just in self.justificationsTime:
                if just.isJustification(j['justification_id']):
                    js.append(j)
                    break
        """

        #combinar justificaciones con controles
        for elem in controls:
            sched = elem['schedule']
            justs = []
            for j in justifications:
                if ('end' not in j or j['end'] is None) and j['begin'] < sched.getEnd(date):
                    justs.append(j)
                elif 'end' in j and j['end'] is not None and j['end'] > sched.getStart(date) and j['begin'] < sched.getEnd(date):
                    justs.append(j)

            elem['justifications'] = justs




    '''
        chequea los schedules contra las workedhours calculadas
        @param con Conexion con la base de datos
        @param userId Identificacion de usuario
        @param controls Controles (combinacion de schedules y worked hours)
        @param date Dia de chequeo
    '''
    def checkWorkedHours(self,con,userId,controls, date):
        fails = []

        #definir primer y ultimo schedule
        firstSched = controls[0]['schedule']
        lastSched = controls[-1]['schedule']


        #si no tiene schedule no controlo
        if firstSched == None:
            return []


        #obtener todos los whs
        allWhs = []
        
        for e in controls:
            allWhs.extend(e['whs'])
            
  
        #buscar si tiene justificacion, si no tiene la agrego como falla
        startDate = firstSched.getStart(date)
        beginDate = self._initDay(startDate)
        endDate = lastSched.getEnd(date)

        justifications = self._getJustifications(con,userId,beginDate,endDate)       
 
        #verificar si falto
        if len(allWhs) <= 0:
            if not self._isJustifiedDay(con,date,userId,justifications):
                fails.append(self._createFail(userId,date,'Sin marcación',justifications))
            return fails

        #combinar controles con justificaciones
        self._combinerJustifications(controls, justifications, date)

        for elem in controls:
            sched = elem['schedule']
            whs = elem['whs']
            justs = elem['justifications']
            
            dateSchd = sched.getStart(date)
            failsBySched = self._getFails(whs, sched, date)
       
            isFirstSchedule = sched == firstSched
            isLastSchedule = sched == lastSched

            for f in failsBySched:
                
                #  ------------ SIN MARCACION -----------
                if f['name'] == 'Sin marcación':
                    if self._isJustifiedTime(justs,sched.getStart(date),sched.getEnd(date)):
                        continue
                    else:
                        fails.append(self._createFail(userId,dateSchd,f['name'],justs))

                #  ---------- LLEGADA TARDIA -------------
                if f['name'] == 'Llegada tardía':
                    #verificar si esta justificada la llegada tardia
                    if self._isJustifiedTimeStart(justs,sched,whs,f,isFirstSchedule, date):
                        continue
                        
                    #si no esta justificada la salida temprana, definir una falla y agregarla a la lista de fallas
                    else:
                        fail = self._createFail(userId,dateSchd,f['name'],justs)
                        fail['startSchedule'] = sched.getStart(date)
                        fail['start'] = f['wh']['start']
                        fail['seconds'] =(f['wh']['start'] - sched.getStart(date)).total_seconds()
                        fail['whSeconds'] = f['wh']['seconds']
                        fails.append(fail)

                # ------------- Sin salida ---------------
                if f['name'] == 'Sin salida':
                    # no hay justificacion que justifique este tipo de falla
                    fails.append(self._createFail(userId,dateSchd,f['name'],justs))

                # ------------ Salida temprana ---------------
                if f['name'] == 'Salida temprana':
                    #verificar si esta justificada la salida temprana
                    if self._isJustifiedTimeEnd(justs, sched, whs, f, isLastSchedule, date):
                        continue

                    #si no esta justificada la salida temprana, definir una falla y agregarla a la lista de fallas
                    else:
                        fail = self._createFail(userId,dateSchd,f['name'],justs)
                        fail['endSchedule'] = sched.getEnd(date)
                        fail['end'] = f['wh']['end']
                        fail['seconds'] =(sched.getEnd(date) - f['wh']['end']).total_seconds()
                        fail['whSeconds'] = f['wh']['seconds']
                        fails.append(fail)
        return fails



    """
       obtener fallas
       @param whs Horas trabajadas correspondientes al dia de chequeo
       @param sched Horario correspondiente al dia de chequeo
       @param date Dia de chequeo
       @return lista de fallas:
          fail = {
            name: Nombre de la falla (LLegada tardía, Sin Salida, Salida Temprada)
            wh: Worked hour correspondiente a la falla
            whAnt: Worked hour anterior a la falla
            whNext: Worked hour posterior a la falla
          }
    """
    def _getFails(self, whs, sched, date):

        if len(whs) == 0:
            # sin marcacion
            return [{'name':'Sin marcación','wh':None}]

        if len(whs) == 1:
            wh = whs[0]
            if wh['start'] - self.tolerancia <= sched.getStart(date) and ('end' in wh and wh['end'] is not None) and (sched.getEnd(date) is not None) and wh['end'] + self.tolerancia >= sched.getEnd(date):
                return []

        fails = []
        whAnt = None
        iNext = 1

       
        
        for wh in whs:
            whNext = whs[iNext] if iNext < len(whs) else None
            
            # Llegada tardía
            if wh['start'] - self.tolerancia > sched.getStart(date):
                fails.append({'name':'Llegada tardía','wh':wh,'whAnt':whAnt,'whNext':whNext})
                
            # 'Sin salida'
            if 'end' not in wh or wh['end'] is None:
                fails.append({'name':'Sin salida','wh':wh,'whAnt':whAnt,'whNext':whNext})
                
            # 'Salida temprana'
            elif wh['end'] + self.tolerancia < sched.getEnd(date):
                fails.append({'name':'Salida temprana','wh':wh,'whAnt':whAnt,'whNext':whNext})
                
            whAnt = wh
            iNext = iNext + 1

        return fails

    def _createFail(self,userId,date,description,justs):
        fail =  {
                    'userId':userId,
                    'date':date,
                    'description':description,
                    'justifications':justs
                }
        return fail
