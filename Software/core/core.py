"""OctoPlus System Core

This program implements the system core for OctoPlus, a 3D printing
error detection system.
@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       2/27/202

"""
from __future__ import absolute_import, unicode_literals

import octoprint.plugin

class CorePlugin(octoprint.plugin.StartupPlugin,
                 octoprint.plugin.ShutdownPlugin):
    def __init__(self):
        self.name    = "System Core"
        self.descr   = "Interface between OctoPrint and the rest of the computer vision algorithms"
        self.author  = "Joshua Bas (jnbas@andrew.cmu.edu)"
        self.url     = "https://github.com/JBas/18500-Capstone"
        self.params = {
            "HSV": (60.0, 0.021, 0.549),
            "HSV_tolerance": 0.10,
            "layer": 0,
            "edge_sigma": 3,
            "weights": [1]
        }
        self.rpi_cam = None
        self.uart_cam = None
        pass

    def on_after_startup(self):
        self._logger.info("Started up!")
        pass

    def on_shutdown(self):
        self._logger.info("Shutting down!")
        pass

    # handler for when a command is sent to
    # the printer
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

            hasError = self.run()
            # do something with hasError

        return

    def run(self) -> bool:
        hasError = False

        #I1 = lib.getRPIArray(self.rpi_cam)
        #e1 = edgeDetect(I1, self.params)

        #err = edgeError(e1, self.edge_ref, self.params)

        #hasError = activate([err], [1], self.params["weights"])

        return hasError

plugin = CorePlugin()

__plugin_implementation__       = plugin
__plugin__name__                = plugin.name
__plugin__description__         = plugin.descr
__plugin__author__              = plugin.author
__plugin__url__                 = plugin.url
"""    
    __plugin_hooks__          = {
        "octoprint.comm.protocol.gcode.sent": plugin.handle_gcode_sent
    }
    pass
"""
