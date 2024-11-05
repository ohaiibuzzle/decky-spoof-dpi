import os 

# We install to $HOME/.local/bin/spoofdpi for ease of use.
SPOOF_DPI_PATH = os.path.join(os.path.expanduser("~"), ".local/bin/spoofdpi")
# Use ~/.config/decky-spoofdpi.json for config
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".config", "decky-spoofdpi.json")
SPOOFDPI_BINARY = "https://github.com/xvzc/SpoofDPI/releases/download/v0.12.0/spoofdpi-linux-amd64.tar.gz"