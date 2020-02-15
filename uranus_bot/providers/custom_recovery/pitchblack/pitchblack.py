"""PitchBlack recovery downloads scraper"""

import xml.etree.ElementTree as eT

from aiohttp import ClientSession

from uranus_bot.providers.utils.utils import fetch


async def load_pitchblack_data():
    """
    load PitchBlack devices downloads
    """
    async with ClientSession() as session:
        downloads = eT.fromstring(
            await fetch(session,
                        "https://sourceforge.net/projects/pitchblack-twrp/rss?path=/"))
        return [i.find('link').text for i in downloads[0].findall('item')]


async def get_pitchblack(device, pitchblack_data):
    """
    fetch latest PitchBlack recovery links for a device
    """
    try:
        link = [i for i in pitchblack_data if device in i][0]
    except IndexError:
        return
    return {link.split('/')[-2]: link}
