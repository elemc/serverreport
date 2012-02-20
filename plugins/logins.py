#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ================================= #
# Python script                     #
# Author: Alexei Panov              #
# e-mail: me AT elemc DOT name      #
# ================================= #

from srplugin import ServerReportPluginBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date

SECURE_FILE="/Users/alex/workspace/temp/secure"
ONLY_THIS_MONTH=False

class UsersLoginsPlugin(ServerReportPluginBase):
    def __init__(self):
        self.secure_data = None
        self._msg_text = []
        if ( not self.check_file() ):
            self._mainmsg = MIMEText("File %s read error!" % SECURE_FILE)
            return
        self._mainmsg = None

    def _parse_secure_string(self, textline):
        if "sshd" in textline:
            if "Accepted password for" in textline:
                textline = textline.replace("Accepted password for", "Выполнен удаленный вход под пользователем")
                textline = textline.replace("from", "с адреса")
                textline = textline.replace("port", "порт")
                self._msg_text.append(textline)
            elif "Failed password for" in textline:
                textline = textline.replace("Failed password for", "Неправильный пароль для пользователя")
                textline = textline.replace("from", "с адреса")
                textline = textline.replace("port", "порт")
                self._msg_text.append(textline)
        elif "su" in textline:
            if "session opened for" in textline:
                textline = textline.replace("session opened for user", "смена привилегий на пользователя")
                textline = textline.replace("by", "для")
                self._msg_text.append(textline)
        elif "sudo" in textline:
            textline = textline.replace("sudo:", "выполнена команда с повышенными привелегиями:")
            self._msg_text.append(textline)
        elif ("groupadd" in textline) and ("new group" in textline):
            textline = textline.replace("new group", "Создана новая группа")
            textline = textline.replace("name", "наименование")
            self._msg_text.append(textline)
        elif ("useradd" in textline) and ("new user" in textline):
            textline = textline.replace("new user", "Создан новый пользователь")
            textline = textline.replace("name", "Имя")

    def _check_secure_string(self, textline):
        if ONLY_THIS_MONTH:
            month_name = date.today().strftime("%b")
            if month_name in textline:
                return True
        else:
            return True

        return False

    def check_file(self):
        try:
            fp = open(SECURE_FILE, 'r')
        except:
            return False

        for line in fp:
            if ( self._check_secure_string(line) ):
                self._parse_secure_string( line )
        fp.close()
        return True

    def __del__(self):
        pass

    def collect(self):
        if self._mainmsg is None:
            self._mainmsg = MIMEText( "Отчет безопасности системы:\n%s" % (str().join(self._msg_text)) )
        return self._mainmsg
