""" Providers utilities """


async def fetch(session, url):
    """ Fetch website page """
    async with session.get(url) as response:
        return await response.text()
