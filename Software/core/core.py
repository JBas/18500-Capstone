"""OctoPlus System Core

This program implements the system core for OctoPlus, a 3D printing
error detection system.
@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       2/27/202

"""
import octoprint.plugin
import numpy as np
import lib

__plugin_name__           = "System Core"
__plugin_description__    = "Interface between OctoPrint and the rest of the computer vision"
__plugin_author__         = "Joshua Bas, jnbas@andrew.cmu.edu, joshua.n.bas@gmail.com"
__plugin_url__            = "https://github.com/JBas/18500-Capstone"
__plugin_hooks__          = {
    "octoprint.comm.protocol.gcode.sent": handle_gcode_sent
}

def __plugin_check__():
    try:

    except:
        return False
    return True


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
