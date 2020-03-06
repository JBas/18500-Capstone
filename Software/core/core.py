"""OctoPlus System Core

This program implements the system core for OctoPlus, a 3D printing
error detection system.
@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       2/27/202

"""
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
#from lib import CheckThread

class CorePlugin(octoprint.plugin.StartupPlugin,
                 octoprint.plugin.ShutdownPlugin):
    def __init__(self):
        self.name    = "System Core"
        self.descr   = "Interface between OctoPrint and the rest of the computer vision"
        self.author  = "Joshua Bas, jnbas@andrew.cmu.edu, joshua.n.bas@gmail.com"
        self.url     = "https://github.com/JBas/18500-Capstone"
        self.layer = 0
        self.tlist = []
        pass

    def on_after_startup(self):
        self._logger.info("Started up!")
        pass

    def on_shutdown(self):
        self._logger.info("Shutting down!")
        pass
"""    
    def handle_gcode_sent(comm_instance,
                             phase,
                             cmd,
                             cmd_type,
                             gcode,
                             *args,
                             **kwargs):
        if gcode and gcode is "G0":
            self._logger.info("Sent a Z-axis change command!")
            self.layer += 1
            for i in range(len(self.tlist), -1):
                t = self.tlist[i]
                if (t.isAlive()):
                    t.incrCycles()
                else:
                    # do something with t.hasError
                    self.tlist.pop(i)
            t = CheckThread()
            t.start()
            self.tlist.append(t)


        return
"""


plugin = CorePlugin()

__plugin_implementation__       = plugin
__plugin__name__                = plugin.name
__plugin__description__         = plugin.descr
__plugin__author__              = plugin.author
__plugin__url__                 = plugin.url
"""    
    __plugin_hooks__          = {
        "octoprint.comm.protocol.gcode.sent": plugin.handle_gcode_queuing
    }
    pass
"""
