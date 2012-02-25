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

class ServerReportPluginReplaceFile(ServerReportPluginBase):
	filename_for_report = None;
	dict_of_replace = {}
	
	def __init__(self):
		ServerReportPluginBase.__init__(self)
		self._buffer = []
		self._openfile()
		self._do_buffer()
		self._check_buffer()

	def _openfile(self):
		if self.filename_for_report is None:
			return
		fp = open(self.filename_for_report, 'r')
		for line in fp:
			self._buffer.append(line.strip())
		fp.close()
	
	def __del__(self):
		while( len(self._buffer) != 0 ):
			self._buffer.remove(self._buffer[0])

	def collect(self):
		if self.filename_for_report is None:
			return None
		msg_body = str('\n').join(self._buffer)
		msg = MIMEText("Отчет по файлу %s\n%s\n\n" % (self.filename_for_report, msg_body))
		return msg

	def _do_buffer(self):
		if ( len( self.dict_of_replace.keys() ) == 0 ):
			return

		new_buffer = []
		for line in self._buffer:
			founded = 0
			for key in self.dict_of_replace.keys():
				replace_str = self.dict_of_replace[key]
				if key in line:
					founded += 1
					line = line.replace(key, replace_str)

			if founded > 0:
				new_buffer.append(line)

		self._buffer = new_buffer

	def _check_buffer(self):
		if len(self._buffer) == 0:
			self._buffer.append("Событий за указанный период не происходило. Журнал пуст.")
		
class ServerReportPluginExcludeFile(ServerReportPluginReplaceFile):
	exclude_list = []
	def __init__(self):
		ServerReportPluginReplaceFile.__init__(self)
		
	def _do_buffer(self):
		if ( len(self.exclude_list) == 0 ):
			return

		new_buffer = []
		for line in self._buffer:
			excluded = False
			for exclude_str in self.exclude_list:
				if exclude_str in line:
					excluded = True
			if not excluded:
				new_buffer.append(line)

		self._buffer = new_buffer
