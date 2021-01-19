import datetime
from typing import Dict
import asyncio

import discord

from src.on_message.commands.util.command_base import CommandBase
from src.haracho_voice_state import HarachoVoiceState


class Kaere(CommandBase):
    COMMAND = "kaere"
    COMMAND_TEMPLATE = "{{prefix}}{command} <mode> (<time>)"\
                       .format(command=COMMAND)
    HELP = "{}".format(COMMAND) + \
           "無能ボイスで帰宅を催促します\n" + \
           "コマンド:{}".format(COMMAND_TEMPLATE)

    CREATE_SCHEDULE_SUCCESS = "{}にお知らせするよ"
    REMOVE_SCHEDULE_SUCCESS = "{}のkaereを削除するよ"

    LIST_TITLE_FORMAT = "***蛍の光予約一覧***\n{}"
    LIST_CONTENT_FORMAT = "***・{}*** ({})\n"

    INVALID_DATE_FORMAT = "日付の形式が間違ってるよ`HH:MM`で指定してね"
    CONFLICT_KAERE_SCHEDULE = "その時間は既に指定されてるよ"
    INVALID_SET_ARGS = "セットする時間を教えてね"
    SCHEDUlE_NOT_FOUND = "まだお知らせする予定はないよ"
    INVALID_REMOVE_ARGS = "削除する時間を教えてね"

    def __init__(
        self,
        error_notify_channel: discord.TextChannel,
        root_voice_channel: discord.VoiceChannel,
        afk_voice_channel: discord.VoiceChannel,
        haracho_member: discord.Member,
        timezone=9,
    ):
        self.timezone = datetime.timezone(datetime.timedelta(hours=timezone))
        self.error_notify_channel = error_notify_channel
        self.root_voice_channel = root_voice_channel
        self.afk_voice_channel = afk_voice_channel
        self.schedule: Dict[datetime.time, str] = {}
        self.haracho_member = haracho_member
        self.haracho_voice_state = HarachoVoiceState()
        self._execute_scheduled_kaere()

    async def execute(self, params: discord.Message):
        words = params.content.split()
        send_message_channel = params.channel

        author = params.author

        if len(words) == 1:
            await self._kaere(send_message_channel)
            return

        command = words[1]
        if command == "set":
            if len(words) < 2:
                await send_message_channel.send(Kaere.INVALID_SET_ARGS)
                return

            time = words[2]
            await self._set_new_schedule(send_message_channel, author, time)
            return

        if command == "list":
            await self._list_schedule(send_message_channel)
            return

        if command == "remove":
            if len(words) < 2:
                await send_message_channel.send(Kaere.INVALID_REMOVE_ARGS)
                return
            time = words[2]
            await self._remove_schedule(send_message_channel, time)

    async def _set_new_schedule(
        self,
        send_message_channel: discord.TextChannel,
        message_author_name: str,
        raw_time: str
    ):
        try:
            time = self._check_date_format(raw_time)
        except ValueError:
            await send_message_channel.send(Kaere.INVALID_DATE_FORMAT)
            return

        if time in self.schedule.keys():
            await send_message_channel.send(Kaere.CONFLICT_KAERE_SCHEDULE)
            return

        await send_message_channel.send(
            Kaere.CREATE_SCHEDULE_SUCCESS.format(
                str(time)
            )
        )
        self.schedule[time] = message_author_name

    def _check_date_format(self, raw_date: str) -> datetime.time:
        return datetime.datetime.strptime(raw_date, "%H:%M").time()

    async def _remove_schedule(
        self,
        send_message_channel: discord.TextChannel,
        raw_date: str
    ):
        try:
            time = self._check_date_format(raw_date)
        except ValueError:
            await send_message_channel.send(Kaere.INVALID_DATE_FORMAT)
            return

        if time not in self.schedule.keys():
            return
        self.schedule.pop(time)
        await send_message_channel.send(Kaere.REMOVE_SCHEDULE_SUCCESS)

    async def _list_schedule(
        self,
        send_message_channel: discord.TextChannel
    ):
        if len(self.schedule) == 0:
            await send_message_channel.send(Kaere.SCHEDUlE_NOT_FOUND)
            return

        sorted_schedule = sorted(self.schedule.items(), key=lambda x: x[0])

        contents = ""
        for time, name in sorted_schedule:
            contents += Kaere.LIST_CONTENT_FORMAT.format(str(time), name)
        await send_message_channel.send(
            Kaere.LIST_TITLE_FORMAT.format(
                contents
            )
        )

    async def _kaere(self, send_notify_channel: discord.TextChannel):
        try:
            self.haracho_voice_state.turnOnVoiceState()
        except RuntimeError:
            await send_notify_channel.send("")

        voice_client = await self.root_voice_channel.connect(reconnect=False)
        voice_client.play(discord.FFmpegAudio(source="ast/snd/neroyo.mp3"))

        for _ in range(20):
            if not voice_client.is_connected():
                await voice_client.disconnect(force=True)
                self.haracho_voice_state.turnOffVoiceState()
            await asyncio.sleep(5)

        if voice_client.is_connected():
            await voice_client.disconnect(force=True)
            self.haracho_voice_state.turnOffVoiceState()

    async def _execute_scheduled_kaere(self):
        while True:
            time = datetime.datetime.now(tz=self.timezone)
            time = datetime.time(hour=time.hour, minute=time.minute)
            if time in self.schedule.keys():
                self.schedule.pop(time)
                await self._kaere(self.error_notify_channel)
