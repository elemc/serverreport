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
    def __init__(self):
        self._uname()
        self._mainmsg = MIMEMultipart()
        self._mainmsg['Subject'] = "%s report from %s" % (REPORT_PERIOD_TYPE, self.uname_nodename)
        self._mainmsg['From'] = EMAIL_FROM
        self._mainmsg['To'] = str(', ').join(EMAIL_TO)
        self._mainmsg.preamble = "%s report from %s %s %s %s %s" % (
            REPORT_PERIOD_TYPE,
            self.uname_sysname,
            self.uname_nodename,
            self.uname_release,
            self.uname_version,
            self.uname_machine )
        
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
            s = smtplib.SMPT(SMTP_HOST, SMTP_PORT)
        s.login(SMTP_USER, SMTP_PASSWORD)
        s.sendmail(EMAIL_FROM, EMAIL_TO, self._mainmsg.as_string())

    def __del__(self):
        pass
