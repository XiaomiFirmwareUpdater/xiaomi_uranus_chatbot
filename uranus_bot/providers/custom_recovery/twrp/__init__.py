""" TWRP data provider """

from uranus_bot.providers.custom_recovery.twrp.twrp import twrp_data_loop
from uranus_bot.telegram_bot.tg_bot import BOT

BOT.loop.create_task(twrp_data_loop())
