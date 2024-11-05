import os 
import sys
import json
import requests
import gzip
import tarfile
import constants


class SpoofDPIConfig:
    dns_server = "8.8.8.8"
    use_doh = False
    port = 9696

    def __init__(self):
        pass

    @staticmethod
    def load():
        with open(constants.CONFIG_PATH, "r") as f:
            config = SpoofDPIConfig()
            loaded_json = json.load(f)
            config.dns_server = loaded_json["dns_server"]
            config.use_doh = loaded_json["use_doh"]
            config.port = loaded_json["port"]
            return config
        
    @staticmethod
    def save(config):
        with open(constants.CONFIG_PATH, "w") as f:
            json.dump(config, f)

async def get_spoofdpi():
    if not os.path.exists(constants.SPOOF_DPI_PATH):
        # spoof-dpi is a tar gz file, we need to extract it
        response = requests.get(constants.SPOOFDPI_BINARY)
        ungzipped = gzip.GzipFile(fileobj=response.raw)
        tar = tarfile.open(fileobj=ungzipped)
        tar.extractall(path=os.path.dirname(constants.SPOOF_DPI_PATH))
        tar.close()
        os.chmod(constants.SPOOF_DPI_PATH, 0o755)

async def cleanup_spoofdpi(with_config=False):
    if os.path.exists(constants.SPOOF_DPI_PATH):
        os.remove(constants.SPOOF_DPI_PATH)

    if os.path.exists(constants.CONFIG_PATH) and with_config:
        os.remove(constants.CONFIG_PATH)

async def start_spoofdpi() -> int:
    if not os.path.exists(constants.SPOOF_DPI_PATH):
        await get_spoofdpi()

    config = SpoofDPIConfig.load()

    # command line: spoofdpi -silent true -dns-addr <DNS_SERVER> -port <PORT> -enable-doh <true|false>
    pid  = os.spawnlp(os.P_NOWAIT, constants.SPOOF_DPI_PATH, constants.SPOOF_DPI_PATH, "-silent", "true", "-dns-addr", config.dns_server, "-port", str(config.port), "-enable-doh", str(config.use_doh))
    return pid