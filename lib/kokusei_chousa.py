"""
国勢調査です
鯖民の通常ユーザー/BOTの数を統計します
例によって関数です
"""

import discord

NUMBER_TEXT = "***†只今の限界開発鯖の人口†***\n```\n・通常ユーザー: {} 人\n・Botユーザー: {} 人\n・Bot率: {}%```"


async def number(channel: discord.TextChannel):
    bot_number = 0
    user_number = 0
    for member in channel.guild.members:
        if member.bot:
            bot_number += 1
        else:
            user_number += 1
    bot_ratio = float(bot_number) / (float(bot_number) + float(user_number))
    await channel.send(NUMBER_TEXT.format(user_number, bot_number, round(bot_ratio, 3) * 100))
