# -*- coding: utf-8 -*-
'''
    implementa el modelo de los mails.
    debe agregarse las secciones a la config

    [mail]
    host = hosts
    user = usuario
    password = clave
    enabled = true|false

'''
import inject, smtplib, re

import email
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

from model.registry import Registry
# from model.exceptions import *


class Mail:

    def __init__(self):
        self.mailRe = re.compile('.*<(.*@.*)>.*')
        reg = inject.instance(Registry)
        self.registry = reg.getRegistry('mail')

    def __extractFrom(self,ffrom):
        fr = self.mailRe.match(ffrom)
        if fr is None:
            return ffrom
        fffrom = fr.group(1)
        return fffrom

    def createMail(self,From,To,subject):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = Header(subject,'utf-8')
        msg['From'] = From
        msg['To'] = Header(To,'utf-8')
        return msg

    def getHtmlPart(self,body):
        msg = MIMEText(body,'html','utf-8')
        return msg

    def getTextPart(self, body):
        msg = MIMEText(body,'plain','utf-8')
        return msg

    def getFilePart(self, name, data, content_type='application', subtype='pdf'):
        b = MIMEBase(content_type, subtype)
        b.set_payload(data)
        email.encoders.encode_base64(b)
        b.add_header('Content-Disposition','attachment;filename={}'.format(name))
        return b

    def _sendMail(self, ffrom, tos, body):
        host = self.registry.get('host')
        s = smtplib.SMTP(host)
        try:
            if s == None:
              raise MailServerNotFound()

            authenticated = self.registry.get('authenticated')
            if authenticated and authenticated == 'true':
                user = self.registry.get('user')
                if user is not None:
                  username = user
                  password = self.registry.get('password')
                  s.login(username, password)

            s.send_message(body,from_addr=ffrom,to_addrs=tos)
            #From = self.__extractFrom(ffrom)
            #s.sendmail(From.encode('iso-8859-1'), tos, body)

        finally:
          s.quit()


    """ envía un mail con partes en html y partes en texto """
    def sendMail(self, ffrom, tos, subject, replace=[], html=None, text=None):
        enabled = self.registry.get('enabled')
        if not enabled:
            return;

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
            self._sendMail(ffrom,[to],msg)
