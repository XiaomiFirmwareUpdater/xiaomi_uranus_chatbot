from asyncio import sleep
from functools import wraps

from telethon.errors import (
    ChannelPrivateError,
    ChatWriteForbiddenError,
    UserIsBlockedError,
    InterdcCallErrorError,
    MessageNotModifiedError,
    InputUserDeactivatedError,
    MessageIdInvalidError,
    SlowModeWaitError,
    FloodWaitError,
    PeerIdInvalidError,
    AuthKeyError
)


def exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (ChannelPrivateError, ChatWriteForbiddenError,
                UserIsBlockedError, InterdcCallErrorError,
                MessageNotModifiedError, InputUserDeactivatedError,
                MessageIdInvalidError, PeerIdInvalidError):
            pass
        except SlowModeWaitError as error:
            await sleep(error.seconds)
            return exception_handler(await func(*args, **kwargs))
        except FloodWaitError as error:
            await sleep(error.seconds)
            return exception_handler(await func(*args, **kwargs))
        except AuthKeyError as error:
            if error.code == 406 and error.message == "TOPIC_DELETED":
                pass
            else:
                raise error
    return wrapper
