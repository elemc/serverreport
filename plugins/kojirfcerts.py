#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ================================= #
# Python script                     #
# Author: Alexei Panov              #
# e-mail: me AT elemc DOT name      #
# ================================= #

from srplugin import ServerReportPluginBase
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from serverreport import DEBUG_MODE
import os.path, os

class KojiCertsPlugin(ServerReportPluginBase):
    msg_param_file  = "/tmp/koji-cert-params.lst"
    cert_files_dest = "/tmp"

    def __init__(self):
        self._certname = None
        self._certemail = None
        self._certbrowser_pwd = None

        try:
            f = open(self.msg_param_file, 'r')
        except:
            if DEBUG_MODE:
                print("DEBUG: Не могу открыть файл %s" % self.msg_param_file)
            return

        for l in f:
            if len(l.strip()) == 0:
                continue
            try:
                key, value = l.split('=')
            except:
                continue
            if "certname" == key.lower():
                self._certname = value.strip()
            elif "certemail" == key.lower():
                self._certemail = value.strip()
            elif "cbpwd" == key.lower():
                self._certbrowser_pwd = value.strip()
    
    def collect(self):
        if (self._certname is None) or (self._certemail is None) or (self._certbrowser_pwd is None):
            if DEBUG_MODE:
                print("DEBUG: Параметры из файла не прочитаны!")
            return None

        mail = MIMEMultipart()

        msg_body = """
Привет, %s .
Сертификаты приложены к данному письму.
Что есть в архиве:
* client.crt - клиентский сертификат, требуется скопировать его в каталог ~/.koji/;
* clientca.crt - серверный сертификат, его также требуется скопировать в каталог ~/.koji/;
* serverca.crt - тоже серверный сертификат, и его надо скопировать в каталог ~/.koji/;
* %s_browser_cert.p12 - сертификат для браузера, пароль "%s", для установки - читай инструкцию к своему браузеру;
* koji.conf - конфигурационный файл для клиенсткого приложения koji, после установки просто скопируй его с заменой в /etc/.

На этом все.
С уважением, Russian Fedora.
""" % (self._certname, self._certname, self._certbrowser_pwd)
        msg = MIMEText( msg_body, 'plain' )
        
        mail.attach(msg)
        
        # читаем и прикладываем файл
        cert_archive_fn = os.path.join(self.cert_files_dest, "%s_koji_certs.tar.bz2" % self._certname)
        try:
            fp = open(cert_archive_fn, 'rb')
        except:
            if DEBUG_MODE:
                print("Не могу открыть файл %s" % cert_archive_fn)
            return None
        
        msg_file = MIMEBase('application', 'octet-stream')
        msg_file.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(msg_file)
        msg_file.add_header('Content-Disposition', 'attachment', filename=os.path.basename(cert_archive_fn))
        mail.attach(msg_file)
        
        return mail

    def __del__(self):
        pass
