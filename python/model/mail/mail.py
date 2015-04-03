import inject, smtplib, re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from model.config import Config
from wexceptions import *


class Mail:

    config = inject.attr(Config)

    def __init__(self):
        self.mailRe = re.compile('.*<(.*@.*)>.*')

    def __extractFrom(self,ffrom):
        fr = self.mailRe.match(ffrom)
        if fr is None:
            return ffrom
        fffrom = fr.group(1)
        return fffrom

    def createMail(self,From,To,subject):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject,'utf-8')
        msg['From'] = Header(From,'utf-8')
        msg['To'] = Header(To,'utf-8')
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

          s.send_message(body)
          #From = self.__extractFrom(ffrom)
          #s.sendmail(From.encode('iso-8859-1'), tos, body)

      finally:
          s.quit()


    """ envía un mail con partes en html y partes en texto """
    def sendMail(self,ffrom,tos,subject,replace=[],html=None,text=None):

        parts = []

        if html:
            fTemplate = open(html,'r')
            try:
                hbody = fTemplate.read()
                for pattern,data in replace:
                    hbody = re.sub(pattern, data, hbody)
                parts.append(self.getHtmlPart(hbody))
            finally:
                fTemplate.close()

        if text:
            fTemplate = open(text,'r')
            try:
                tbody = fTemplate.read()
                for pattern,data in replace:
                    tbody = re.sub(pattern, data, tbody)
                parts.append(self.getTextPart(tbody))
            finally:
                fTemplate.close()

        for to in tos:
            msg = self.createMail(ffrom,to,subject)
            for part in parts:
                msg.attach(part)
            self._sendMail(ffrom,[to],msg.as_string())
