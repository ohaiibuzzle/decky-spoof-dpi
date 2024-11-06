import logging
import subprocess
from typing import Union

from config_file import SpoofDPIConfig
import decky_plugin

import spoofdpi_control


class Plugin:
    SDPI_SUBPROCESS: subprocess.Popen = None

    async def stop(self, manually_triggered=True):
        # SIGTERM the spoofdpi process
        if self.SDPI_SUBPROCESS is not None:
            self.SDPI_SUBPROCESS.kill()
            if manually_triggered:
                await spoofdpi_control.reset_deck_proxy_config()
            self.SDPI_SUBPROCESS = None
        pass

    async def start(self) -> int:
        # Start the spoofdpi process if self.SDPI_PID is None
        if self.SDPI_SUBPROCESS is None:
            self.SDPI_SUBPROCESS = await spoofdpi_control.start_spoofdpi()
            return self.SDPI_SUBPROCESS.pid
        pass

    async def getStatus(self) -> Union[int, None]:
        if self.SDPI_SUBPROCESS is None:
            return None
        return self.SDPI_SUBPROCESS.pid

    async def setSettings(self, dns_server, port, use_doh):
        logging.info("Setting SpoofDPI config to " + dns_server + " " + port + " " + str(use_doh))

        await SpoofDPIConfig.set_setting("dns_server", dns_server)
        await SpoofDPIConfig.set_setting("port", port)
        await SpoofDPIConfig.set_setting("use_doh", use_doh)

        if self.SDPI_SUBPROCESS is not None:
            self.SDPI_SUBPROCESS.kill()
            self.SDPI_SUBPROCESS = None
            await spoofdpi_control.set_deck_proxy_config(port)
            await self.start()

    async def getSettings(self):
        dns_server = await SpoofDPIConfig.get_setting("dns_server")
        port = await SpoofDPIConfig.get_setting("port")
        use_doh = await SpoofDPIConfig.get_setting("use_doh")
        logging.info("Getting SpoofDPI config: " + dns_server + " " + port + " " + str(use_doh))

        return dns_server, port, use_doh

    async def _main(self):
        decky_plugin.logger.info("Decky-SpoofDPI has been loaded!")
        if await SpoofDPIConfig.get_setting("auto_start", False):
            await self.start()

    async def _unload(self):
        decky_plugin.logger.info("Decky-SpoofDPI is being unloaded!")
        await self.stop(manually_triggered=False)
        pass

    async def _uninstall(self):
        decky_plugin.logger.info("Decky-SpoofDPI is being uninstalled!")
        await spoofdpi_control.reset_deck_proxy_config()
        spoofdpi_control.cleanup_spoofdpi(with_config=True)
        pass

    async def _migration(self):
        decky_plugin.logger.info("Decky-SpoofDPI is being migrated!")
        pass
