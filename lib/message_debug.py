"""
message_debug関連の処理がなされます
実装してみたら一つしか関数ができなかったので関数での実装となります
"""
import discord

from lib.util import Singleton

async def message_debug(before, after):
    await before.channel.send("メッセージのデバッグを表示します。")
    await before.channel.send("```\n{}\n```".format(str(before.content)))