"""Xiaomi Geeks Discord Bot main module."""

from discord import Embed

from uranus_bot.discord_bot import DATABASE
from uranus_bot.discord_bot.discord_bot import BOT
from uranus_bot.discord_bot.messages.main import start_message
from uranus_bot.discord_bot.utils.chat import get_chat_info


@BOT.before_invoke
async def register_chat(ctx):
    """Register chats that invoke the bot through an interaction."""
    if not DATABASE.is_known_chat(ctx.channel.id):
        DATABASE.add_chat_to_db(await get_chat_info(ctx))


@BOT.hybrid_command(name='start', description='Show the welcome message', with_app_command=True)
async def start(ctx):
    """Send the welcome message."""
    await ctx.send(None, embed=await start_message())


def command_usage(app_command):
    """Format an application command and its parameters."""
    parameters = ' '.join(
        f'<{parameter.name}>' if parameter.required else f'[{parameter.name}]'
        for parameter in app_command.parameters
    )
    return f'/{app_command.name} {parameters}'.rstrip()


@BOT.hybrid_command(name='help', description='Show bot usage information', with_app_command=True)
async def help_command(ctx, command: str = None):
    """Send bot usage information."""
    if command:
        app_command = BOT.tree.get_command(command)
        if not app_command:
            await ctx.send(f'Unknown command: `{command}`')
            return
        await ctx.send(
            embed=Embed(
                title=command_usage(app_command),
                description=app_command.description,
            )
        )
        return

    commands = [
        f'`{command_usage(app_command)}` — {app_command.description}'
        for app_command in sorted(BOT.tree.get_commands(), key=lambda item: item.name)
    ]
    await ctx.send(embed=Embed(title='Commands', description='\n'.join(commands)))
