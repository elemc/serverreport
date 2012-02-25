#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ================================= #
# Python script                     #
# Author: Alexei Panov              #
# e-mail: me AT elemc DOT name      #
# ================================= #

from srplugin import ServerReportPluginBase
import os, os.path

class ServerReportPluginDir(ServerReportPluginBase):

	dest_dir			= None
	exclude_word_list	= []
	
	def __init__(self):
		ServerReportPluginBase.__init__(self)
		self._buffer = {}
		self._init_plugin()

	def __del__(self):
		self._buffer.clear()

	def _do_dir(self, dir):
		if not os.path.exist(dir):
			return

		for f in os.listdir(dir):
			full_f = os.path.join(dir, f)
			if os.path.isdir(full_f):
				self._do_dir(full_f)
			else:
				self._do_file(full_f)
				
	def _do_file(self, f):
		fp = open(f, 'r')

		buf = []
		for l in fp:
			founded = 0
			for exclude_word in self.exclude_word:
				if exclude_word in l:
					founded += 1
			if founded == 0:
				buf.append(l.strip())
				
		self._buffer[f] = buf
		fp.close()

	def _init_plugin(self):
		if self.dest_dir is None:
			return

		self._do_dir(self.dest_dir)

	def _do_body(self):
		if self._buffer is None:
			return str()

		body = []
		for key in self._buffer.keys():
			body.append("=== %s ===" % key)
			for l in self._buffer[key]:
				body.append(l)
			body.append("=== END ===")
			body.append("\n")

	def collect(self):
		if self.dest_dir is None:
			return None
		msg_body = self._do_body()
		msg = MIMEText("Отчет по каталогу %s\n\n%s" % (self.dest_dir, str('\n').join(msg_body) ))
		return msg
