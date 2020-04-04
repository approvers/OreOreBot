"""
PartyIchiyo関連の処理をする
"""

import discord
import asyncio
import datetime
import random

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
        self.timezone = datetime.timezone(datetime.timedelta(hours=9))

        self.is_disabled = True
        self.time_interval: int = 1
        self.random_minute: int = int(random.randint(0,60))
        print("Next guerrilla will be:{}".format(self.random_minute))

    def change_propaty(self, is_disabled = None, time_interval = None, random_minute = None):
        if not is_disabled is None:
            self.is_disabled = is_disabled
        if not time_interval is None:
            self.time_interval = time_interval
        if not random_minute is None:
            self.random_minute = random_minute
            print("Next guerrilla will be:{}".format(self.random_minute))

    async def base(self):
        """
        ゲリラのループ処理を行う関数
        """
        while not self.is_disabled:
            time = datetime.datetime.now(tz=self.timezone)

            if time.hour % self.time_interval == 0 and\
                    time.minute == self.random_minute and\
                    len(self.base_voice_channel.members) != 0:
                await self.do()
                self.change_propaty(random_minute=random.randint(0,60))
                print("Next guerrilla will be:{}".format(self.random_minute))

            await asyncio.sleep(50)

    async def do(self):
        """
        実際にPartyIchiyoを実行する
        """
        voice_client = await self.base_voice_channel.connect(reconnect=False)
        voice_client.play(discord.FFmpegPCMAudio("ast/snd/edm.mp3"))
        await self.kikisen_channel.send("パーティー Nigth")
        await asyncio.sleep(5)
        await voice_client.disconnect(force=True)