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

        self.change_propaty(is_disabled=True, time_interval=1, random_minute=int(random.randint(0,60)))

    def change_propaty(self, is_disabled = None, time_interval = None, random_minute = None):
        if not is_disabled is None:
            self.is_disabled = is_disabled
        if not time_interval is None:
            self.time_interval = time_interval
        if not random_minute is None:
            self.random_minute = random_minute
            print("Next guerrilla will be:{}".format(self.random_minute))

    async def change_command(self, commands, channel):
        if commands[0].lower() == "partyichiyo":
            if len(commands) >= 2:
                if commands[1].lower() == "disable":
                    self.change_propaty(is_disabled=True)
                    await channel.send("ゲリラpartyichiyoは無効化されました")
                elif commands[1].lower() == "enable":
                    self.change_propaty(is_disabled=False)
                    await channel.send("ゲリラpartyichiyoは有効化されました")
                elif commands[1].lower() == "status":
                    await channel.send("ゲリラ一葉の現在の状態は" + str(not self.is_disabled) + "です。")
                elif commands[1].lower() == "change":
                    if len(commands) >= 3:
                        if self.is_disabled:
                            await channel.send("partyichiyoは無効化されています")
                            return
                        self.change_propaty(random_minute=int(commands[2]))
                        await channel.send(
                            "次回のゲリラが" + str(self.random_minute) + "に設定されました")
                    else:
                        self.change_propaty(random_minute=random.randint(0, 60))
                        await channel.send(
                            "次回のゲリラが" + str(self.random_minute) + "に設定されました")
                return
            await self.do()
            return

    async def base(self):
        """
        ゲリラのループ処理を行う関数
        """
        while True:
             time = datetime.datetime.now(tz=self.timezone)

             if time.hour % self.time_interval == 0 and time.minute == self.random_minute and\
                     len(self.base_voice_channel.members) != 0 and not self.is_disabled:
                await self.do()
                self.change_propaty(random_minute=random.randint(0,60))

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