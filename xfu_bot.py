#!/usr/bin/env python3.7
"""Xiaomi Helper Bot"""

import json
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async
from modules import gsmarena, mi_vendor_updater as mi_vendor,\
    xiaomi_firmware_updater as mi_firmware, xiaomi_oss as mi_oss, xiaomi_info as info,\
    miui_updates_tracker as miui, xiaomi_eu
# from telegram.ext import MessageHandler, Filters

# read bog config
with open('config.json', 'r') as f:
    CONFIG = json.load(f)
TOKEN = CONFIG['tg_bot_token']

# set logging
logging.basicConfig(filename='current.log',
                    filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

IS_ADMIN = True
IS_MORE = True
try:
    from admin import admin
except ImportError:
    print("Can't find admin module, skipping it")
    IS_ADMIN = False
try:
    from private import private
except ImportError:
    print("Can't find private commands module, skipping it")
    IS_MORE = False


@run_async
def start(update, context):
    """start command"""
    message = "Hello {}! \nI'm Uranus, an all-in-one bot for Xiaomi users!\n" \
              "I can get you latest Official ROMs, Firmware updates links," \
              " and many more things!\nCheck how to use me by clicking /help" \
              "\n Join @XiaomiGeeks to get all updates and announcements about the bot!"\
        .format(update.message.from_user.first_name)
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown')


@run_async
def recovery(update, context):
    """reply with latest available recovery ROMs"""
    if not context.args:
        message = '*Usage: * `/recovery device`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = miui.fetch_recovery(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong recovery ROM request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def fastboot(update, context):
    """reply with latest available fastboot ROMs"""
    if not context.args:
        message = '*Usage: * `/fastboot device`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = miui.fetch_fastboot(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong fastboot ROM request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def firmware(update, context):
    """generate firmware link on website"""
    if not context.args:
        message = '*Usage: * `/firmware device`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = mi_firmware.gen_fw_link(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong firmware request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def latest(update, context):
    """reply with latest available ROMs version"""
    if not context.args:
        message = '*Usage: * `/latest device`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = miui.check_latest(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong latest info request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def oss(update, context):
    """reply with latest available OSS kernel links"""
    if not context.args:
        message = '*Usage: * `/oss device`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = mi_oss.oss(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong oss info request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def history(update, context):
    """reply with latest available OSS kernel links"""
    if not context.args:
        message = '*Usage: * `/list device`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower().split('_')[0]
    message, status = mi_firmware.history(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong list history request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def models(update, context):
    """reply with latest available OSS kernel links"""
    if not context.args:
        message = '*Usage: * `/models codename`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower().split('_')[0]
    message, status = info.check_models(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong list models request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def whatis(update, context):
    """reply with device name"""
    if not context.args:
        message = '*Usage: * `/whatis codename`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = info.whatis(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong whatis request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def codename(update, context):
    """reply with device codename"""
    if not context.args:
        message = '*Usage: * `/codename device`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = ' '.join(context.args).lower()
    message, status = info.get_codename(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong codename request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def specs(update, context):
    """reply with device's specs"""
    if not context.args:
        message = '*Usage: * `/specs codename`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower().split('_')[0]
    message, status = gsmarena.specs(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong specs request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='no')


@run_async
def vendor(update, context):
    """reply with latest fw+vendor links"""
    if not context.args:
        message = '*Usage: * `/vendor codename`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = mi_vendor.fetch_vendor(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong vendor request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def eu(update, context):
    """reply with latest Xiaomi.eu links"""
    if not context.args:
        message = '*Usage: * `/eu codename`\n' \
                  'Check how to use the bot with examples /help'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = xiaomi_eu.xiaomi_eu(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.info("wrong vendor request: %s", update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def usage(update, context):
    """Help - How to use the bot"""
    message = "Available commands with examples:\n" \
              "[Check here](https://xiaomifirmwareupdater.com/projects/uranus-chatbot/#usage)"
    update.message.reply_text(message, parse_mode='Markdown',
                              reply_to_message_id=update.message.message_id)


def error(update, context):
    """Log Errors caused by Updates."""
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


def unknown(update, context):
    """Reply to unknown commands"""
    context.bot.send_message(chat_id=update.message.chat_id,
                             reply_to_message_id=update.message.message_id,
                             text="Sorry, I didn't understand that command.")


def main():
    """
    main function
    :return: null
    """
    # Updater continuously fetches new updates from telegram and passes them on to the Dispatcher
    updater = Updater(token=TOKEN, workers=1, use_context=True)
    dispatcher = updater.dispatcher
    # This class dispatches all kinds of updates to its registered handlers.

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    dispatcher.add_error_handler(error)

    help_handler = CommandHandler("help", usage)
    dispatcher.add_handler(help_handler)

    recovery_handler = CommandHandler('recovery', recovery)
    dispatcher.add_handler(recovery_handler)

    fastboot_handler = CommandHandler('fastboot', fastboot)
    dispatcher.add_handler(fastboot_handler)

    firmware_handler = CommandHandler('firmware', firmware)
    dispatcher.add_handler(firmware_handler)

    latest_handler = CommandHandler('latest', latest)
    dispatcher.add_handler(latest_handler)

    oss_handler = CommandHandler('oss', oss)
    dispatcher.add_handler(oss_handler)

    history_handler = CommandHandler('list', history)
    dispatcher.add_handler(history_handler)

    models_handler = CommandHandler('models', models)
    dispatcher.add_handler(models_handler)

    whatis_handler = CommandHandler('whatis', whatis)
    dispatcher.add_handler(whatis_handler)

    codename_handler = CommandHandler('codename', codename)
    dispatcher.add_handler(codename_handler)

    specs_handler = CommandHandler('specs', specs)
    dispatcher.add_handler(specs_handler)

    vendor_handler = CommandHandler('vendor', vendor)
    dispatcher.add_handler(vendor_handler)

    eu_handler = CommandHandler('eu', eu)
    dispatcher.add_handler(eu_handler)

    if IS_ADMIN:  # load admin commands if module is found
        admin.main(dispatcher)
    if IS_MORE:  # load private commands if module is found
        private.main(dispatcher)

    # unknown_handler = MessageHandler(Filters.command, unknown)
    # dispatcher.add_handler(unknown_handler)

    updater.start_polling()  # start the bot

    updater.idle()


if __name__ == '__main__':
    main()
