"""Data Provider class"""
import asyncio

from uranus_bot import LOGGER
from uranus_bot.providers.custom_recovery.twrp.twrp import load_twrp_data


class Provider:
    """Provides data that needs to be refreshed"""
    def __init__(self, _loop):
        self.loop = _loop
        self.twrp_data = {}
        self.loop.create_task(self.twrp_data_loop())

    async def twrp_data_loop(self):
        """
        loop devices' twrp_data info every six hours
        """
        while True:
            LOGGER.info("Refetching twrp data")
            self.twrp_data = await load_twrp_data()
            await asyncio.sleep(60 * 60 * 6)
