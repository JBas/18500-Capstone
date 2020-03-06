"""OctoPlus System Core

This program implements the system core for OctoPlus, a 3D printing
error detection system.
@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       2/27/202

"""
from __future__ import absolute_import, unicode_literals

import octoprint.plugin
import threading
#import lib
"""
MAX_ERROR_CHECK = 5
class CheckThread(threading.Thread):
    def __init__(self, rpc, layer, group=None, target=None, name="check",
                 args=(), kwargs=None, verbose=None):
        self.cycles = 0
        self.rpc = rpc
        self.layer = layer
        threading.Thread.__init__(self, group=group, tagert=target,
                                  name=name, args=args, kwargs=kwargs,
                                  verbose=verbose)
        pass

    def incrCycle(self):
        self.cycles += 1
        pass

    def run(self):
        I1 = lib.getI1()
        #I2 = lib.getI2()

        #ppc = PPC(I1, I2)
        #ppc.generate()
        #ppc_result = ppc.analyze(self.rpc, self.layer)

        #edge_result = _____()

        #do something... 
        pass
"""

def worker():
    print("Worker")
    return


class CorePlugin(octoprint.plugin.StartupPlugin,
                 octoprint.plugin.ShutdownPlugin):

#    tlist = []

    def __init__(self):
        self.name    = "System Core"
        self.descr   = "Interface between OctoPrint and the rest of the computer vision"
        self.author  = "Joshua Bas, jnbas@andrew.cmu.edu, joshua.n.bas@gmail.com"
        self.url     = "https://github.com/JBas/18500-Capstone"
        self.layer = 0
        pass

    def on_after_startup(self):
        self.__logger.info("Started up!")
        t = threading.Thread(target=worker)
        t.start()
        pass

    def on_shutdown(self):
        self.__logger.info("Shutting down!")
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
            self.__logger.info("Sent a Z-axis change command!")

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
