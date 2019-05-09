#!/usr/bin/env python3.7
"""Xiaomi Helper Bot"""

import json
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
import modules.functions as xfu
# from telegram.ext import MessageHandler, Filters

IS_ADMIN = True
try:
    import admin.admin as admin
except ImportError:
    print("Can't find admin module, skipping it")
    IS_ADMIN = False

# read bog config
with open('config.json', 'r') as f:
    CONFIG = json.load(f)
TOKEN = CONFIG['tg_bot_token']

# set logging
logging.basicConfig(filename='current.log',
                    filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def start(update, context):
    """start command"""
    message = "Hey! I'm Uranus, an all-in-one bot for Xiaomi users!\n" \
              "I can get you latest Official ROMs, Firmware updates links," \
              " and many more things!\nCheck how to use me by clicking /help" \
              "\n Join @XiaomiGeeks to get all updates and announcements about the bot!"
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown')


def recovery(update, context):
    """reply with latest available recovery ROMs"""
    if len(context.args) < 1:
        message = '*Usage: * `/recovery device`'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = xfu.fetch_recovery(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.warning("@%s requested wrong recovery ROM: %s",
                       update.effective_user.username, update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')
    LOGGER.info("@%s requested recovery ROM: %s",
                update.effective_user.username, update.message.text)


def fastboot(update, context):
    """reply with latest available fastboot ROMs"""
    if len(context.args) < 1:
        message = '*Usage: * `/fastboot device`'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = xfu.fetch_fastboot(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.warning("@%s requested wrong fastboot ROM: %s",
                       update.effective_user.username, update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')
    LOGGER.info("@%s requested fastboot ROM: %s",
                update.effective_user.username, update.message.text)


def firmware(update, context):
    """generate firmware link on website"""
    if len(context.args) < 1:
        message = '*Usage: * `/firmware device`'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = xfu.gen_fw_link(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.warning("@%s requested wrong firmware: %s",
                       update.effective_user.username, update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')
    LOGGER.info("@%s requested firmware: %s",
                update.effective_user.username, update.message.text)


def latest(update, context):
    """reply with latest available ROMs version"""
    if len(context.args) < 1:
        message = '*Usage: * `/latest device`'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = xfu.check_latest(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.warning("@%s requested wrong latest info: %s",
                       update.effective_user.username, update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')
    LOGGER.info("@%s requested latest info: %s",
                update.effective_user.username, update.message.text)


def oss(update, context):
    """reply with latest available OSS kernel links"""
    if len(context.args) < 1:
        message = '*Usage: * `/oss device`'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower()
    message, status = xfu.oss(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.warning("@%s requested wrong oss info: %s",
                       update.effective_user.username, update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')
    LOGGER.info("@%s requested oss info: %s",
                update.effective_user.username, update.message.text)


def history(update, context):
    """reply with latest available OSS kernel links"""
    if len(context.args) < 1:
        message = '*Usage: * `/list device`'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower().split('_')[0]
    message, status = xfu.history(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.warning("@%s requested wrong oss info: %s",
                       update.effective_user.username, update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')
    LOGGER.info("@%s requested oss info: %s",
                update.effective_user.username, update.message.text)


def models(update, context):
    """reply with latest available OSS kernel links"""
    if len(context.args) < 1:
        message = '*Usage: * `/models codename`'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower().split('_')[0]
    message, status = xfu.check_models(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.warning("@%s requested wrong models info: %s",
                       update.effective_user.username, update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')
    LOGGER.info("@%s requested models info: %s",
                update.effective_user.username, update.message.text)


def whatis(update, context):
    """reply with latest available OSS kernel links"""
    if len(context.args) < 1:
        message = '*Usage: * `/whatis codename`'
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id,
                                 parse_mode='Markdown')
        return
    device = context.args[0].lower().split('_')[0]
    message, status = xfu.whatis(device)
    if status is False:
        context.bot.send_message(chat_id=update.message.chat_id, text=message,
                                 reply_to_message_id=update.message.message_id)
        LOGGER.warning("@%s requested wrong whatis info: %s",
                       update.effective_user.username, update.message.text)
        return
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes')
    LOGGER.info("@%s requested whatis info: %s",
                update.effective_user.username, update.message.text)


def usage(update, context):
    """Help - How to use the bot"""
    message = "Available commands:\n" \
              "/recovery `codename` - gets latest recovery ROMs info.\n" \
              "/fastboot `codename` - gets latest fastboot ROMs info.\n" \
              "/latest `codename` - gets latest MIUI versions info.\n" \
              "/firmware `codename` - gets latest available firmware for device.\n" \
              "/oss `codename` - gets all official available OSS kernels for device.\n" \
              "/list `codename` - gets all official available recovery MIUI ROMs for device.\n" \
              "/models `codename` - gets info about all available models of a device.\n" \
              "/whatis `codename` - tells you which device is this."
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
    updater = Updater(token=TOKEN, use_context=True)
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

    if IS_ADMIN:  # load admin commands if module is found
        admin.main(dispatcher)
    # unknown_handler = MessageHandler(Filters.command, unknown)
    # dispatcher.add_handler(unknown_handler)

    updater.start_polling()  # start the bot

    updater.idle()


if __name__ == '__main__':
    main()
