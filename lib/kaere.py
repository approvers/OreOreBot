"""
Kaere関連の処理をする
"""

import discord
import asyncio
import datetime

from lib.util import Singleton

class Kaere(Singleton):
    """
    !kaere関連の処理を司るクラス
    """

    def __init__(self, voice_channel, text_channel, hakaba_voice_channel):
        """
        初期化処理を行う
        Parameters
        ----------
        voice_channel: discord.VoiceChannel
            メインのボイスチャンネルkaereが実行される
        text_channel: discord.TextChannel
            聞き専チャンネルkaereに関するメッセージが送信される
        hakaba_voice_channel: discord.VoiceChannel
            墓場のボイスチャンネル 設定によって実行後ここに強制移動させられる
        """
        self.timezone = datetime.timezone(datetime.timedelta(hours=9))
        self.voice_channel = voice_channel
        self.text_channel = text_channel
        self.hakaba_voice_channel = hakaba_voice_channel

        self.kaere_do_dict = {}  # {str:discord.User.display_name}
        self.do_disconnect = False
        self.is_doing = False

    async def command_controller(self, commands, member_name):
        commands.pop(0)

        if len(commands) == 0:
            await self.do(is_not_list=False)
            return

        if commands[0] == "set":
            if len(commands) < 2:
                await self.text_channel.send("お知らせしてほしい時間を`!kaere set HH:MM`の形式でおしえてね")
                return
            if not await self.time_controller(commands[1]):
                return
            if datetime.datetime.strptime(commands[1], "%H:%M").time() in self.kaere_do_dict:
                await self.text_channel.send("その時間はもうお知らせする予定だよ")
                return
            await self.text_channel.send("{}におしらせするね".format(str(datetime.datetime.strptime(commands[1], "%H:%M").time())[0:5]))
            self.kaere_do_dict[datetime.datetime.strptime(commands[1], "%H:%M").time()] = member_name
            return

        if commands[0] == "list":
            if len(self.kaere_do_dict) == 0:
                await self.text_channel.send("まだお知らせする予定はないよ")
                return
            display_text = "***蛍の光予約一覧***\n"
            for do_time, member_in in self.kaere_do_dict.items():
                display_text += ("***・{}*** ({})\n").format(str(do_time)[0:5], member_in)
            await self.text_channel.send("お知らせする時間のリストだよ\n" + display_text)
            return

        if commands[0] == "remove":
            if len(commands) < 2:
                await self.text_channel.send("お知らせをキャンセルしたい時間を`!kaere remove HH:MM`の形式でおしえてね")
                return
            if not await self.time_controller(commands[1]):
                return
            if not (datetime.datetime.strptime(commands[1], "%H:%M").time() in self.kaere_do_dict):
                await self.text_channel.send("その時間にお知らせする予定はないよ")
                return
            self.kaere_do_dict.pop(datetime.datetime.strptime(commands[1], "%H:%M").time())
            await self.text_channel.send("{}のお知らせをキャンセルしたよ".format(str(datetime.datetime.strptime(commands[1], "%H:%M").time())[0:5]))
            return

        if commands[0] == "force":
            if self.do_disconnect:
                self.do_disconnect = False
                await self.text_channel.send("強制切断をオフにしたよ")
            else:
                self.do_disconnect = True
                await self.text_channel.send("強制切断をオンにしたよ")

    async def time_controller(self, checker):
        try:
            datetime.datetime.strptime(checker, "%H:%M").time()
            return True
        except:
            await self.text_channel.send("そんな時間は存在しないよ...？")
            return False

    async def base(self):
        """
        蛍の光のループ処理を行う関数
        """
        while True:
            time = datetime.datetime.now(tz=self.timezone)
            time = datetime.time(hour=time.hour, minute=time.minute)
            if time in self.kaere_do_dict.keys():
                self.kaere_do_dict.pop(time)
                await self.do(is_not_list=True)
            await asyncio.sleep(50)

    async def do(self,is_not_list):
        """
        実際にkaereを実行する
        """
        if self.is_doing:
            return
        self.is_doing = True
        voice_client = await self.voice_channel.connect(reconnect=False)
        voice_client.play(discord.FFmpegPCMAudio(source="ast/snd/neroyo.mp3"))
        if self.do_disconnect and is_not_list:
            await self.text_channel.send("アナウンスの終了後、強制切断するナリ")
        await asyncio.sleep(100)
        if self.do_disconnect and is_not_list:
            await voice_client.disconnect(force=True)
            await asyncio.sleep(0.50)
            for member in self.voice_channel.members:
                await member.move_to(channel=self.hakaba_voice_channel, reason="†***R.I.P.***† ***安らかに眠れ***")
                await asyncio.sleep(0.50)
        self.is_doing = False
