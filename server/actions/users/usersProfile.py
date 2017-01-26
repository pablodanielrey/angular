# -*- coding: utf-8 -*-
import inject
import logging
import uuid
# import asyncio
# from asyncio import coroutine
# from autobahn.asyncio.wamp import ApplicationSession

from model.users.usersAdminModel import UserAdminModel




# from model.exceptions import *

import autobahn
import wamp

class UsersProfile(wamp.SystemComponentSession):
