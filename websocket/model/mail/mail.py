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
        msg = MIMEText(body,'html','utf-8')
        return msg

    def getTextPart(self,body):
        msg = MIMEText(body,'plain','utf-8')
        return msg


    def _sendMail(self, ffrom, tos, body):
      s = smtplib.SMTP(self.config.configs['mail_host'])
      try:
          if s == None:
              raise MailServerNotFound()
          s.login(self.config.configs['mail_user'],self.config.configs['mail_password'])
          s.sendmail(ffrom, tos, body)

      finally:
          s.quit()


    """ envía un mail con partes en html y partes en texto """
    def sendMail(self,ffrom,tos,subject,replace,html=None,text=None):

        parts = []

        if html:
            fTemplate = fopen(html,'r')
            try:
                hbody = fTemplate.read()
                for pattern,data in replace:
                    hbody = re.sub(pattern, data, hbody)
                parts.append(self.getHtmlPart(hbody))
            finally:
                fTemplate.close()

        if text:
            fTemplate = fopen(text,'r')
            try:
                tbody = fTemplate.read()
                for pattern,data in replace:
                    tbody = re.sub(pattern, data, tbody)
                parts.append(self.getTextPart(tbody))
            finally:
                fTemplate.close()

        for to in tos:
            msg = self.mail.createMail(From,To,subject)
            for part in parts:
                msg.attach(part)
            self._sendMail(From,[To],msg.as_string())
