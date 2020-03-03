"""OctoPlus System Core

This program implements the system core for OctoPlus, a 3D printing
error detection system.
@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       2/27/202

"""
import octoprint.plugin
import logging
import numpy as np

class CorePlugin(octoprint.plugin.StartupPlugin,
                 octroprint.plugin.ShutdownPlugin):

    def __init__(self):
        pass

    def handle_gcode_queuing(comm_instance,
                             phase,
                             cmd,
                             cmd_type,
                             gcode,
                             *args,
                             **kwargs):
        if gcode in ("some command"):
            logging.getLogger(__name__).info("Queuing a ___ command!")

        return

__plugin_name__           = "System Core"
__plugin_description__    = "Interface between OctoPrint and the rest of the computer vision"
__plugin_author__         = "Joshua Bas, jnbas@andrew.cmu.edu, joshua.n.bas@gmail.com"
__plugin_url__            = "https://github.com/JBas/18500-Capstone"

def __plugin_load__():
    plugin = CorePlugin()

    global __plugin__implementation__
    global __plugin__hooks__

    __plugin_implementation__ = plugin 

    __plugin_hooks__          = {
        "octoprint.comm.protocol.gcode.sent": plugin.handle_gcode_sent,
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
