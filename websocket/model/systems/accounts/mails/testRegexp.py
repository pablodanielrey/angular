
import re

f = open('requestAccountConfirmation.html','r')
body = f.read()
print re.sub('###NAME###','nombre',body)
