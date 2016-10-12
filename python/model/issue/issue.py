# -*- coding: utf-8 -*-
from redmine import Redmine
from model.users.users  import UserPassword, User, Mail
from model.offices.office import Office
from model.serializer import JSONSerializable
from model.registry import Registry
import base64
import logging
import datetime
import uuid
import re
from model.assistance.utils import Utils


import cProfile

def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return profiled_func



class Issue(JSONSerializable):

    def __init__(self):
        self.id = None
        self.parentId = None
        self.projectId = None
        self.office = None
        self.priority = 2
        self.area = None
        self.userId = None
        self.subject = ''
        self.description = None
        self.statusId = 1
        self.assignedToId = None
        self.files = []
        self.start = datetime.date.today()
        self.updated = None
        self.children = []
        self.files = []
        self.tracker = RedmineAPI.TRACKER_ERROR
        self.fromOfficeId = None
        self.creatorId = None

    @classmethod
    def findById(cls, con, id):
        return RedmineAPI.findByIds(con, [id])

    @classmethod
    def findByIds(cls, con, ids):
        return RedmineAPI.findByIds(con, ids)

    @classmethod
    def getOfficesIssues(cls, con, officeIds):
        return RedmineAPI.getOfficesIssues(con, officeIds)

    @classmethod
    def getMyIssues(cls, con, userId, statuses, froms, tos):
        return RedmineAPI.getMyIssues(con, userId, statuses, froms, tos)

    @classmethod
    def getAssignedIssues(cls, con, userId, oIds, statuses, froms):
        return RedmineAPI.getAssignedIssues(con, userId, oIds, statuses, froms)

    def changeStatus(self, status):
        return RedmineAPI.changeStatus(self.id, self.projectId, status)

    def changePriority(self, priority):
        return RedmineAPI.changePriority(self.id, self.projectId, priority)

    def create(self, con):
        return RedmineAPI.create(con, self)


class Attachment(JSONSerializable):

    def __init__(self):
        self.id = ''
        self.url = ''
        self.size = 0
        self.name = ''


class RedmineAPI:

    import os
    REDMINE_URL = os.environ['ISSUES_REDMINE']
    KEY = os.environ['ISSUES_REDMINE_KEY']
    TRACKER_ERROR = 1
    TRACKER_COMMENT = 4
    STATUS_NEW = 1
    STATUS_WORKING = 2
    STATUS_FINISH = 3
    STATUS_CLOSE = 5
    CREATOR_FIELD = 1
    FROM_FIELD = 2

    @classmethod
    def _loadFile(cls, file):
        att = Attachment()
        att.id = file.id
        att.url = file.content_url
        att.size = file.filesize
        att.name = file.filename
        return att


    officeRedmineIdCache = {}
    officeIdCache = {}
    officeCache = {}

    @classmethod
    def _loadOffice(cls, con, redmine, officeId):
        if officeId is None:
            return None

        id = None
        if officeId not in cls.officeRedmineIdCache.keys():
            project = redmine.project.get(officeId)
            id = project.identifier
            cls.officeRedmineIdCache[officeId] = id
            cls.officeIdCache[id] = officeId
        else:
            id = cls.officeRedmineIdCache[officeId]

        """
        saco la cache de office asi las obtengo siempre desde le server
        office = None
        if id not in cls.officeCache.keys():
            office = cls._findOffice(con, id)
            cls.officeCache[id] = office
        else:
            office = cls.officeCache[id]

        return office
        """
        return cls._findOffice(con, id)

    @classmethod
    def _findOffice(cls, con, id):
        if id is None:
            return None

        """ saco la cache
        office = None
        if id not in cls.officeCache.keys():
            offices = Office.findByIds(con, [id])
            office = offices[0] if len(offices) > 0 else None
            cls.officeCache[id] = office
        else:
            office = cls.officeCache[id]

        return office
        """
        offices = Office.findByIds(con, [id])
        office = offices[0] if len(offices) > 0 else None
        return office


    """
    metodos codificados por ema sin cache.
    @classmethod
    def _loadOffice(cls, con, redmine, officeId):
        if officeId is None:
            return None

        offId = cls.officeRedmineIdCache[officeId]

        project = redmine.project.get(officeId)
        id = project.identifier
        return cls._findOffice(con, id)

    @classmethod
    def _findOffice(cls, con, id):
        if id is None:
            return None

        offices = Office.findByIds(con, [id])
        return offices[0] if len(offices) > 0 else None
    """

    @classmethod
    def _getCreatorOfficeId(cls, r):
        for cf in r.custom_fields:
            if cf.id == cls.FROM_FIELD:
                return cf.value
        return None

    @classmethod
    def _fromResult(cls, con, r, redmine, related=False):

        logging.info(r)

        attrs = dir(r)
        issue = Issue()
        issue.id = r.id
        issue.parentId = [r.parent.id if 'parent' in attrs else None][0]
        issue.projectId =  [r.project.id if 'project' in attrs else None][0]

        office = cls._loadOffice(con, redmine, issue.projectId)
        if office is not None and office.type is not None and office.type['value'] == 'area':
            issue.area = office
            issue.office = cls._findOffice(con, office.parent)
        else:
            issue.area = None
            issue.office = office

        issue.projectName = [r.project.name if 'project' in attrs else None][0]

        issue.userId = cls._loadUserByUIdRedmine(con, r.author.id, redmine)
        issue.subject = r.subject
        issue.description = r.description

        issue.priority = r.priority.id
        issue.statusId = r.status.id
        issue.assignedToId =[r.assigned_to.id if 'assigned_to' in attrs else None][0]

        issue.start = Utils._localizeUtc(r.created_on) if Utils._isNaive(r.created_on) else r.created_on
        issue.updated = Utils._localizeUtc(r.updated_on) if Utils._isNaive(r.updated_on) else r.updated_on

        for cf in r.custom_fields:
            if cf.id == cls.CREATOR_FIELD:
                issue.creatorId = cf.value
            elif cf.id == cls.FROM_FIELD:
                issue.fromOfficeId = cf.value
                issue.fromOffice = cls._findOffice(con, issue.fromOfficeId)

        if related:
            childrens = [iss.id for iss in r.children if iss is not None]
            issue.children = cls.findByIds(con, childrens)
            issue.files = [cls._loadFile(file) for file in r.attachments if file is not None]

        return issue


    @classmethod
    def findByIds(cls, con, issuesIds, childrens=False, attachments=False):
        """ retorna los issues del modelo nuestro identificados por los ids issuesIds """
        assert isinstance(issuesIds, list)

        redmine = cls._getRedmineInstance()
        if redmine is None:
            return None

        includes = []
        if childrens:
            includes.append('childrens')
        if attachments:
            includes.append('attachments')

        issues = []
        for issueId in issuesIds:
            try:
                if len(includes) > 0:
                    issues.append(redmine.issue.get(issueId, include=','.join(includes)))
                else:
                    issues.append(redmine.issue.get(issueId))
            except Exception as e:
                logging.exception(e)
                logging.error('------------------------------------')
                logging.error('error obteniendo issue {}'.format(issueId))
                logging.error('------------------------------------')
        return [cls._fromResult(con, issue, redmine, True) for issue in issues]


    @classmethod
    def _findUserId(cls, con, redmine, userId):
        """ retorna el id del usuario de nuestra base a id de usuario de redmine """
        ups = UserPassword.findByUserId(con, userId)
        if len(ups) <= 0:
            return None
        up = ups[0]

        user = cls._getUserRedmine(up, userId, con)
        return user.id

    @classmethod
    def _getRedmineInstance(cls, con = None, userId = None, isImpersonate = False):
        if isImpersonate is None or not isImpersonate:
            return Redmine(cls.REDMINE_URL, key = cls.KEY, version='3.3', requests={'verify': False})
        else:
            ups = UserPassword.findByUserId(con, userId)
            if len(ups) <= 0:
                return None
            up = ups[0]
            userRedmine = cls._getUserRedmine(up, userId, con).login
            return Redmine(cls.REDMINE_URL, key = cls.KEY, impersonate = userRedmine, version='3.3', requests={'verify': False})

    @classmethod
    def _getUserRedmine(cls, up, uid, con):
        redmine = cls._getRedmineInstance(cls, con)
        user = up.username
        usersRedmine = redmine.user.filter(name=user)
        if len(usersRedmine) <= 0:
            usersRedmine = [cls._createUserRedmine(uid, up, con, redmine)]
        return usersRedmine[0]

    @classmethod
    def _createUserRedmine(cls, uid, up, con, redmine):
        u = User.findById(con, [uid])[0]
        mails = Mail.findByUserId(con, uid)
        mailsEcono = [ mail for mail in mails if '@econo.unlp.edu.ar' in mail.email]
        mail = mailsEcono[0].email if len(mailsEcono) > 0 else (mails[0].email if len(mails) > 0 else None)

        user = redmine.user.new()
        user.login = u.dni
        user.password = up.password
        user.firstname = u.name
        user.lastname = u.lastname
        user.mail = mail
        user.save()
        return user

    @classmethod
    def _loadUserByUIdRedmine(cls, con, uid, redmine):
        userRedmine = redmine.user.get(uid)
        dni = userRedmine.login if userRedmine != None and 'login' in dir(userRedmine) else None
        (userId, version) = User.findByDni(con, [dni])[0]
        return userId

    @classmethod
    def findAllProjects(cls):
        redmine = cls._getRedmineInstance()
        if redmine is None:
            return []
        projects = redmine.project.all()
        return [p.identifier for p in projects]

    @classmethod
    def getOfficesIssues(cls, con, officeIds):
        userIds = Office.findOfficesUsers(con, officeIds)
        issues = []
        for userId in userIds:
            issues.extend(cls.getMyIssues(con, userId))
        # return [cls._fromResult(con, issue) for issue in issues if not cls._include(issues,issue)]
        return [issue for issue in issues if not cls._include(issues,issue)]

    @classmethod
    def getMyIssues(cls, con, userId, statuses, froms, tos):
        redmine = cls._getRedmineInstance()
        user = cls._findUserId(con, redmine, userId)
        issues = cls._getIssuesByUser(con, user, statuses, froms, tos, redmine)
        return [issue for issue in issues]
        #return [cls._fromResult(con, issue, redmine) for issue in issues if not cls._include(issues,issue)]

    @classmethod
    def _getIssuesByUser(cls, con, userId, statuses, froms, tos, redmine):
        if redmine is None:
            return []
        issues = redmine.issue.filter(author_id=userId, status_id='open')
        """ elimino las que tienen padre """
        rissues = [issue.id for issue in issues if 'parent' not in dir(issue)]
        #return [issue.id for issue in issues]
        return rissues

    @classmethod
    # @do_cprofile
    def getAssignedIssues(cls, con, userId, oIds, froms=None, statuses=None):
        """
            Retorna una lista de issues asignados a las oficinas : oIds
            froms = de quien proviene el Issue. si es [] entonces retorna todos los que NO TENGAN oficina de origen. Si es None no se tiene en cuenta.
            statuses = estados de los issues. si es None no se tiene en cuenta como filtro.
        """
        assert isinstance(oIds,list)
        if len(oIds) <= 0:
            return []

        if statuses is not None:
            assert isinstance(statuses,list)
            if len(statuses) <= 0:
                return []

        redmine = cls._getRedmineInstance(con)
        userRedmine = cls._findUserId(con, redmine, userId)
        issues = cls._getIssuesByProject(con, oIds, froms, statuses, userRedmine, redmine)
        return [i.id for i in set(issues)]

    @classmethod
    def _getIssuesByProject(cls, con, pIds, cIds, statuses, user, redmine):
        if redmine is None:
            return []
        issues = []
        projects = [p.identifier for p in redmine.project.all()]
        for pId in pIds:
            # issues.extend(redmine.issue.filter(tracker_id=cls.TRACKER_ERROR, project_id=pidentifier, subproject_id='!*', status_id='open'))

            if pId in projects:
                if cIds is None:
                    issues.extend(redmine.issue.filter(tracker_id=cls.TRACKER_ERROR, project_id=pId, status_id='open'))

                elif len(cIds) <= 0:
                    """
                        no tienen oficina origen
                    """
                    logging.info('filtrando por cIds = []')
                    auxIssues = redmine.issue.filter(tracker_id=cls.TRACKER_ERROR, project_id=pId, status_id='open')
                    issues.extend([iss for iss in auxIssues if not cls._hasCustomField(iss, RedmineAPI.FROM_FIELD)])

                else:
                    """
                    No funciona como dice la documentación!!. asi que lo filtro despues de obtenerlos MALISIMOO!!!

                    for cId in cIds:
                        logging.info('Filtrando por from_field {}'.format(cId))
                        cFields = [cls._getCustomFieldToFilter(RedmineAPI.FROM_FIELD, cId)]
                        issues.extend(redmine.issue.filter(tracker_id=cls.TRACKER_ERROR, project_id=pId, custom_fields=cFields, status_id='open'))
                    """

                    auxIssues = redmine.issue.filter(tracker_id=cls.TRACKER_ERROR, project_id=pId, status_id='open')
                    filteredIssues = set()
                    for cId in cIds:
                        filteredIssues.update([iss for iss in auxIssues if cls._hasCustomFieldValue(iss, RedmineAPI.FROM_FIELD, cId)])
                    issues.extend(filteredIssues)

        logging.info(issues)
        return issues

    @classmethod
    def _include(cls, issues, issue):
        ids = []
        aux = issue

        while 'parent' in dir(aux) and aux.parent:
            ids.append(aux.id)
            aux = aux.parent

        for iss in issues:
            if iss.id in ids:
                return True
        return False

    @classmethod
    def create(cls, con, iss):
        redmine = cls._getRedmineInstance(con, iss.userId, True)
        if redmine is None:
            return None

        issue = redmine.issue.new()

        issue.project_id = iss.projectId
        issue.subject = iss.subject
        issue.description = iss.description
        issue.status_id = iss.statusId
        issue.parent_issue_id = iss.parentId
        issue.start_date = iss.start
        issue.tracker_id = iss.tracker
        issue.priority_id = iss.priority
        cfields = cls.getCustomFields(iss)
        if len(cfields) > 0:
            issue.custom_fields = cfields
        issue.uploads = iss.files
        issue.save()

        return issue.id


    """
        ///////////////////////////// CUSTOM FIELDS //////////////////////////////
        ////// FROM = oficina de la que viene el pedido
        ////// CREATOR = quien cargo el pedido
        ///////////
    """

    @classmethod
    def _hasCustomField(cls, issue, customId):
        for cf in issue.custom_fields:
            if cf['id'] == customId:
                if cf['value'] is not None and cf['value'].strip() != '':
                    return True
        return False

    @classmethod
    def _hasCustomFieldValue(cls, issue, customId, value):
        for cf in issue.custom_fields:
            if cf['id'] == customId and cf['value'] == value:
                return True
        return False

    @classmethod
    def _getCustomFieldToFilter(cls, customId, value):
        return {'id':customId, 'value': value}

    @classmethod
    def getCustomFields(cls, issue):
        custom_fields = []
        if issue.creatorId != issue.userId and issue.creatorId is not None:
            custom_fields.append({'id': RedmineAPI.CREATOR_FIELD, 'value': issue.creatorId})
        if issue.fromOfficeId is not None:
            custom_fields.append({'id': RedmineAPI.FROM_FIELD, 'value': issue.fromOfficeId})
        return custom_fields

    """
        //////////////////////////////////////////////
    """

    @classmethod
    def changeStatus(cls, issue_id, project_id, status):
        redmine = cls._getRedmineInstance()
        if status is None or redmine is None:
            return None
        return redmine.issue.update(issue_id, status_id = status)

    @classmethod
    def changePriority(cls, issue_id, project_id, priority):
        redmine = cls._getRedmineInstance()
        if priority is None or redmine is None:
            return None
        return redmine.issue.update(issue_id, priority_id = priority)


class IssueModel():
    TRACKER_ERROR = RedmineAPI.TRACKER_ERROR
    TRACKER_COMMENT = RedmineAPI.TRACKER_COMMENT
    cache = {}
    ditesiId = '117ae745-acb3-48df-9005-343538f85403'
    soporteId = '4a3409e3-b4f0-43ab-b922-98a1138e3360'
    desarroloId = 'e55e67d4-9675-4bdf-bed0-da3adc0aec71'
    servidoresId = '02ad99c8-934d-402b-ab3e-64fd2440de05'

    @classmethod
    def getSubjectTypes(cls, con, oId):
        generic = [
            'Quiero una cuenta institucional de correo',
            'No tengo usuario y clave',
            'No me acuerdo mi usuario/clave',
            'Ingreso mi clave pero me dice acceso denegado/incorrecto',
            'No tengo acceso a internet',
            'No puedo enviar correo',
            'No puedo recibir correo',
            'Envié correo y no llega a destino',
            'Me enviaron correo y no lo recibo',
            'Tengo problemas con la libreta de direcciones'
        ]
        systems = [
            'No puedo entrar al sistema',
            'No puedo entrar al au24',
            'No funciona el sistema de Asistencia',
            'No funciona el sistema de Pedidos',
            'No funciona el sistema de Inserción Laboral',
            'No puedo actualizar mis datos',
            'No puedo subir mi CV',
            'Error en el sistema'
        ]
        net = [
            'No me puedo conectar a la wifi',
            'Estoy conectado a wifi pero no navega'
        ]
        supp = [
            'El equipo no enciende',
            'El equipo anda lento',
            'El equipo hace mucho ruido',
            'El equipo se apaga solo',
            'Error de Windows o Programas',
            'Problemas con Monitor',
            'No encuentro un archivo',
            'Problemas con la nube (archivos)',
            'Me quede sin espacio en disco',
            'No puedo imprimir',
            'Problemas con la impresora',
            'Virus',
            'Problema de perfil de usuario'
        ]
        if oId == cls.ditesiId:
            r = []
            r.extend(generic)
            r.extend(systems)
            r.extend(net)
            r.extend(supp)
            r.append('Otro')
            return r
        elif oId == cls.soporteId:
            r = []
            r.extend(generic)
            r.extend(net)
            r.extend(supp)
            r.append('Otro')
            return r
        elif oId == cls.desarroloId:
            r = []
            r.extend(systems)
            r.append('Otro')
            return r
        elif oId == cls.servidoresId:
            r = []
            r.extend(generic)
            r.extend(systems)
            r.extend(net)
            r.append('Otro')
            return r
        else:
            return ['Otro']

    @classmethod
    def getOffices(cls, con, userId):
        """
            retorna las oficinas públicas que están permitidas como destino de pedidos.
            oficinas públicas.
            suboficinas de las oficinas a la que pertenece la persona (tipo: direcciones y departamentos).
        """
        officesIds = Office.findAll(con)
        projects = RedmineAPI.findAllProjects()
        offices = Office.findByIds(con, [oid for oid in officesIds if oid in projects])
        publicOffices = [o for o in offices if o.public]

        userOfficesIds = Office.findByUser(con, userId, types=['direction','department'], tree=True)
        userOffices = Office.findByIds(con, [oid for oid in userOfficesIds if oid in projects])

        if userOffices is not None:
            idPublicOffices = [o.id for o in publicOffices]
            publicOffices.extend([o for o in userOffices if o.id not in idPublicOffices])

        return publicOffices

    @classmethod
    def getAreas(cls, con, oId):
        """
            Retorna las suboficinas de oId que tienen tipo área.
            También se les puede realizar pedidos a las áreas específicas.
        """
        offs = Office.findByIds(con, [oId])
        if offs is None or len(offs) <= 0:
            return []
        areas = offs[0].findChilds(con, types=['area'], tree=False)
        return Office.findByIds(con, areas)

    @classmethod
    def create(cls, con, parentId, officeId, authorId, subject, description, fromOfficeId, creatorId, files, tracker = TRACKER_ERROR):
        issue = Issue()
        issue.parentId = parentId
        issue.projectId = officeId
        issue.userId = authorId
        issue.subject = subject
        issue.description = description
        issue.tracker = tracker
        issue.fromOfficeId = fromOfficeId
        issue.creatorId = creatorId


        issue.files = []
        for file in files:
            data = base64.b64decode(file['content'])
            id = str(uuid.uuid4())
            path = '/tmp/' + id
            f = open(path, 'wb')
            f.write(data)
            f.close()
            issue.files.append({'path':path, 'filename':file['name'], 'content_type': file['type']})

        return issue.create(con)

    @classmethod
    def searchUsers(cls, con, regex):
        assert regex is not None

        if regex == '':
            return []

        userIds = User.search(con, regex)

        users = []
        for u in userIds:
            (uid, version) = u
            if uid not in cls.cache.keys():
                print(uid)
                user = User.findById(con, [uid])[0]
                cls.cache[uid] = user
            users.append(cls.cache[uid])

        """
            antes de implementar el search en users se usaba esto.
        m = re.compile(".*{}.*".format(regex), re.I)
        matched = []

        digits = re.compile('^\d+$')
        if digits.match(regex):
            ''' busco por dni '''
            matched = [ cls._getUserData(con, u) for u in users if m.search(u.dni) ]
            return matched

        ''' busco por nombre y apellido '''
        matched = [ cls._getUserData(con, u) for u in users if m.search(u.name) or m.search(u.lastname) ]
        return matched
        """

        return [cls._getUserData(con, u) for u in users]



    @classmethod
    def _getUserData(cls, con, user):
        u = UserIssueData()
        u.name = user.name
        u.lastname = user.lastname
        u.dni = user.dni
        u.id = user.id
        u.genre = user.genre
        u.photo = [User.findPhoto(con, user.photo) if 'photo' in dir(user) and user.photo is not None and user.photo != '' else None][0]
        return u

class UserIssueData(JSONSerializable):

    def __init__(self):
        self.name = ''
        self.lastname = ''
        self.dni = ''
        self.photo = ''
        self.id = ''
