import inject
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from model.config import Config



class MailServerNotFound(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__;



class Mail:

    config = inject.attr(Config)

    def createMail(self,From,To,subject):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject,'utf-8')
        msg['From'] = From
        msg['To'] = To
        return msg

    def getHtmlPart(self,body):
        msg = MIMEText(body.encode('utf-8'),'html','utf-8')
        return msg

    def getTextPart(self,body):
        msg = MIMEText(body.encode('utf-8'),'plain','utf-8')
        return msg


    def sendMail(self, ffrom, tos, body):
      s = smtplib.SMTP(self.config.configs['mail_host'])
      try:
          if s == None:
              raise MailServerNotFound()
          s.login(self.config.configs['mail_user'],self.config.configs['mail_password'])
          s.sendmail(ffrom, tos, body)

      finally:
          s.quit()
