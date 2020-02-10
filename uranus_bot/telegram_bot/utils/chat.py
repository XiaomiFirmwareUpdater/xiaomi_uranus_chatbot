""" Xiaomi Geeks Telegram Bot chat utilities"""

from telethon.tl.types import User


async def get_chat_id(event) -> int:
    """Returns chat ID of user or channel"""
    return event.message.from_id if event.message.from_id else event.message.to_id.channel_id


async def get_user_info(event) -> dict:
    """Returns a dictionary of user information"""
    chat_type = "user" if event.is_private else "group" if event.is_group else "channel"
    chat = await event.get_chat()
    if isinstance(chat, User):
        sender = await event.get_sender()
        name = ''
        if sender.first_name:
            name += sender.first_name.strip()
        if sender.last_name:
            name += ' ' + sender.last_name.strip()
        username = sender.username if sender.username else None
        chat_id = sender.id
    else:
        name = chat.title
        username = chat.username if chat.username else None
        chat_id = chat.id
    return {'id': chat_id, 'username': username, 'name': name, 'type': chat_type}
