"""
PartyIchiyo関連の処理をする
"""

import discord
import asyncio
import datetime

from lib.util import Singleton

class PartyIchiyo(Singleton):
    """
    PartyIchiyoを司るクラス
    """

    def __init__(self, base_voice_channel, kikisen_channel):
        """
        初期化処理
        Parameters
        ----------
        main_voice_channel: discord.TextChannel
            メインのボイスチャンネルPartyIchiyoが実行されるチャンネル
        kikisenn_channel: discord.VoiceChannel
            聞き専チャンネルPartyIchiyoのメッセージが送信されるチャンネル
        """
        self.base_voice_channel    = base_voice_channel
        self.kikisen_channel      = kikisen_channel

        self.is_disabled = False
        self.time_interbal = 1

    def change_propaty(self):
        pass

    async def do(self):
        """
        実際にPartyIchiyoを実行する
        """
        voice_client = await self.base_voice_channel.connect(reconnect=False)
        voice_client.play(discord.FFmpegPCMAudio("ast/snd/edm.mp3"))
        await self.kikisen_channel.send("パーティー Nigth")
        await asyncio.sleep(5)
        await voice_client.disconnect(force=True)