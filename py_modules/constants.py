import os
import decky_plugin

# We install to $HOME/.local/bin/spoofdpi for ease of use.
SPOOF_DPI_PATH = f"{decky_plugin.DECKY_PLUGIN_DIR}/bin/spoof-dpi"
# Use ~/.config/decky-spoofdpi.json for config
CONFIG_PATH = os.path.join(os.path.expanduser(
    "~"), ".config", "decky-spoofdpi.json")
DECK_PROXY_PATH = os.path.join(
    os.path.expanduser("~"), ".steam/steam/config/proxyconfig.vdf")
SPOOFDPI_BINARY = "https://github.com/xvzc/SpoofDPI/releases/download/v0.12.0/spoofdpi-linux-amd64.tar.gz"
