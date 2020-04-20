"""OctoPlus System Core

This program implements the system core for OctoPlus, a 3D printing
error detection system.
@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       2/27/202

"""
from __future__ import absolute_import, unicode_literals

import octoprint.plugin

class CorePlugin(octoprint.plugin.StartupPlugin,
                 octoprint.plugin.SettingsPlugin,
                 octoprint.plugin.ShutdownPlugin):
    def __init__(self):
        self.name    = "System Core"
        self.descr   = "Interface between OctoPrint and the rest of the computer vision algorithms"
        self.author  = "Joshua Bas (jnbas@andrew.cmu.edu)"
        self.url     = "https://github.com/JBas/18500-Capstone"
        self.params = {
            "HSV": (60.0, 0.021, 0.549),
            "HSV_tolerance": 0.10,
            "edge_sigma": 3,
            "weights": [1]
        }
        self.layer = 0
        self.rpi_cam = None
        self.uart_cam = None
        pass

    def get_settings_defaults(self):
        return dict(
            params=dict()
                "HSV": (60.0, 0.021, 0.549),
                "HSV_tolerance": 0.10,
                "edge_sigma": 3,
                "weights": [1]
            )

    def on_after_startup(self):
        HSV = self._settings.get(["params", "HSV"])
        HSV_tolerance = self._settings.get(["params", "HSV_tolerance"])
        egde_sigma = self._settings.get_int(["params", "edge_sigma"])
        weights = self._settings.get(["params", "weights"])

        self._logger.info("Started up!")
        self._logger.info("HSV: {HSV},
                           HSV_tolerance: {HSV_tolerance},
                           edge_sigma: {edge_sigma},
                           weights: {weights}".format(**locals()))
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
