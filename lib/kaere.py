"""
Kaere関連の処理をする
"""

import discord
import asyncio
import datetime

from lib.util import Singleton

class Kaere(Singleton):
    """
    Kaereを司るクラス
    """

    def __init__(self, voice_channel, text_channel, hakaba_voice_channel):
        """
        初期化処理
        Parameters
        ----------
        main_voice_channel: discord.TextChannel
            メインのボイスチャンネルkaereが実行されるチャンネル
        textn_channel: discord.VoiceChannel
            聞き専チャンネルkaereのメッセージが送信されるチャンネル
        """
        self.timezone       = datetime.timezone(datetime.timedelta(hours=9))
        self.voice_channel  = voice_channel
        self.text_channel   = text_channel
        self.hakaba_voice_channel = hakaba_voice_channel

        self.kaere_do_dict = {} # {str:discord.User}
        self.do_disconnect = False
        self.is_doing = False

    async def command_controller(self, commands, member_name):
        commands.pop(0)

        if len(commands) == 0:
            await self.do(is_not_list=False)
            return

        if commands[0] == "set":
            if len(commands) < 2:
                await self.text_channel.send("お知らせしてほしい時間を`!kaere set HHMM`の形式でおしえてね")
                return
            if not await self.time_valid(commands[1]):
                return
            if commands[1] in self.kaere_do_dict:
                await self.text_channel.send("その時間はもうお知らせする予定だよ")
                return
            await self.text_channel.send("{}におしらせするね".format(commands[1]))
            self.kaere_do_dict[commands[1]] = member_name
            return

        if commands[0] == "list":
            if len(self.kaere_do_dict) == 0:
                await self.text_channel.send("まだお知らせする予定はないよ")
                return
            display_text = "***蛍の光予約一覧***\n"
            for do_time, member_in in self.kaere_do_dict.items():
                print(do_time)
                display_text += ("***・{}時{}分*** ({})\n").format(do_time[0:2], do_time[2:4], member_in)
            await self.text_channel.send("お知らせする時間のリストだよ\n" + display_text)
            return

        if commands[0] == "remove":
            if len(commands) < 2:
                await self.text_channel.send("お知らせをキャンセルしたい時間を`!kaere remove HHMM`の形式でおしえてね")
                return
            if not await self.time_valid(commands[1]):
                return
            if not commands[1] in self.kaere_do_dict.keys():
                await self.text_channel.send("その時間にお知らせする予定はないよ")
                return
            self.kaere_do_dict.pop(commands[1])
            await self.text_channel.send("{}のお知らせをキャンセルしたよ".format(commands[1]))
            return

        if commands[0] == "force":
            if self.do_disconnect:
                self.do_disconnect = False
                await self.text_channel.send("強制切断をオフにしたよ")
            else:
                self.do_disconnect = True
                await self.text_channel.send("強制切断をオンにしたよ")

    async def time_valid(self,check_str):
        try:
            is_ok = ((0 <= int(check_str[0:2]) <= 23) and (0 <= int(check_str[2:4]) < 60)) and (len(check_str) == 4)
            if not is_ok:
                await self.text_channel.send("そんな時間は存在しないよ...？")
                return False
        except:
            await self.text_channel.send("そんな時間は存在しないよ...？")
            return False
        return True

    async def base(self):
        """
        ゲリラのループ処理を行う関数
        """
        while True:
            time = datetime.datetime.now(tz=self.timezone).strftime("%H%M")
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
            for member in self.voice_channel.members:
                await member.move_to(channel=self.hakaba_voice_channel, reason="†***R.I.P.***† ***安らかに眠れ***")
                await asyncio.sleep(0.50)
        await voice_client.disconnect(force=True)
        self.is_doing = False
