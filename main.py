"""
はらちょの根幹ファイル
"""
import asyncio
import sys
import os
import json
import codecs

import discord

from lib.util import Singleton
from lib.lol_counter import LolCounter
from lib.time_signal import TimeSignal

from message_command import MessageCommands


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

        # mesm_json_syntax_conceal = 0sages.json (時報json) の読み込みを試みる
        # msg_dictのkeyはstr型です、int型で呼び出そうとしないで()
        with codecs.open("messages.json", 'r', 'utf-8') as json_file:
            self.msg_dict = json.loads(json_file.read())

    def launch(self):
        """
        clientの起動
        """
        self.run(self.token)

    async def on_ready(self):

        """
        Clientの情報をもとにした初期化と時報の起動
        """
        if len(self.guilds) == 1:
            self.base_channel = self.get_channel(self.base_channel_id)

            time_signal = TimeSignal(
                self.base_channel,
                self.msg_dict["ziho"]
            )

            asyncio.ensure_future(time_signal.base())

            harasyo = self.get_emoji(684424533997912096)
            isso = self.get_emoji(685162743317266645)
            MessageCommands.static_init(self.guilds[0].members, harasyo, isso)
            await self.base_channel.send("響だよ。その活躍ぶりから不死鳥の通り名もあるよ")

    async def on_message(self, message):
        """
        BOT以外がメッセージを送信したときに関数に処理をさせる
        """
        if message.author.bot and not message.author.id in MainClient.CLI_BOTS:
            return
        channel = message.channel
        message_str = message.content
        command = MessageCommands(message_str, channel, message.author)
        await command.execute()


if __name__ == "__main__":
    TOKEN = os.environ["TOKEN"]
    BASE_CHANNEL = sys.argv[1]
    MAIN = MainClient(TOKEN. BASE_CHANNEL)
    MAIN.launch()

