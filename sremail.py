#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ================================= #
# Python script                     #
# Author: Alexei Panov              #
# e-mail: me AT elemc DOT name      #
# ================================= #

from email.mime.multipart import MIMEMultipart
from emailsettings import *
import os
import smtplib

class ServerReportEmail(object):
    def __init__(self, email):
        #self._uname()
        self.email_to = email
        self._mainmsg = MIMEMultipart()
        self._mainmsg['Subject'] = EMAIL_SUBJECT #% (self.uname_nodename, REPORT_PERIOD_TYPE)
        self._mainmsg['From'] = EMAIL_FROM
        self._mainmsg['To'] = self.email_to
        self._mainmsg.preamble = "Сертификаты на сервер koji.russianfedora.ru"
        
    def _uname(self):
        (self.uname_sysname,
         self.uname_nodename,
            self.uname_release,
            self.uname_version,
            self.uname_machine) = os.uname()

    def add_content(self, content):
        self._mainmsg.attach(content)

    def send(self):
        s = None
        if SMTP_USE_SSL:
            s = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            s = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        s.login(SMTP_USER, SMTP_PASSWORD)
        s.sendmail(EMAIL_FROM, self.email_to, self._mainmsg.as_string())

    def __del__(self):
        pass
