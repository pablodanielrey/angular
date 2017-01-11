

import sys
sys.path.append('/home/ivan/www/angular/python') #definir ruta de acceso al modelo


from model import SqlContext
from model.users.entities.user import User

con = None
ctx = SqlContext(con)
user = User()


User.find(ctx)



User.find(ctx, userId=["123"])



User.find(ctx, userId=["123"], officeId=["123", "345"])



User.find(ctx, userId=True, valorBooleano=False, officeId=["123", "345"], orderBy={"officeId":True})



User.findByIds(ctx, [123])

User.findByIds(ctx, [123], userId=True, officeId=["123", "445"])








"""
ctx = SqlContext(con)

Office.findBy(ctx, userId=["123"])



Office.findBy(ctx, userId=["123"], officeId=["123", "345"])



Office.findBy(ctx, userId=True, valorBooleano=False, officeId=["123", "345"], orderBy={"officeId":222})



"""
