#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ================================= #
# Python script                     #
# Author: Alexei Panov              #
# e-mail: me AT elemc DOT name      #
# ================================= #

from srplugin import ServerReportPluginReplaceFile

class LoginsPlugin(ServerReportPluginReplaceFile):
	filename_for_report = "/Users/alex/workspace/temp/secure"
	dict_of_replace = {
		'Accepted password for':		'Выполнен удаленный вход под пользователем',
		'Failed password for':			'Неправильный пароль для пользователя',
		'session opened for user':		'смена привилегий на пользователя',
		'sudo:':						'выполнена команда с повышенными привелегиями:',
		'new group':					'Создана новая группа',
		'new user':						'Создан новый пользователь',
		'from':							'от',
		'port':							'порт',
		'by':							'для',
		'name':							'наименование',
		}
	def __init__(self):
		ServerReportPluginReplaceFile.__init__(self)
