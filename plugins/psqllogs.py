#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ================================= #
# Python script                     #
# Author: Alexei Panov              #
# e-mail: me AT elemc DOT name      #
# ================================= #

from srplugindir import ServerReportPluginDir

class PGSqlLogs(ServerReportPluginDir):
	dest_dir = "/var/lib/pgsql/data/pg_log"
	exclude_word_list = [
		"nonstandard use of \\ in a string literal at character",
		"Use the escape string syntax for backslashes, e.g., E'\\'".
		]
	def __init__(self):
		ServerReportPluginExcludeFile.__init__(self)
		
