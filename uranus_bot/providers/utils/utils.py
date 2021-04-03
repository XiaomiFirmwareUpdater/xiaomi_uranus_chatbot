""" Providers utilities """
from aiohttp import ClientResponse


async def fetch(session, url) -> str:
    """ Fetch website page """
    response: ClientResponse
    async with session.get(url) as response:
        return await response.text()
