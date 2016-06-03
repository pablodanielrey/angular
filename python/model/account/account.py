# -*- coding: utf-8 -*-
import inject
from model.users.users import User, MailDAO, Student
from model.laboralinsertion.laboralInsertion import LaboralInsertion

class AccountModel:

    laboralInsertion = inject.instance(LaboralInsertion)
    # anibal, ezequiel
    detise = ['4eb3ca83-34a0-45b4-895f-1b4da3390fdd', '8ade8f8d-c9e1-4a0c-8d9d-16d5e4b721af']
    # sebastian
    posgrado = ['86d5f163-a890-4695-a666-643c0ae05138']
    # paula
    insercion = ['9c5cf510-cc0d-4cc2-83e5-e61e3e39be58']
    # emanuel, walter, ivan, alejandro, santiago, maxi, pablo
    ditesi = ['0cd70f16-aebb-4274-bc67-a57da88ab6c7', '205de802-2a15-4652-8fde-f23c674a1246', 'd44e92c1-d277-4a45-81dc-a72a76f6ef8d',
            '35f7a8a6-d844-4d6f-b60b-aab810610809', '4b89c515-2eba-4316-97b9-a6204d344d3a', 'cd8fbf39-4ad2-4d11-b17b-3b070105f870',
            '89d88b81-fbc0-48fa-badb-d32854d3d93a'
    ]

    student = 'student'
    teacher = 'teacher'
    postgraduate = 'postgraduate'
    assistance = 'assistance'
    graduate = 'graduate'

    def getTypes(self, con, userId):
        if userId in self.detise:
            return [self.student, self.teacher, self.postgraduate, self.graduate]
        if userId in self.posgrado:
            return [self.student, self.teacher, self.postgraduate, self.graduate]
        if userId in self.insercion:
            return [self.student, self.teacher, self.postgraduate, self.graduate]
        if userId in self.ditesi:
            return [self.student, self.teacher, self.postgraduate, self.assistance, self.graduate]
        return []


    def _verify(self, userId, type):
        if userId in self.detise:
            return (type == self.student or type == self.teacher or type == self.postgraduate or type == self.graduate)
        if userId in self.posgrado:
            return (type == self.student or type == self.teacher or type == self.postgraduate or type == self.graduate)
        if userId in self.insercion:
            return (type == self.student or type == self.teacher or type == self.postgraduate or type == self.graduate)
        if userId in self.ditesi:
            return True

    def updateType(self, con, userId, user, type):
        if self._verify(userId, type):
            users = User.findById(con, [user.id])
            if len(users) <= 0:
                raise Exception("No existe el usuario")
            u = users[0]
            u.type = type
            u.updateType(con)
            return u.id
        else:
            raise Exception("No tiene permisos para cambiar el tipo")


    def createUser(self, con, user, studentNumber, type):
        '''
            user: {'dni': '1233487', 'lastname': 'pompin', 'name': 'pepe'}
            studentNumber : '111/1'
            type: 'student | teacher'
        '''
        # creo el usuario
        person = User()
        person.dni = user['dni']
        person.lastname = user['lastname']
        person.name = user['name']
        person.type = type
        person.id = person.persist(con)
        person.updateType(con)

        # creo el student
        if studentNumber is not None and studentNumber != '':
           s = Student()
           s.id = person.id
           s.studentNumber = studentNumber
           s.persist(con)


    def deleteMail(self, con, id):
        self.laboralInsertion.deleteMail(con, id)
        MailDAO.delete(con, id)

    def findByDni(self, con, userId, dni):
        data = User.findByDni(con, dni)
        users = [] if data is None else User.findById(con, [data[0]])
        if userId in self.detise:
            return [u for u in users if u.type == self.student or u.type == self.teacher or u.type == self.postgraduate or u.type == self.graduate or u.type is None]
        if userId in self.posgrado:
            return [u for u in users if u.type == self.student or u.type == self.teacher or u.type == self.postgraduate or u.type == self.graduate or u.type is None]
        if userId in self.insercion:
            return [u for u in users if u.type == self.student or u.type == self.teacher or u.type == self.postgraduate or u.type == self.graduate or u.type is None]
        if userId in self.ditesi:
            return users
