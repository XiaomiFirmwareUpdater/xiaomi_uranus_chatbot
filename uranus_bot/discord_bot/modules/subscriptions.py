""" subscribe command handler """
from asyncio import sleep

from discord import Embed, DMChannel

from uranus_bot import XFU_WEBSITE, DISCORD_BOT_ADMINS
from uranus_bot.discord_bot.utils.chat import get_chat_info
from uranus_bot.providers.firmware.firmware import diff_updates
from uranus_bot.providers.miui_updates_tracker.miui_updates_tracker import diff_miui_updates
from uranus_bot.discord_bot import DATABASE
from uranus_bot.discord_bot.messages.miui_updates import miui_update_message
from uranus_bot.discord_bot.discord_bot import BOT, PROVIDER


@BOT.command(name='subscribe')
async def subscribe(ctx, *args):
    """Subscribe to firmware/miui/vendor updates"""
    if len(args) > 2:
        return
    sub_type = args[0]
    if sub_type not in ["firmware", "miui", "vendor"]:
        return
    device = args[1]
    if not await is_device(sub_type, device):
        await ctx.send("**Wrong codename!**")
        return
    if not await subscription_allowed(ctx.message):
        return
    if DATABASE.add_subscription(await get_chat_info(ctx), sub_type, device):
        message = f"Subscribed to {device} {sub_type} updates successfully!"
    else:
        message = f"You are already subscribed to {device} {sub_type} updates!"
    await ctx.send(None, embed=Embed(title=message))


@BOT.command(name='unsubscribe')
async def unsubscribe(ctx, *args):
    """unsubscribe from firmware/miui/vendor updates"""
    if not await subscription_allowed(ctx.message):
        return
    if len(args) > 2:
        return
    sub_type = args[0]
    if sub_type not in ["firmware", "miui", "vendor"]:
        return
    device = args[1]
    if not await is_device(sub_type, device):
        await ctx.send("**Wrong codename!**")
        return
    DATABASE.remove_subscription(await get_chat_info(ctx), sub_type, device)
    message = f"Unsubscribed from {device} {sub_type} updates successfully!"
    await ctx.send(None, embed=Embed(title=message))


async def subscription_allowed(message) -> bool:
    """Check if the subscription is allowed"""
    return bool(isinstance(message.channel, DMChannel)
                or message.author.guild_permissions.administrator
                or message.author.id in DISCORD_BOT_ADMINS)


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
            continue
        for codename, updates in new_updates.items():
            subscriptions = DATABASE.get_subscriptions('firmware', codename)
            if subscriptions:
                for subscription in subscriptions:
                    for update in updates:
                        chat = BOT.get_user(subscription[0]) \
                            if subscription[1] == "user" else BOT.get_channel(subscription[0])
                        await chat.send(
                            None, embed=Embed(title=
                                              f"**New Firmware update available for {codename}**",
                                              description=f"{update}",
                                              url=f"{XFU_WEBSITE}/firmware/{codename}/"))
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
                continue
            for codename, updates in new_updates.items():
                subscriptions = DATABASE.get_subscriptions('miui', codename)
                if subscriptions:
                    for subscription in subscriptions:
                        for update in updates:
                            embed = await miui_update_message(update, PROVIDER.codenames_names)
                            chat = BOT.get_user(subscription[0]) \
                                if subscription[1] == "user" else BOT.get_channel(subscription[0])
                            await chat.send(None, embed=embed)
                            await sleep(2)
            await sleep(65 * 60)


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
                        chat = BOT.get_user(subscription[0]) \
                            if subscription[1] == "user" else BOT.get_channel(subscription[0])
                        await chat.send(None, embed=Embed(
                            title=
                            f"**New Vendor update available for {codename}**",
                            description=f"{update}",
                            url=f"{XFU_WEBSITE}/vendor/{codename}/"))
                        await sleep(2)
        await sleep(65 * 60)


BOT.loop.create_task(post_vendor_updates())
