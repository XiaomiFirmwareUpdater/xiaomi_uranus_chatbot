"""Data Provider class"""
import asyncio

from uranus_bot import LOGGER
from uranus_bot.providers.custom_recovery.twrp.twrp import load_twrp_data
from uranus_bot.providers.devices_info.info import load_firmware_codenames,\
    load_vendor_codenames, load_devices_names, load_miui_codenames, load_models


class Provider:
    """Provides data that needs to be refreshed"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, _loop):
        self.loop = _loop
        self.twrp_data = {}
        self.firmware_codenames = []
        self.miui_codenames = []
        self.vendor_codenames = []
        self.codenames_names = {}
        self.names_codenames = {}
        self.models_data = {}
        self.loop.create_task(self.twrp_data_loop())
        self.loop.create_task(self.firmware_codenames_loop())
        self.loop.create_task(self.miui_codenames_loop())
        self.loop.create_task(self.vendor_codenames_loop())
        self.loop.create_task(self.devices_names_loop())
        self.loop.create_task(self.models_loop())

    async def twrp_data_loop(self):
        """
        loop devices' twrp_data info every six hours
        """
        while True:
            LOGGER.info("Refreshing twrp data")
            self.twrp_data = await load_twrp_data()
            await asyncio.sleep(60 * 60 * 6)

    async def firmware_codenames_loop(self):
        """
        loop devices' firmware codenames every six hours
        """
        while True:
            LOGGER.info("Refreshing firmware codenames")
            self.firmware_codenames = await load_firmware_codenames()
            await asyncio.sleep(60 * 60 * 6)

    async def miui_codenames_loop(self):
        """
        loop devices' miui codenames every six hours
        """
        while True:
            LOGGER.info("Refreshing miui codenames")
            self.miui_codenames = await load_miui_codenames()
            await asyncio.sleep(60 * 60 * 6)

    async def vendor_codenames_loop(self):
        """
        loop devices' vendor codenames every six hours
        """
        while True:
            LOGGER.info("Refreshing vendor codenames")
            self.vendor_codenames = await load_vendor_codenames()
            await asyncio.sleep(60 * 60 * 6)

    async def devices_names_loop(self):
        """
        loop devices' codenames and names every six hours
        """
        while True:
            LOGGER.info("Refreshing devices codenames and names")
            self.codenames_names, self.names_codenames = await load_devices_names()
            await asyncio.sleep(60 * 60 * 6)

    async def models_loop(self):
        """
        loop devices' models every six hours
        """
        while True:
            LOGGER.info("Refreshing models data")
            self.models_data = await load_models()
            await asyncio.sleep(60 * 60 * 6)
