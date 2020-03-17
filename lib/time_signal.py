"""
時報を司るもじゅーる
"""
import datetime
import asyncio

import discord

from lib.util import Singleton
from lib.weather import get_weather


class TimeSignal(Singleton):
    """
    時報を操作するClass
    """
    def __init__(self, channel: discord.TextChannel, messages: dict, timezone=9, report_timing=(6, 19)):
        """
        時報に使用する変数の初期化
        Parameters
        ----------
        channel: discord.Channel
            時報を送信するチャンネル
        messages: dict<int, str>
            時報で送信するメッセージを指定する
        timezone: int
            default = UTC+9
            時報で利用するタイムゾーンを指定する
        report_timing: tuple
            天気予報をするタイミングを指定
            0: 今日の天気
            1: 明日の天気
        """
        self.channel = channel
        self.messages = messages
        self.timezone = datetime.timezone(datetime.timedelta(hours=timezone))

        self.weather_report_timing = {
            "today": report_timing[0],
            "tomorrow": report_timing[1]
        }

    async def base(self):
        """
        時報のループ処理を行う関数
        """
        while True:
            time = datetime.datetime.now(tz=self.timezone)

            if time.minute == 0:
                await self.time_signal(time.hour)

            await asyncio.sleep(50)

    async def time_signal(self, hour: int):
        """
        時報を実行する関数
        Parameters
        ----------
        hour: int
            現在の時間
        """
        await self.channel.send(self.messages[str(hour)])

        if hour in self.weather_report_timing.values():
            day = [d for d, v in self.weather_report_timing.items() if v == hour][0]

            weather = get_weather()[day]

            if day == "today":
                await self.report_today(weather)
            else:
                await self.report_tomorrow(weather)

        await asyncio.sleep(15)

    async def report_today(self, weather: dict):
        """
        今日の天気予報
        Parameters
        ----------
        weather: dict
            天気の情報が入った辞書
        """
        await self.channel.send(
            "今日の天気は{}\n最高気温は{}℃で昨日と{}℃違うよ\n最低気温は{}℃で昨日と{}℃違うよ\n今日も頑張ってね"\
            .format(
                weather["weather"],
                weather["high"],
                weather["high_diff"][1:-1],
                weather["low"],
                weather["low_diff"][1:-1]
            )
        )

    async def report_tomorrow(self, weather: dict):
        """
        昨日の天気予報
        Parameters
        ----------
        weather: dict
            天気の情報が入った辞書
        """
        await self.channel.send(
            "昨日の天気は{}\n最高気温は{}℃で今日と{}℃違うよ\n最低気温は{}℃で今日と{}℃違うよ\n今日も一日お疲れ様"\
            .format(
                weather["weather"],
                weather["high"],
                weather["high_diff"][1:-1],
                weather["low"],
                weather["low_diff"][1:-1]
            )
        )

