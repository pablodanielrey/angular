
import sys
sys.path.append('/home/ivan/www/angular/python') #definir ruta de acceso al modelo


from model import SqlContext
from model.users.entities.user import User

con = None
ctx = SqlContext(con)
user = User()


User.findBy(ctx)



User.findBy(ctx, userId=["123"])



User.findBy(ctx, userId=["123"], officeId=["123", "345"])



User.findBy(ctx, userId=True, valorBooleano=False, officeId=["123", "345"], orderBy={"officeId":True})










"""
ctx = SqlContext(con)

Office.findBy(ctx, userId=["123"])



Office.findBy(ctx, userId=["123"], officeId=["123", "345"])



Office.findBy(ctx, userId=True, valorBooleano=False, officeId=["123", "345"], orderBy={"officeId":222})



"""
