"""Uranus Bot inline mode"""
# pylint: disable=too-many-branches

from uranus_bot.modules.xiaomi_firmware_updater import gen_fw_link
from uranus_bot.modules.miui_updates_tracker import fetch_recovery,\
    fetch_fastboot, history, check_latest
from uranus_bot.modules.mi_vendor_updater import fetch_vendor
from uranus_bot.modules.xiaomi_eu import xiaomi_eu
from uranus_bot.modules.custom_recovery import twrp, ofrp, pbrp
from uranus_bot.modules.xiaomi_oss import oss
from uranus_bot.modules.xiaomi_info import whatis, check_models
from uranus_bot.modules.misc import guides, tools, unlock


def process_query(command, query_request):
    """Process inline query"""
    results = None
    if command == "firmware":
        results = gen_fw_link(query_request, inline=True)
    elif command == "recovery":
        results = fetch_recovery(query_request, inline=True)
    elif command == "fastboot":
        results = fetch_fastboot(query_request, inline=True)
    elif command == "archive":
        results = history(query_request, inline=True)
    elif command == "latest":
        results = check_latest(query_request, inline=True)
    elif command == "vendor":
        results = fetch_vendor(query_request, inline=True)
    elif command == "eu":
        results = xiaomi_eu(query_request, inline=True)
    elif command == "twrp":
        results = twrp(query_request, inline=True)
    elif command == "of":
        results = ofrp(query_request, inline=True)
    elif command == "pb":
        results = pbrp(query_request, inline=True)
    elif command == "oss":
        results = oss(query_request, inline=True)
    elif command == "whatis":
        results = whatis(query_request, inline=True)
    elif command == "models":
        results = check_models(query_request, inline=True)
    elif command == "guides":
        results = guides(inline=True)
    elif command == "tools":
        results = tools(inline=True)
    elif command == "unlockbl":
        results = unlock(inline=True)
    return results
