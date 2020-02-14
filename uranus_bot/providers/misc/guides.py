"""Tools info provider"""

from uranus_bot.providers.misc import WIKI, XDA


async def get_guides():
    """various tools for Xiaomi devices"""
    return [{
        "Flashing official ROMs": f"{WIKI}/Flash_official_ROMs.html",
        "Flashing TWRP & custom ROMs": f"{WIKI}/Flash_TWRP_and_custom_ROMs.html",
        "Fix notifications on MIUIl": f"{WIKI}/Fix_notifications_on_MIUI.html",
        "Disable MIUI Ads 1": f"{WIKI}/Disable_ads_in_MIUI.html",
        "Disable MIUI Ads 2": f"{XDA}/xiaomi-miui-ads-hamper-user-experience/"
    }]
