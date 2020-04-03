"""
PartyIchiyo関連の処理をする
"""

import discord
import asyncio

from lib.util import Singleton

class PartyIchiyo(Singleton):
    """
    PartyIchiyoを司るクラス
    """

    def __init__(self,main_voice_channel,kikisenn_channel):
        """
        初期化処理
        Parameters
        ----------
        main_voice_channel: discord.TextChannel
            メインのボイスチャンネルPartyIchiyoが実行されるチャンネル
        kikisenn_channel: discord.VoiceChannel
            聞き専チャンネルPartyIchiyoのメッセージが送信されるチャンネル
        """
        self.kikisenn_channel    = kikisenn_channel
        self.voice_channel       = main_voice_channel


    async def do(self):
        """
        実際にPartyIchiyoを実行する
        """
        voice_client = await self.voice_channel.connect(timeout=6.0, reconnect=False)
        player = await voice_client.play(discord.FFmpegPCMAudio("/ast/snd/edm.mp3"))
        player.start()
        await self.kikisenn_channel.send("パーティー Nigth")
        await asyncio.sleep(6)
        await voice_client.disconnect(force=True)