import os
import subprocess
import sys
import json
import gzip
import tarfile
from typing import List, Union
from config_file import SpoofDPIConfig
import constants
import logging
import decky

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
    logging.info("Cleaning up SpoofDPI")
    if os.path.exists(constants.DECK_PROXY_PATH):
        os.remove(constants.DECK_PROXY_PATH)

async def start_spoofdpi() -> Union[subprocess.Popen, None]:
    logging.info("Starting SpoofDPI")

    if not os.path.exists(constants.DECK_PROXY_PATH):
        logging.info("Setting up decky proxy config")
        await SpoofDPIConfig.set_setting("auto_start", True)
        await set_deck_proxy_config(await SpoofDPIConfig.get_setting("port", 9696))

    logging.info("Starting SpoofDPI with dns server " +
                 await SpoofDPIConfig.get_setting("dns_server", '8.8.8.8') + " and port " + str(await SpoofDPIConfig.get_setting("port", 9696)))

    sdpi_subprocess = subprocess.Popen([constants.SPOOF_DPI_PATH, "-silent=true", f"-dns-addr={await SpoofDPIConfig.get_setting('dns_server', '8.8.8.8')}",
                                        f"-port={str(await SpoofDPIConfig.get_setting('port', 9696))}", f"-enable-doh={str(await SpoofDPIConfig.get_setting('use_doh', False))}"])
    pid = sdpi_subprocess.pid

    logging.info(f"Started SpoofDPI with pid {pid}")

    return sdpi_subprocess
