# Xiaomi Geeks Chat Bot V2

#### By [yshalsager](https://t.me/yshalsager)

[![Crowdin](https://badges.crowdin.net/xiaomi-geeks-chatbot/localized.svg)](https://crowdin.com/project/xiaomi-geeks-chatbot)

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Xiaomi Geeks Chat Bot (Uranus) is an all-in-one chat bot that provides useful services for Xiaomi users on Telegram and Discord.

You can start using it or adding it to your group [here on Telegram](https://t.me/XiaomiGeeksBot), or `@XiaomiGeeksBot#1241` on Discord.

### About the code:

This project is a modular bot, made using Python 3 and the following libraries:

- [Telethon](https://github.com/LonamiWebs/Telethon/)

- [aiohttp](https://github.com/aio-libs/aiohttp)

- [discord.py](https://github.com/Rapptz/discord.py)

The whole bot functions in this repo, which are licensed under GPL3, are based on [XiaomiFirmwareUpdater](https://github.com/XiaomiFirmwareUpdater/) other projects and files, including and not limited to:

- [mi-firmware-updater](https://github.com/XiaomiFirmwareUpdater/mi-firmware-updater)
- [miui-updates-tracker](https://github.com/XiaomiFirmwareUpdater/miui-updates-tracker)
- [xiaomifirmwareupdater.github.io](https://github.com/XiaomiFirmwareUpdater/xiaomifirmwareupdater.github.io)
- [mi-vendor-updater](https://github.com/TryHardDood/mi-vendor-updater)
- [xiaomi_devices](https://github.com/XiaomiFirmwareUpdater/xiaomi_devices)

However, [the telegram bot](https://t.me/XiaomiGeeksBot) may contain some other features that are not available in this code, like the Admins module.

### Bot features:

This chat bot aims to provide easy access for all the stuff that Xiaomi users need, starting from guides and tools, and ending with advanced things like custom recovery and firmware.

- Get MIUI official updates links.
- Get Firmware and Vendor packages for custom roms users.
- Get Custom recovery like TWRP, Orangefox, and PitchBlack.
- Get Xiaomi.eu ROMs.
- Various guides and tools.
- Subscribe to the aforementioned updates to get new releases notifications.
- Use the bot in your own language, more than 10 languages are supported.

### Running this bot on your own:

- Make sure you have python3.7+ installed.

- Install the required libs.
  
  ```
  pip3 install -r requirements.txt
  ```

- Copy the bot config file and rename it to config.yml, then fill the required placeholders.

- Run Telegram bot using `python3 -m telegram_bot`

- Run Discord bot using `python3 -m discord_bot`
