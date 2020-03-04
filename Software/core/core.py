"""OctoPlus System Core

This program implements the system core for OctoPlus, a 3D printing
error detection system.
@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       2/27/202

"""
from __future__ import absolute_import

import octoprint.plugin
import logging
#import numpy as np
#import threading
#import lib

MAX_ERROR_CHECK = 5
"""
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
class CorePlugin(octoprint.plugin.StartupPlugin,
                 octroprint.plugin.ShutdownPlugin):

    name    = "System Core"
    descr   = "Interface between OctoPrint and the rest of the computer vision"
    author  = "Joshua Bas, jnbas@andrew.cmu.edu, joshua.n.bas@gmail.com"
    url     = "https://github.com/JBas/18500-Capstone"
    tlist = []

    def __init__(self):
        pass

    def on_after_startup():
        self.__logger.info("Started up!")
        #self.rpc
        pass

    def on_shutdown():
        self.__logger.info("Shutting down!")
        pass

    def handle_gcode_queuing(comm_instance,
                             phase,
                             cmd,
                             cmd_type,
                             gcode,
                             *args,
                             **kwargs):
        if gcode and gcode is "G0":
            logging.getLogger(__name__).info("Queuing a Z-axis command!")
            #for i in range(len(self.tlist), -1):
            #    self.tlist[i].incrCycles()
            #    if tlist[i].getCycles() > MAX_ERROR_CHECK:
            #        # any errors on this thread's layer
            #        # should have been caught
            #        self.tlist.pop(i)

            #t = Thread(target=self.check,
            #           name = "check",
            #           args = ())
            #self.tlist.append(t)

        return


def __plugin_load__():
    plugin = CorePlugin()

    global __plugin__implementation__
    global __plugin__hooks__
    global __plugin__name__
    global __plugin__description__
    global __plugin__author__
    global __plugin__url__

    __plugin_implementation__       = plugin
    __plugin__name__                = plugin.name
    __plugin__description__         = plugin.descr
    __plugin__author__              = plugin.author
    __plugin__url__                 = plugin.url

    __plugin_hooks__          = {
        "octoprint.comm.protocol.gcode.queuing": plugin.handle_gcode_queuing
    }
    pass




















"""
def main(gcode):
    # user submits g-code
    # system created g-code model

    system = System()
    system.createRPC(gcode)
    
    # ultimaker begins print job
    system.startPrint()

    while (system.status() is "printing"):
        # collect image data from camera
        
        if (interrupted or timer):
            disp = ?
            # assign weights to model disparities
            weighted = weights*disp

            # sum weighted disparities
            total_error = np.sum(weighted)

            # pass weighted disparities through activation func
            decision = activate(total_error)
            if (decision == some_error_label):
                system.notify()
                system.stop()
            
            system.update()

    return -1
"""
