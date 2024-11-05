import constants
import json
import os

from settings import SettingsManager
# Get environment variable
settingsDir = os.environ["DECKY_PLUGIN_SETTINGS_DIR"]


class SpoofDPIConfig:
    @staticmethod
    def get() -> SettingsManager:
        return SettingsManager(settingsDir, "spoofdpi.json")

    @staticmethod
    async def set_setting(key: str, value) -> None:
        SpoofDPIConfig.get().setSetting(key, value)

    @staticmethod
    async def get_setting(key: str, defaults=None):
        return SpoofDPIConfig.get().getSetting(key, defaults)
