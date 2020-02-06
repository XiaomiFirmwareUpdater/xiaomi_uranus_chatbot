#!/usr/bin/env python3.7
"""Xiaomi Helper Bot"""

import logging
import re
from os.path import dirname

import yaml
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, InlineQueryHandler
from telegram.ext import Updater
from telegram.ext.dispatcher import run_async

from uranus_bot.modules import gsmarena, mi_vendor_updater as mi_vendor, \
    xiaomi_firmware_updater as mi_firmware, xiaomi_oss as mi_oss, xiaomi_info as info, \
    miui_updates_tracker as miui, xiaomi_eu, custom_recovery, misc

from uranus_bot.modules.inline import process_query

# from telegram.ext import MessageHandler, Filters

WORK_DIR = dirname(__file__)
PARENT_DIR = '/'.join(dirname(__file__).split('/')[:-1])

# read bog config
with open(f'{PARENT_DIR}/config.yml', 'r') as f:
    CONFIG = yaml.load(f, Loader=yaml.CLoader)
TOKEN = CONFIG['tg_bot_token']

# set logging
logging.basicConfig(filename=f'{WORK_DIR}/current.log',
                    filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

IS_ADMIN = True
IS_MORE = True
try:
    from uranus_bot.admin import admin
except ImportError:
    print("Can't find admin module, skipping it")
    IS_ADMIN = False
try:
    from uranus_bot.private import private
except ImportError:
    print("Can't find private commands module, skipping it")
    IS_MORE = False

HELP_URL = "https://xiaomifirmwareupdater.com/projects/uranus-chatbot/#usage"


def send_markdown_message(update, context, message, disable_web_preview='yes'):
    """ Send telegram message in markdown"""
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview=disable_web_preview)


def send_reply_markup_message(update, context, message, reply_markup):
    """ Send telegram message with markup keyboard"""
    context.bot.send_message(chat_id=update.message.chat_id, text=message,
                             reply_to_message_id=update.message.message_id,
                             parse_mode='Markdown', disable_web_page_preview='yes',
                             reply_markup=reply_markup)


@run_async
def start(update, context):
    """start command"""
    message = f"Hello {update.message.from_user.first_name}!\n" \
              "I'm Uranus, an all-in-one bot for Xiaomi users!\n" \
              "I can get you latest Official ROMs, Firmware updates links," \
              " and many more things!\nCheck how to use me by clicking /help" \
              "\nJoin [my channel](https://t.me/yshalsager_projects)" \
              "to get all updates and announcements about the bot!"
    keyboard = [
        [InlineKeyboardButton("Join my channel", url="https://t.me/yshalsager_projects"),
         InlineKeyboardButton("Read bot usage", url=HELP_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def recovery(update, context):
    """reply with latest available recovery ROMs"""
    if not context.args:
        message = '*Usage: * `/recovery device`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower()
    message, reply_markup = miui.fetch_recovery(device, inline=False)
    if not message:
        message = f"Cannot find recovery downloads for {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong recovery ROM request: %s", update.message.text)
        return
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def fastboot(update, context):
    """reply with latest available fastboot ROMs"""
    if not context.args:
        message = '*Usage: * `/fastboot device`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower()
    message, reply_markup = miui.fetch_fastboot(device, inline=False)
    if not message:
        message = f"Cannot find fastboot downloads for {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong fastboot ROM request: %s", update.message.text)
        return
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def firmware(update, context):
    """generate firmware link on website"""
    if not context.args:
        message = '*Usage: * `/firmware device`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower()
    message, reply_markup = mi_firmware.gen_fw_link(device, inline=False)
    # try:
    #     message, reply_markup = mi_firmware.gen_fw_link(device)[0]
    # except ValueError:
    #     message, reply_markup = mi_firmware.gen_fw_link(device)
    if not message or reply_markup is None:
        message = f"Cannot find firmware links for {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong firmware request: %s", update.message.text)
        return
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def latest(update, context):
    """reply with latest available ROMs version"""
    if not context.args:
        message = '*Usage: * `/latest device`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower()
    message = miui.check_latest(device, inline=False)
    if not message:
        message = f"Cannot find info about {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong latest info request: %s", update.message.text)
        return
    send_markdown_message(update, context, message)


@run_async
def oss(update, context):
    """reply with latest available OSS kernel links"""
    if not context.args:
        message = '*Usage: * `/oss device`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower()
    message = mi_oss.oss(device, inline=False)
    if not message:
        message = f"Cannot find OSS kernel info for {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong oss info request: %s", update.message.text)
        return
    send_markdown_message(update, context, message)


@run_async
def history(update, context):
    """reply with miui available roms archive link"""
    if not context.args:
        message = '*Usage: * `/archive device`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower().split('_')[0]
    message, reply_markup = miui.history(device, inline=False)
    if not message:
        message = f"Can't find info about {device}"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong list history request: %s", update.message.text)
        return
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def models(update, context):
    """reply with latest available OSS kernel links"""
    if not context.args:
        message = '*Usage: * `/models codename`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower().split('_')[0]
    message = info.check_models(device, inline=False)
    if not message:
        message = f"Cannot find models info for {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong list models request: %s", update.message.text)
        return
    send_markdown_message(update, context, message)


@run_async
def whatis(update, context):
    """reply with device name"""
    if not context.args:
        message = '*Usage: * `/whatis codename`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower()
    message = info.whatis(device, inline=False)
    if not message:
        message = f"Cannot find info about {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong whatis request: %s", update.message.text)
        return
    send_markdown_message(update, context, message)


@run_async
def codename(update, context):
    """reply with device codename"""
    if not context.args:
        message = '*Usage: * `/codename device`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = ' '.join(context.args).lower()
    message = info.get_codename(device)
    if not message:
        message = f"Cannot find codename info about {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong codename request: %s", update.message.text)
        return
    send_markdown_message(update, context, message)


@run_async
def specs(update, context):
    """reply with device's specs"""
    if not context.args:
        message = '*Usage: * `/specs codename`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower().split('_')[0]
    message = gsmarena.specs(device)
    if not message:
        message = f"Cannot find {device} specs!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong specs request: %s", update.message.text)
        return
    send_markdown_message(update, context, message, disable_web_preview='no')


@run_async
def vendor(update, context):
    """reply with latest fw+vendor links"""
    if not context.args:
        message = '*Usage: * `/vendor codename`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower()
    message, reply_markup = mi_vendor.fetch_vendor(device, inline=False)
    if not message:
        message = f"Cannot find vendor downloads for {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong vendor request: %s", update.message.text)
        return
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def miui_eu(update, context):
    """reply with latest Xiaomi.eu links"""
    if not context.args:
        message = '*Usage: * `/eu codename`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower()
    message, reply_markup = xiaomi_eu.xiaomi_eu(device, inline=False)
    if not message:
        message = f"Cannot find Xiaomi.eu downloads for {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong vendor request: %s", update.message.text)
        return
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def get_twrp(update, context):
    """reply with latest TWRP link"""
    if not context.args:
        message = '*Usage: * `/twrp codename`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower()
    message, reply_markup = custom_recovery.twrp(device, inline=False)
    if not message:
        message = f"Cannot find TWRP downloads for {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong twrp request: %s", update.message.text)
        return
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def get_pbrp(update, context):
    """reply with latest PBRP link"""
    if not context.args:
        message = '*Usage: * `/pb codename`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower()
    message, reply_markup = custom_recovery.pbrp(device, inline=False)
    if not message:
        message = f"Cannot find PBRP downloads for {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong pbrp request: %s", update.message.text)
        return
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def get_ofrp(update, context):
    """reply with latest OrangeFox link"""
    if not context.args:
        message = '*Usage: * `/of codename`\n' \
                  'Check how to use the bot with examples /help'
        send_markdown_message(update, context, message)
        return
    device = context.args[0].lower()
    message, reply_markup = custom_recovery.ofrp(device, inline=False)
    if not message:
        message = f"Cannot find OrangeFox downloads for {device}!"
        send_markdown_message(update, context, message)
        LOGGER.info("wrong OF request: %s", update.message.text)
        return
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def unlock(update, context):
    """reply with device unlock info"""
    message, reply_markup = misc.unlock(inline=False)
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def tools(update, context):
    """reply with device unlock info"""
    message, reply_markup = misc.tools(inline=False)
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def guides(update, context):
    """reply with device unlock info"""
    message, reply_markup = misc.guides(inline=False)
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def arb(update, context):
    """reply with device unlock info"""
    message, photo = misc.arb()
    context.bot.send_photo(chat_id=update.message.chat_id, caption=message, photo=photo,
                           reply_to_message_id=update.message.message_id,
                           parse_mode='Markdown', disable_web_page_preview='yes')


@run_async
def usage(update, context):
    """Help - How to use the bot"""
    message = "Available commands with examples:\n"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Check here", url=HELP_URL)]])
    send_reply_markup_message(update, context, message, reply_markup)


@run_async
def inline_query(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    query_args = re.findall(r'\S+', query.strip())
    if not query or len(query_args) < 1:
        return
    command = query_args[0]
    try:
        query_request = query_args[1]
    except IndexError:
        query_request = None
    results = process_query(command, query_request)
    if results and not isinstance(results, tuple):
        context.bot.answer_inline_query(update.inline_query.id, results)
        # update.inline_query.answer(results)


def error(update, context):
    """Log Errors caused by Updates."""
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


# def unknown(update, context):
#     """Reply to unknown commands"""
#     context.bot.send_message(chat_id=update.message.chat_id,
#                              reply_to_message_id=update.message.message_id,
#                              text="Sorry, I didn't understand that command.")


def main():
    """
    main function
    :return: null
    """
    # Updater continuously fetches new updates from telegram and passes them on to the Dispatcher
    updater = Updater(token=TOKEN, workers=1, use_context=True)
    dispatcher = updater.dispatcher
    # This class dispatches all kinds of updates to its registered handlers.

    commands = [CommandHandler('start', start), CommandHandler("help", usage),
                CommandHandler('recovery', recovery), CommandHandler('fastboot', fastboot),
                CommandHandler('firmware', firmware), CommandHandler('latest', latest),
                CommandHandler('oss', oss), CommandHandler('archive', history),
                CommandHandler('models', models), CommandHandler('whatis', whatis),
                CommandHandler('specs', specs), CommandHandler('codename', codename),
                CommandHandler('vendor', vendor), CommandHandler('eu', miui_eu),
                CommandHandler('twrp', get_twrp), CommandHandler('pb', get_pbrp),
                CommandHandler('of', get_ofrp), CommandHandler('unlockbl', unlock),
                CommandHandler('tools', tools), CommandHandler('arb', arb),
                CommandHandler('guides', guides), CommandHandler('oss', oss)]
    for command in commands:
        dispatcher.add_handler(command)
    dispatcher.add_handler(InlineQueryHandler(inline_query))
    dispatcher.add_error_handler(error)

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
