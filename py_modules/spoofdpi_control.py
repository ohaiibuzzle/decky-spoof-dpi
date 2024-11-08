import os
import subprocess
from typing import Union
from config_file import SpoofDPIConfig
import constants
import decky
import decky_plugin

async def set_deck_proxy_config(port):
    TEMPLATE = """
    "proxyconfig"
    {
        "proxy_mode"        "2"
        "address"           "http://127.0.0.1"
        "port"              "{port}"
        "exclude_local"     "1"
    }"""

    config = TEMPLATE.replace("{port}", str(port))

    with open(constants.DECK_PROXY_PATH, "w") as f:
        f.write(config)

    await decky.emit("decky_spoof_dpi_needs_restart")


async def reset_deck_proxy_config() -> bool:
    await SpoofDPIConfig.set_setting("auto_start", False)

    if os.path.exists(constants.DECK_PROXY_PATH):
        os.remove(constants.DECK_PROXY_PATH)
        await decky.emit("decky_spoof_dpi_needs_restart")
        return True

    return False


async def cleanup_spoofdpi(with_config=False):
    decky_plugin.logger.info("Cleaning up SpoofDPI")
    if os.path.exists(constants.DECK_PROXY_PATH):
        os.remove(constants.DECK_PROXY_PATH)

async def start_spoofdpi() -> Union[subprocess.Popen, None]:
    decky_plugin.logger.info("Starting SpoofDPI")

    dns_server = await SpoofDPIConfig.get_setting("dns_server", "8.8.8.8")
    port = await SpoofDPIConfig.get_setting("port", 9696)
    use_doh = await SpoofDPIConfig.get_setting("use_doh", False)

    if not os.path.exists(constants.DECK_PROXY_PATH):
        decky_plugin.logger.info("Setting up decky proxy config")
        await SpoofDPIConfig.set_setting("auto_start", True)
        await set_deck_proxy_config(port)

    decky_plugin.logger.info("Starting SpoofDPI with dns server " +
                 dns_server + " and port " + str(port) + " and use_doh " + str(use_doh))

    sdpi_subprocess = subprocess.Popen([constants.SPOOF_DPI_PATH, "-silent=true", f"-dns-addr={dns_server}",
                                        f"-port={port}", f"-enable-doh={use_doh}"])
    pid = sdpi_subprocess.pid

    decky_plugin.logger.info(f"Started SpoofDPI with pid {pid}")

    return sdpi_subprocess
