import os

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code one directory up
# or add the `decky-loader/plugin` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky_plugin

import py_modules.constants as constants
import py_modules.spoofdpi_control as spoofdpi_control


class Plugin:
    SDPI_PID = None
    async def stop(self):
        # SIGTERM the spoofdpi process
        if self.SDPI_PID is not None:
            os.kill(self.SDPI_PID, 15)
        pass

    async def start(self):
        # Start the spoofdpi process if self.SDPI_PID is None
        if self.SDPI_PID is None:
            spoofdpi_control.start_spoofdpi()
        pass

    async def getConfig(self):
        curr_config = spoofdpi_control.SpoofDPIConfig.load()
        return curr_config.dns_server, curr_config.use_doh, curr_config.port
    
    async def setConfig(self, dns_server, use_doh, port):
        spoofdpi_control.SpoofDPIConfig.save({
            "dns_server": dns_server,
            "use_doh": use_doh,
            "port": port
        })
        await self.stop()
        await self.start()
        pass

    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        decky_plugin.logger.info("Decky-SpoofDPI has been loaded!")
        spoofdpi_control.get_spoofdpi()


    # Function called first during the unload process, utilize this to handle your plugin being stopped, but not
    # completely removed
    async def _unload(self):
        decky_plugin.logger.info("Decky-SpoofDPI is being unloaded!")
        await Plugin.stop()
        pass

    # Function called after `_unload` during uninstall, utilize this to clean up processes and other remnants of your
    # plugin that may remain on the system
    async def _uninstall(self):
        decky_plugin.logger.info("Decky-SpoofDPI is being uninstalled!")
        spoofdpi_control.cleanup_spoofdpi(with_config=True)
        pass

    # Migrations that should be performed before entering `_main()`.
    async def _migration(self):
        decky_plugin.logger.info("Decky-SpoofDPI is being migrated!")
        await spoofdpi_control.get_spoofdpi()
        pass
