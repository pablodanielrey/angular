# -*- coding: utf-8 -*-
from model import Ids
from model.entity import Entity

class Student(Entity):

    def __init__(self):
        self.id = None
        self.student_number = None
        
