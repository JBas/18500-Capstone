# coding=utf-8
"""OctoPlus System Core

This program implements the system core for OctoPlus, a 3D printing
error detection system.
@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       2/27/202

"""

from __future__ import absolute_import
import octoprint.plugin
from edge import edgeDetect, edgeError

class OctoplusPlugin(octoprint.plugin.StartupPlugin,
                     octoprint.plugin.SettingsPlugin,
                     #octoprint.plugin.AssetPlugin,
                     octoprint.plugin.TemplatePlugin,
                     octoprint.plugin.ShutdownPlugin):

    def __init__(self):
        self.layer = 0
        self.rpi_cam = None
        self.uart_cam = None
        pass

    ##~~ StartupPlugin mixin

    def on_after_startup(self):
        HSV = self._settings.get(["params", "HSV"])
        HSV_tolerance = self._settings.get(["params", "HSV_tolerance"])
        edge_sigma = self._settings.get_int(["params", "edge_sigma"])
        weights = self._settings.get(["params", "weights"])

        self._logger.info("Started up!")
        self._logger.info("HSV: {HSV}, HSV_tolerance: {HSV_tolerance}, edge_sigma: {edge_sigma}, weights: {weights}".format(**locals()))
        pass

	##~~ SettingsPlugin mixin
    
    def get_settings_defaults(self):
        return dict(
            params=dict(
                HSV=(60.0, 0.021, 0.549),
                HSV_tolerance=0.10,
                edge_sigma=3,
                weights=[1]
            ),
            url="https://en.wikipedia.org/wiki/Hello_world"
        )
    
    def on_settings_save(self, data):
        old_url = self._settings.get(["url"])
        old_HSV = self._settings.get(["params", "HSV"])

        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        url = self._settings.get(["url"])
        HSV = self._settings.get(["params", "HSV"])

        if (url != old_url) or (HSV != old_HSV):
            self._logger.info("old url: {old_url}, old HSV: {old_HSV}, new url: {url}, new HSV: {HSV}".format(**locals()))
        else:
            self._logger.info("nothing changed!")
        pass

	##~~ TemplatePlugin mixin

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

	##~~ AssetPlugin mixin

#	def get_assets(self):
#		# Define your plugin's asset files to automatically include in the
#		# core UI here.
#		return dict(
#			js=["js/OctoPlus.js"],
#			css=["css/OctoPlus.css"],
#			less=["less/OctoPlus.less"]
#		)
    
    ##~~ ShudownPlugin mixin

    def on_shutdown(self):
        self._logger.info("Shutting down!")
        pass

	##~~ Softwareupdate hook

#    def get_update_information(self):
#		# Define the configuration for your plugin to use with the Software Update
#		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
#		# for details.
#        return dict(
#        OctoPlus=dict(
#				displayName="Octoplus Plugin",
#				displayVersion=self._plugin_version,
#
#				# version check: github repository
#				type="github_release",
#				user="JBas",
#				repo="OctoPrint-Octoplus#",
#				current=self._plugin_version,
#
#				# update method: pip
#				pip="https://github.com/JBas/OctoPrint-Octoplus/archive/{target_version}.zip"
#			)
#		)

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

    def run(self):
        hasError = False

        #I1 = lib.getRPIArray(self.rpi_cam)
        #e1 = edgeDetect(I1, self.params)

        #err = edgeError(e1, self.edge_ref, self.params)

        #hasError = activate([err], [1], self.params["weights"])

        return hasError

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Octoplus Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = OctoplusPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		#"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.gcode.sent": __plugin_implementation__.handle_gcode_sent
	}
