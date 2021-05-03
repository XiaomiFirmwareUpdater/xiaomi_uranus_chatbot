""" subscribe command handler """
import json
from asyncio import sleep
from datetime import datetime

from discord import Embed, DMChannel

from uranus_bot import XFU_WEBSITE, DISCORD_BOT_ADMINS
from uranus_bot.discord_bot.utils.chat import get_chat_info
from uranus_bot.providers.firmware.firmware import diff_updates
from uranus_bot.providers.miui_updates_tracker.miui_updates_tracker import is_new_update
from uranus_bot.discord_bot import DATABASE, DISCORD_LOGGER
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


@BOT.command(name='subscription')
async def subscription_handler(ctx):
    """List your current subscriptions"""
    if not await subscription_allowed(ctx.message):
        return
    subscriptions = DATABASE.get_chat_subscriptions(ctx.message.channel.id)
    message = ""
    for subscription in subscriptions:
        message += f"{subscription.sub_type} ({subscription.device})"
    embed = Embed(title=f"**You're subscribed to:**", description=message)
    await ctx.send(None, embed=embed)


async def subscription_allowed(message) -> bool:
    """Check if the subscription is allowed"""
    return bool(isinstance(message.channel, DMChannel)
                or message.author.guild_permissions.administrator
                or message.author.id in DISCORD_BOT_ADMINS)


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
                        chat = BOT.get_user(subscription.user_id) \
                            if subscription.chat_type == "user" else BOT.get_channel(subscription.user_id)
                        if not chat:
                            continue
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
        if not PROVIDER.miui_updates:
            await sleep(60)
            continue
        for updates_group in PROVIDER.miui_updates:
            codename = updates_group[0]['codename']
            subscriptions = DATABASE.get_subscriptions('miui', codename)
            if subscriptions:
                for subscription in subscriptions:
                    for update in updates_group:
                        branch = update['branch'].split(' ')[0].lower()
                        try:
                            last_update = json.loads(subscription.last_updates)['miui'][branch]
                        except TypeError:
                            continue
                        if is_new_update(update, last_update):
                            try:
                                last_update['version'] = update['version']
                                last_update['date'] = datetime.strftime(update['date'], '%Y-%m-%d')
                                DATABASE.set_last_updates(subscription, branch, last_update)
                            except Exception as err:
                                DISCORD_LOGGER.error("Unable to update last update data.\n" + str(err))
                                continue
                            embed = await miui_update_message(update, PROVIDER.codenames_names)
                            chat = BOT.get_user(subscription.user_id) \
                                if subscription.chat_type == "user" else BOT.get_channel(subscription.user_id)
                            if not chat:
                                continue
                            await chat.send(None, embed=embed)
                            await sleep(3)
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
                        chat = BOT.get_user(subscription.user_id) \
                            if subscription.chat_type == "user" else BOT.get_channel(subscription.user_id)
                        await chat.send(None, embed=Embed(
                            title=
                            f"**New Vendor update available for {codename}**",
                            description=f"{update}",
                            url=f"{XFU_WEBSITE}/vendor/{codename}/"))
                        await sleep(2)
        await sleep(65 * 60)


BOT.loop.create_task(post_vendor_updates())
