"""
はらちょの根幹ファイル
"""
import asyncio
import os
import json
import codecs

import discord

from lib.util import Singleton
from lib.time_signal import TimeSignal
from lib.voice_diff import VoiceDiffHandler
from lib.message_debug import *
from lib.mitetazo import mitetazo
from lib.editmiteta import mitetazo_edit

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

    __ready = False
    def __init__(self, token: str, base_channel_id: int, base_voice_id: int, kikisen_channel_id: int, hakaba_voice_id: int):
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
        intents = discord.Intents.all()
        intents.members = True
        super(MainClient, self).__init__(presences=True, guild_subscriptions=True, intents=intents)
        self.token = token
        self.base_channel_id = base_channel_id
        self.base_voice_id = base_voice_id
        self.kikisen_channel_id = kikisen_channel_id
        self.hakaba_voice_id = hakaba_voice_id

        self.voice_diff_handler = VoiceDiffHandler()

        # Initialize in on_ready()
        # Because use value in client
        self.base_channel = None
        self.base_voice_channel = None
        self.kikisen_channel = None
        self.hakaba_voice_channel = None

        self.guild = None

        # mesm_json_syntax_conceal = 0sages.json (時報json) の読み込みを試みる
        # msg_dictのkeyはstr型です、int型で呼び出そうとしないで()
        with codecs.open(os.getcwd() + "/messages.json", 'r', 'utf-8') as json_file:
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
        if (MainClient.__ready):
            return
        MainClient.__ready = True
        if len(self.guilds) == 1:
            self.base_channel = self.get_channel(self.base_channel_id)
            self.base_voice_channel = self.get_channel(self.base_voice_id)
            self.kikisen_channel = self.get_channel(self.kikisen_channel_id)
            self.hakaba_voice_channel = self.get_channel(self.hakaba_voice_id)
            self.guild = self.guilds[0]

            time_signal = TimeSignal(
                self.base_channel,
                self.msg_dict["ziho"]
            )

            asyncio.ensure_future(time_signal.base())

            harasyo = self.get_emoji(684424533997912096)
            isso = self.get_emoji(685162743317266645)
            abc_emojis = {"AC":self.get_emoji(693007620159832124),"WA":self.get_emoji(693007620201775174),
                          "CE":self.get_emoji(693007619803185194),"TLE":self.get_emoji(693007620444913664)}
            MessageCommands.static_init(self.guilds[0].members, harasyo, isso, abc_emojis,
                                        self.base_voice_channel, self.kikisen_channel, self.hakaba_voice_channel)
            asyncio.ensure_future(MessageCommands.PARTY_ICHIYO.base())
            asyncio.ensure_future(MessageCommands.KAERE.base())
            print("Bot started successfully!")
            await self.base_channel.send("響だよ。その活躍ぶりから不死鳥の通り名もあるよ")

    async def on_message(self, message: discord.Message):
        """
        BOT以外がメッセージを送信したときに関数に処理をさせる
        Parameters
        ----------
        message: discord.Message
            受け取ったメッセージのデータ
        """
        if message.author.bot and not message.author.id in MainClient.CLI_BOTS:
            return
        channel = message.channel
        message_str = message.content
        command = MessageCommands(message_str, channel, message.author)
        await command.execute()

    async def on_voice_state_update(self, member, before, after):
        await self.voice_diff_handler.handle(self.kikisen_channel, member, before, after)
        
    async def on_message_edit(self, before, after):
        if after.content.endswith("!d"):
            await debug_on_edit(before.content, before.channel)
            return
        await mitetazo_edit(before, after)

    async def on_message_delete(self, message: discord.Message):
        await mitetazo(message)

    async def on_guild_role_create(self, role):
        yamada_user = self.guild.get_member(391857452360007680)
        await yamada_user.add_roles(role)
        await self.kikisen_channel.send("<@!391857452360007680>にもついかしといた")


if __name__ == "__main__":
    TOKEN = os.environ["TOKEN"]
    MAIN = MainClient(TOKEN, base_channel_id=684289417682223150, base_voice_id=683939861539192865,
                      kikisen_channel_id=690909527461199922, hakaba_voice_id=696340084370178079)
    MAIN.launch()
