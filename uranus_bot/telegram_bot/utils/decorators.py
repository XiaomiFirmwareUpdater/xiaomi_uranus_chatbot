from asyncio import sleep
from functools import wraps

from telethon.errors import (
    ChannelPrivateError,
    ChatWriteForbiddenError,
    UserIsBlockedError,
    InterdcCallErrorError,
    MessageNotModifiedError,
    InputUserDeactivatedError,
    SlowModeWaitError,
    FloodWaitError
)


def exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (ChannelPrivateError, ChatWriteForbiddenError,
                UserIsBlockedError, InterdcCallErrorError,
                MessageNotModifiedError, InputUserDeactivatedError):
            pass
        except SlowModeWaitError as error:
            await sleep(error.seconds)
            return await func(*args, **kwargs)
        except FloodWaitError as error:
            await sleep(error.seconds)
            return await func(*args, **kwargs)

    return wrapper
