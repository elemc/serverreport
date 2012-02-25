#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ================================= #
# Python script                     #
# Author: Alexei Panov              #
# e-mail: me AT elemc DOT name      #
# ================================= #

from email.mime.text import MIMEText

class ServerReportPluginBase(object):
    def __init__(self):
		pass

    def collect(self):
        msg = MIMEText("Base plugin")
        return msg

    def __del__(self):
        pass

