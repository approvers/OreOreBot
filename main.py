import discord
import datetime
import asyncio
import sys
import os
import subprocess
import requests
import json
import codecs
from random import randint

from lib import scraping
from lib.weather import get_weather
from lib.util import Singleton
from lib.lol_counter import LolCounter

from message_command import MessageCommands

import re

class MainClient(discord.Client, Singleton):
    """
    Discordクライアント(多重起動防止機構付き)
    """
    CLI_BOTS = [
        685429240908218368, 
        684655652182032404, 
        685457071906619505        
    ]
    def __init__(self, token, base_channel_id):
        """
        クライアントを起動する前の処理
        tokenとか最初にメッセージ送信するチャンネルの指定をしたりする
        Parameters
        ----------
        token: str
            discordのBotのトークン
        base_channel_id: int
            ログインをし、時報を送信するチャンネルのid
        """
        super(MainClient, self).__init__()
        self.token = token
        self.base_channel_id = base_channel_id

        # Initialize in on_ready()
        # Because use value in client
        self.base_channel = None
        self.lol_counter  = None
        self.HARASYO      = None

        # mesm_json_syntax_conceal = 0sages.json (時報json) の読み込みを試みる
        # msg_dictのkeyはstr型です、int型で呼び出そうとしないで()
        with codecs.open("messages.json", 'r', 'utf-8') as f:
            self.msg_dict = json.loads(f.read())


    def launch(self):
        self.run(self.token)

    async def on_ready(self):

        """
        Clientの情報をもとにした初期化と時報の起動
        """
        if len(self.guilds) == 1:
            self.base_channel = self.get_channel(self.base_channel_id)
            self.lol_counter = LolCounter(self.guilds[0].members)
            asyncio.ensure_future(self.ziho())
            harasyo = self.get_emoji(684424533997912096)
            isso = self.get_emoji(685162743317266645)
            MessageCommands.static_init(self.guilds[0].members, harasyo, isso)
            await self.base_channel.send("響だよ。その活躍ぶりから不死鳥の通り名もあるよ")

    async def on_message(self, message):
        if message.author.bot and not message.author.id in MainClient.CLI_BOTS:
            return
        channel = message.channel
        message_str = message.content
        command = MessageCommands(message_str, channel, message)
        await command.execute()

    async def ziho(self):
        """
        時報を制御する関数
        """
        timezone = datetime.timezone(datetime.timedelta(hours=9))
        messages = self.msg_dict["ziho"]
        while True:
            time = datetime.datetime.now(tz=timezone)
            if time.minute == 0:
                hour = str(time.hour)
                await self.base_channel.send(messages[hour])
                if hour == "6":
                    weather = get_weather()["today"]
                    await self.base_channel.send(
                        "今日の天気は{}\n最高気温は{}℃で昨日と{}℃違うよ\n最低気温は{}℃で昨日と{}℃違うよ\n今日も頑張ってね"\
                        .format(
                            weather["weather"],
                            weather["high"],
                            weather["high_diff"][1:-1],
                            weather["low"],
                            weather["low_diff"][1:-1]
                        )
                    )
                if hour == "19":
                    weather = get_weather()["tomorrow"]
                    await self.base_channel.send(
                        "明日の天気は{}\n最高気温は{}℃で今日と{}℃違うよ\n最低気温は{}℃で今日と{}℃違うよ\n今日も1日お疲れ様"\
                        .format(
                            weather["weather"],
                            weather["high"],
                            weather["high_diff"][1:-1],
                            weather["low"],
                            weather["low_diff"][1:-1]
                        )
                    )
                await asyncio.sleep(15)
            await asyncio.sleep(50)

if __name__ == "__main__":
    token = os.environ["TOKEN"]
    base_channel_id = 684289417682223150
    main = MainClient()
    main.launch()

