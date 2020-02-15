""" subscribe command handler """
from asyncio import sleep
from telethon import events, Button

from uranus_bot import XFU_WEBSITE
from uranus_bot.providers.firmware.firmware import diff_updates
from uranus_bot.providers.miui_updates_tracker.miui_updates_tracker import diff_miui_updates
from uranus_bot.telegram_bot import DATABASE
from uranus_bot.telegram_bot.messages.miui_updates import miui_update_message
from uranus_bot.telegram_bot.tg_bot import BOT, PROVIDER
from uranus_bot.telegram_bot.utils.chat import get_user_info, is_group_admin


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
    if not await is_device(sub_type, device):
        await event.reply("**Wrong codename!**")
        return
    if DATABASE.add_subscription(await get_user_info(event), sub_type, device):
        message = f"Subscribed to {device} {sub_type} updates successfully!"
    else:
        message = f"You are already subscribed to {device} {sub_type} updates!"
    await event.reply(message)
    raise events.StopPropagation


@BOT.on(events.NewMessage(pattern=r'/unsubscribe (firmware|miui|vendor) (\w+)'))
async def unsubscribe(event):
    """Unsubscribe to updates"""
    if not await subscription_allowed(event):
        return
    sub_type = event.pattern_match.group(1)
    device = event.pattern_match.group(2)
    if not await is_device(sub_type, device):
        await event.reply("**Wrong codename!**")
        return
    DATABASE.remove_subscription(await get_user_info(event), sub_type, device)
    message = f"Unsubscribed from {device} {sub_type} updates successfully!"
    await event.reply(message)
    raise events.StopPropagation


async def subscription_allowed(event) -> bool:
    """Check if the subscription is allowed"""
    return bool(event.is_private \
                or await is_group_admin(event) \
                or event.is_channel and not event.is_private and not event.is_group)


async def is_device(sub_type, device) -> bool:
    """Check if the given device codename is correct"""
    return bool(sub_type == 'firmware' and device in PROVIDER.firmware_codenames \
                or sub_type == 'miui' and device in PROVIDER.miui_codenames \
                or sub_type == 'vendor' and device in PROVIDER.vendor_codenames)


async def post_firmware_updates():
    """ Send firmware updates to subscribers every 65 minutes """
    while True:
        new_updates = await diff_updates(PROVIDER.firmware_data, PROVIDER.bak_firmware_data)
        if not new_updates:
            await sleep(65 * 60)
        for codename, updates in new_updates.items():
            subscriptions = DATABASE.get_subscriptions('firmware', codename)
            if subscriptions:
                for subscription in subscriptions:
                    for update in updates:
                        await BOT.send_message(subscription[0],
                                               f"**New Firmware update available for {codename} by** "
                                               f"@XiaomiFirmwareUpdater\n",
                                               buttons=[Button.url(f"{update}",
                                                                   f"{XFU_WEBSITE}/firmware/{codename}/")])
                        await sleep(2)
        await sleep(65 * 60)


BOT.loop.create_task(post_firmware_updates())


async def post_miui_updates():
    """ Send miui updates to subscribers every 65 minutes """
    while True:
        recovery_updates = await diff_miui_updates(PROVIDER.miui_recovery_updates, PROVIDER.bak_miui_recovery_updates)
        fastboot_updates = await diff_miui_updates(PROVIDER.miui_fastboot_updates, PROVIDER.bak_miui_fastboot_updates)
        for new_updates in [recovery_updates, fastboot_updates]:
            if not new_updates:
                await sleep(65 * 60)
            for codename, updates in new_updates.items():
                subscriptions = DATABASE.get_subscriptions('miui', codename)
                if subscriptions:
                    for subscription in subscriptions:
                        for update in updates:
                            message, buttons = await miui_update_message(update, PROVIDER.codenames_names)
                            await BOT.send_message(subscription[0], message, buttons=buttons)
                            await sleep(2)
            await sleep(65 * 60)


BOT.loop.create_task(post_miui_updates())


async def post_vendor_updates():
    """ Send vendor updates to subscribers every 65 minutes """
    while True:
        new_updates = await diff_updates(PROVIDER.vendor_data, PROVIDER.bak_vendor_data)
        if not new_updates:
            await sleep(65 * 60)
        for codename, updates in new_updates.items():
            subscriptions = DATABASE.get_subscriptions('vendor', codename)
            if subscriptions:
                for subscription in subscriptions:
                    for update in updates:
                        await BOT.send_message(subscription[0],
                                               f"**New Vendor update available for {codename} by** "
                                               f"@MIUIVendorUpdater\n",
                                               buttons=[Button.url(f"{update}", f"{XFU_WEBSITE}/vendor/{codename}/")])
                        await sleep(2)
        await sleep(65 * 60)


BOT.loop.create_task(post_vendor_updates())
