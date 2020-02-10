""" Xiaomi Geeks Telegram Bot"""
from subprocess import Popen, PIPE

cmds_list = ['python -m telegram_bot', 'python -m discord_bot']
procs_list = [Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True) for cmd in cmds_list]
for proc in procs_list:
    proc.wait()
