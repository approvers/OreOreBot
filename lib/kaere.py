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

        self.kaere_schedule = {}  # {str:discord.User.display_name}
        self.do_disconnect = False
        self.is_doing = False

    async def command_controller(self, commands, member_name):
        """
        !kaereの根幹部分です
        Param
        -----
        commands: list[str]
            ユーザーが入力した文字列を半角スペースで分割したものが入ります
        member_name: str
            ユーザーの名前が入ります
        """
        commands.pop(0)

        if len(commands) == 0:
            await self.execute(is_auto=False)
            return

        command = commands[0]

        if command == "set":
            if len(commands) < 2:
                await self.text_channel.send("お知らせしてほしい時間を`!kaere set HH:MM`の形式でおしえてね")
                return

            time = commands[1]
            await self.kaere_set(time, member_name)
            return

        if command == "list":
            await self.scheduled_kaere_list()
            return

        if command == "remove":
            if len(commands) < 2:
                await self.text_channel.send("お知らせをキャンセルしたい時間を`!kaere remove HH:MM`の形式でおしえてね")
                return
            time = commands[1]
            await self.schedule_time_remove(time)
            return

        if command == "force":
            if self.do_disconnect:
                await self.text_channel.send("強制切断をオフにしたよ")
            else:
                await self.text_channel.send("強制切断をオンにしたよ")
            self.do_disconnect = not self.do_disconnect

    async def schedule_time_remove(self, raw_time):
        """
        予定されている!kaereをキャンセルする
        """
        try:
            time = self.str_to_time(raw_time)
        except ValueError:
            await self.text_channel.send("そんな時間は存在しないよ...？")
            return

        if time in self.kaere_schedule:
            self.kaere_schedule.pop(time)
            await self.text_channel.send("{}のお知らせをキャンセルしたよ".format(str(time)[0:5]))
            return

        await self.text_channel.send("その時間にお知らせする予定はないよ")

    async def scheduled_kaere_list(self):
        """
        予定されている!kaereのリストを送信する
        """
        if len(self.kaere_schedule) == 0:
            await self.text_channel.send("まだお知らせする予定はないよ")
            return

        display_text = "***蛍の光予約一覧***\n"
        sorted_dict = sorted(self.kaere_schedule.items(), key=lambda a: a[0])

        for schedule_time, member_name in sorted_dict:
            display_text += ("***・{}*** ({})\n").format(str(schedule_time)[0:5], member_name)
        await self.text_channel.send("お知らせする時間のリストだよ\n" + display_text)

    async def kaere_set(self, raw_time, member_name):
        """
        !kaereを予約する
        Param
        -----
        raw_time: str
            変換前の時間の文字列
        member_name: str
            リクエストしたメンバーの名前
        """
        try:
            time = self.str_to_time(raw_time)
        except ValueError:
            await self.text_channel.send("そんな時間は存在しないよ...？")
            return

        if time in self.kaere_schedule:
            await self.text_channel.send("その時間はもうお知らせする予定だよ")
            return

        await self.text_channel.send("{}におしらせするね".format(str(time)[0:5]))
        self.kaere_schedule[time] = member_name

    def str_to_time(self, time: str):
        """
        Param
        -----
        time: str
            時間であるかチェックする文字列

        Return
        ------
        time: datetime.time
            時間のフォーマットに合っているかの真理値
        """
        return datetime.datetime.strptime(time, "%H:%M").time()

    async def base(self):
        """
        蛍の光のループ処理を行う関数
        """
        while True:
            time = datetime.datetime.now(tz=self.timezone)
            time = datetime.time(hour=time.hour, minute=time.minute)
            if time in self.kaere_schedule.keys():
                self.kaere_schedule.pop(time)
                await self.execute(is_auto=True)
            await asyncio.sleep(50)

    async def execute(self, is_auto):
        """
        実際にkaereを実行する
        """
        if self.is_doing:
            await self.text_channel.send("もう実行されてるよ")
            return
        try:
            self.is_doing = True
            voice_client = await self.voice_channel.connect(reconnect=False)
            voice_client.play(discord.FFmpegPCMAudio(source="ast/snd/neroyo.mp3"))
            if self.do_disconnect and is_auto:
                await self.text_channel.send("アナウンスの終了後、強制切断するナリ")

            for _ in range(20):
                if not voice_client.is_connected():
                    self.is_doing = False
                    await voice_client.disconnect(force=True)
                    return
                await asyncio.sleep(5)

            if self.do_disconnect and is_auto:
                await voice_client.disconnect(force=True)
                await asyncio.sleep(0.50)
                for member in self.voice_channel.members:
                    await member.move_to(
                        channel=self.hakaba_voice_channel,
                        reason="†***R.I.P.***† ***安らかに眠れ***"
                    )
                    await asyncio.sleep(0.50)

            if voice_client.is_connected():
                await voice_client.disconnect(force=True)

        except discord.errors.ClientException:
            await self.text_channel.send("もう実行されてるよ")
        except Exception as e:
            await self.text_channel.send("例外が発生したよ\n内容は{}だよ".format(e))

