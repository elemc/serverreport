#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ================================= #
# Python script                     #
# Author: Alexei Panov              #
# e-mail: me AT elemc DOT name      #
# ================================= #

import os, os.path
import sys
from sremail import ServerReportEmail
from srplugin import ServerReportPluginBase
from srpluginfile import ServerReportPluginReplaceFile, ServerReportPluginExcludeFile

PLUGIN_DIR="/usr/local/share/serverreport/plugins"
DEBUG_MODE=False

class ServerReportPlugins(object):
    def __init__(self, plugins_dir = PLUGIN_DIR):
        self.plugins = []
        self.plugins_dir = plugins_dir
        self._search()

    def _search(self):
        if not os.path.exists(self.plugins_dir):
            return
        plugin_dir = os.listdir(self.plugins_dir)
        for plugin in plugin_dir:
            plugin_part = plugin.split('.')
            if len(plugin_part) < 2:
                continue

            if plugin_part[1] != 'py':
                continue
            
            if ( DEBUG_MODE ):
                print("Found plugin %s" % plugin )
            self.plugins.append( plugin.split('.')[0] )

    # Iterable
    def __len__(self):
        return len(self.plugins)

    def __getitem__(self, index):
        return self.plugins[index]

    def __iter__(self):
        return self.plugins.__iter__()
        
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage as %s <email@address>" % sys.argv[0])
        os._exit(1)
    mail = ServerReportEmail(sys.argv[1])

    plugins_dir = os.path.expanduser(PLUGIN_DIR)
    if ( DEBUG_MODE ):
        print("Plugins directory is %s" % plugins_dir)
    plugin_files = ServerReportPlugins(plugins_dir)

    sys.path.insert(0, plugins_dir)

    for plugin_file in plugin_files:
        __import__(plugin_file, None, None, [''])

	plugins_loaded = []
	# Load a plugins
	for master_plugin in ServerReportPluginBase.__subclasses__():
		if len( master_plugin.__subclasses__() ) == 0:
			continue
		for plugin in master_plugin.__subclasses__():
			p = plugin()
			msg = p.collect()
			if msg is not None:
				mail.add_content(msg)
			plugins_loaded.append(plugin)
			
			#for plugin in ServerReportPluginReplaceFile.__subclasses__():
			#p = plugin()
			#mail.add_content(p.collect())
			#plugins_loaded.append(plugin)

	# Other plugins from Base
    for plugin in ServerReportPluginBase.__subclasses__():
		if plugin in plugins_loaded:
			continue
		p = plugin()
		msg = p.collect()
		if msg is not None:
			mail.add_content(msg)

    if ( DEBUG_MODE ):
        print("Now message will be sent...")

    mail.send()
