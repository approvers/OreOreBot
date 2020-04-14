"""
国勢調査です
鯖民の通常ユーザー/BOTの数を統計します
例によって関数です
"""

import discord

NUMBER_TEXT = "***†只今の限界開発鯖の人口†***\n```\n・通常ユーザー: {} 人\n・Botユーザー: {} 人\n・Bot率: {}%```"


async def number(channel: discord.TextChannel):
    """
    メッセージが発言されたギルドのBotとUserの人口を調べる関数
    統計後、それを発言されたチャンネルに送信する
    Parameters
    ----------
    channel: discord.TextChannel
        発言されたテキストチャンネル
    """
    bot_number = 0
    user_number = 0
    for member in channel.guild.members:
        if member.bot:
            bot_number += 1
        else:
            user_number += 1
    bot_parentage = (bot_number) / (bot_number + user_number) * 100
    await channel.send(NUMBER_TEXT.format(user_number, bot_number, round(bot_parentage, 3)))
