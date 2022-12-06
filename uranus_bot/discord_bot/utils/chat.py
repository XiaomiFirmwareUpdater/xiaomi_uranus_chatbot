""" Xiaomi Geeks Discord Bot chat utilities"""
from discord import DMChannel


async def get_chat_info(message) -> dict:
    """Returns a dictionary of user information"""
    if isinstance(message.channel, DMChannel):
        chat_type = "user"
        name = message.author.name
        guild_id = None
        guild_name = None
    else:
        chat_type = "channel"
        name = message.channel.name
        guild_id = message.guild.id
        guild_name = message.guild.name
    return {'id': message.channel.id, 'name': name,'type': chat_type,
            'guild_id': guild_id, 'guild_name': guild_name}
