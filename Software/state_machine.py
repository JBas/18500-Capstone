"""OctoPlus State Machine

This program implements the system state machine for OctoPlus, a 3D printing
error detection system.
@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       2/27/202

"""

import numpy as np
from lib.py import *

def main():
    # user submits g-code
    # user sets initials params
    # system created g-code model
    # ultimaker begins print job

    while system.printing():
        # collect x, y, z, t datat from lasers
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
