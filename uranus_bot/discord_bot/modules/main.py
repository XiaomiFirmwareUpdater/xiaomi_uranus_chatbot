""" Xiaomi Geeks Discord Bot main module"""
from discord import HTTPException
from discord.ext.commands import CommandNotFound, DisabledCommand, NoPrivateMessage, NotOwner, \
    MissingRequiredArgument

from uranus_bot.discord_bot import DATABASE, DISCORD_LOGGER
from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.main import start_message
from uranus_bot.discord_bot.utils.chat import get_chat_info


@BOT.hybrid_command(name='start', with_app_command=True)
async def start(ctx):
    """Sends the welcome message"""
    await ctx.send(None, embed=await start_message())


@BOT.event
async def on_message(message):
    """Deal with incoming messages"""
    # Add new chats to the database
    if not DATABASE.is_known_chat(message.channel.id):
        DATABASE.add_chat_to_db(await get_chat_info(message))
    # Greet first time users
    if not message.guild and message.author != BOT.user and not message.channel.history(limit=1):
        await message.channel.send(None, embed=await start_message())
    else:
        await BOT.process_commands(message)

    # elif not message.guild and message.author != BOT.user:
    #     await message.channel.send("I didn't get that! Please read usage using `!help` command.")


@BOT.event
async def on_command_error(ctx, error):
    """The event triggered when an error is raised while invoking a command.
    Parameters
    ------------
    ctx: commands.Context
        The context used for command invocation.
    error: commands.CommandError
        The Exception raised.
    """
    if hasattr(ctx.command, 'on_error'):
        return

    ignored = (CommandNotFound, NotOwner)
    error = getattr(error, 'original', error)

    if isinstance(error, ignored):
        return

    if isinstance(error, DisabledCommand):
        await ctx.send(f'{ctx.command} has been disabled.')
    elif isinstance(error, MissingRequiredArgument):
        await ctx.author.send(f"Please fill in the missing required argument, "
                              f"read `!help {ctx.command}` for more information about using this command.")
    elif isinstance(error, NoPrivateMessage):
        try:
            await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
        except HTTPException:
            pass
    else:
        DISCORD_LOGGER.warning(f'Ignoring exception in command {ctx.command}:\n{error}')
