""" subscribe command handler """
import json
from asyncio import sleep
from datetime import datetime

from telethon import events

from uranus_bot import DEBUG
from uranus_bot.providers.firmware.firmware import diff_updates
from uranus_bot.providers.miui_updates_tracker.miui_updates_tracker import is_new_update
from uranus_bot.telegram_bot import DATABASE, TG_LOGGER
from uranus_bot.telegram_bot.messages.firmware import firmware_update_message
from uranus_bot.telegram_bot.messages.miui_updates import miui_update_message, \
    wrong_codename_message, subscribed_message, already_subscribed_message, subscriptions_message, unsubscribed_message
from uranus_bot.telegram_bot.messages.vendor import vendor_update_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER
from uranus_bot.telegram_bot.utils.chat import get_user_info, is_group_admin
from uranus_bot.telegram_bot.utils.decorators import exception_handler


@BOT.on(events.NewMessage(pattern=r'/subscribe (firmware|miui|vendor) (\w+)'))
async def subscribe(event):
    """Subscribe to updates"""
    if not await subscription_allowed(event):
        return
    try:
        sub_type = event.pattern_match.group(1)
        device = event.pattern_match.group(2)
    except IndexError:
        sub_type = event.message.message.split(' ')[1]
        device = event.message.message.split(' ')[2]
    locale = DATABASE.get_locale(event.chat_id)
    if not await is_device(sub_type, device):
        await event.reply(await wrong_codename_message(locale))
        return
    if DATABASE.add_subscription(await get_user_info(event), sub_type, device):
        message = await subscribed_message(sub_type, device, locale)
    else:
        message = await already_subscribed_message(sub_type, device, locale)
    await event.reply(message)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern=r'/unsubscribe (firmware|miui|vendor) (\w+)'))
async def unsubscribe(event):
    """Unsubscribe to updates"""
    if not await subscription_allowed(event):
        return
    sub_type = event.pattern_match.group(1)
    device = event.pattern_match.group(2)
    locale = DATABASE.get_locale(event.chat_id)
    if not await is_device(sub_type, device):
        await event.reply(await wrong_codename_message(locale))
        return
    DATABASE.remove_subscription(await get_user_info(event), sub_type, device)
    message = await unsubscribed_message(sub_type, device, locale)
    await event.reply(message)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern=r'/subscription'))
async def subscription_handler(event):
    """List your current subscriptions"""
    if not await subscription_allowed(event):
        return
    locale = DATABASE.get_locale(event.chat_id)
    subscriptions = DATABASE.get_chat_subscriptions(event.chat_id)
    await event.reply(await subscriptions_message(subscriptions, locale))
    raise events.StopPropagation


async def subscription_allowed(event) -> bool:
    """Check if the subscription is allowed"""
    return bool(event.is_private or await is_group_admin(
        event) or event.is_channel and not event.is_private and not event.is_group)


async def is_device(sub_type, device) -> bool:
    """Check if the given device codename is correct"""
    return bool(
        sub_type == 'firmware' and device in PROVIDER.firmware_codenames
        or sub_type == 'miui' and device in PROVIDER.miui_codenames
        or sub_type == 'vendor' and device in PROVIDER.vendor_codenames)


async def post_firmware_updates():
    """ Send firmware updates to subscribers every 65 minutes """
    while True:
        new_updates = await diff_updates(PROVIDER.firmware_data, PROVIDER.bak_firmware_data)
        if not new_updates:
            await sleep(65 * 60)
            continue
        for codename, updates in new_updates.items():
            subscriptions = DATABASE.get_subscriptions('firmware', codename)
            if subscriptions:
                for subscription in subscriptions:
                    for update in updates:
                        locale = DATABASE.get_locale(subscription.user_id)
                        message, buttons = await firmware_update_message(codename, update, locale)
                        await post_update(subscription, message, buttons)
                        await sleep(3)
        await sleep(65 * 60)


if not DEBUG:
    BOT.loop.create_task(post_firmware_updates())


async def post_miui_updates():
    """ Send miui updates to subscribers every 65 minutes """
    while True:
        if not PROVIDER.miui_updates:
            await sleep(60)
            continue
        if PROVIDER.bak_miui_updates and PROVIDER.bak_miui_updates == PROVIDER.miui_updates:
            await sleep(65 * 60)
            continue
        for codename, data in PROVIDER.miui_updates.items():
            subscriptions = DATABASE.get_subscriptions('miui', codename)
            if not subscriptions:
                continue
            for subscription in subscriptions:
                for update in data:
                    if update['branch'] == "Weekly":
                        continue
                    first_add = False
                    if subscription.last_updates:
                        try:
                            last_update = json.loads(subscription.last_updates)
                        except TypeError:
                            continue
                        if last_update.get(update['codename'], {}).get(update['method']):
                            if not is_new_update(update, last_update[update['codename']][update['method']]):
                                continue
                            try:
                                last_update[update['codename']][update['method']]['version'] = update['version']
                                last_update[update['codename']][update['method']]['date'] = datetime.strftime(
                                    update['date'], '%Y-%m-%d')
                                DATABASE.set_last_updates(subscription, last_update)
                            except Exception as err:
                                TG_LOGGER.error("Unable to update last update data.\n" + str(err))
                                continue
                            locale = DATABASE.get_locale(subscription.user_id)
                            message, buttons = await miui_update_message(
                                update, PROVIDER.codenames_names, locale)
                            # print(subscription)
                            await post_update(subscription, message, buttons)
                            await sleep(3)
                        else:
                            first_add = True
                    else:
                        first_add = True
                    if first_add:
                        try:
                            last_update = json.loads(subscription.last_updates) if subscription.last_updates else {}
                        except TypeError:
                            last_update = {}
                        try:
                            if last_update.get(update['codename']):
                                current = last_update[update['codename']]
                                current.update({update['method']: {
                                    'version': update['version'],
                                    'date': datetime.strftime(update['date'], '%Y-%m-%d')}})
                                last_update.update({update['codename']: current})
                            else:
                                last_update.update({
                                    update['codename']: {update['method']: {
                                        'version': update['version'],
                                        'date': datetime.strftime(update['date'], '%Y-%m-%d')}}})
                            DATABASE.set_last_updates(
                                subscription, last_update)
                        except Exception as err:
                            TG_LOGGER.error("Unable to update last update data.\n" + str(err))
        await sleep(65 * 60)

if not DEBUG:
    BOT.loop.create_task(post_miui_updates())


async def post_vendor_updates():
    """ Send vendor updates to subscribers every 65 minutes """
    while True:
        new_updates = await diff_updates(PROVIDER.vendor_data, PROVIDER.bak_vendor_data)
        if not new_updates:
            await sleep(65 * 60)
            continue
        for codename, updates in new_updates.items():
            subscriptions = DATABASE.get_subscriptions('vendor', codename)
            if subscriptions:
                for subscription in subscriptions:
                    for update in updates:
                        locale = DATABASE.get_locale(subscription.user_id)
                        message, buttons = await vendor_update_message(codename, update, locale)
                        await post_update(subscription, message, buttons)
                        await sleep(3)
        await sleep(65 * 60)

# if not DEBUG:
#     BOT.loop.create_task(post_vendor_updates())


@exception_handler
async def post_update(subscription, message, buttons):
    """Send update to subscribed chat"""
    if subscription.chat_type == 'channel':
        entity = await BOT.get_entity(int('-100' + str(subscription.user_id)))
        await BOT.send_message(entity, message, buttons=buttons)
    else:
        try:
            await BOT.send_message(subscription.user_id, message, buttons=buttons)
        except ValueError:
            try:
                entity = await BOT.get_entity(subscription.user_id)
                await BOT.send_message(entity, message, buttons=buttons)
            except ValueError:
                pass
