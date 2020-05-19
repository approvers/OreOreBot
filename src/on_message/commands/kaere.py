import datetime
from typing import Dict
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

    INVALID_DATE_FORMAT = "date format is invalid"
    CONFLICT_KAERE_SCHEDULE = "kaere schedule conflict"

    def __init__(
        self,
        root_voice_channel: discord.VoiceChannel,
        afk_voice_channel: discord.VoiceChannel,
        timezone=9,
    ):
        self.timezone = datetime.timezone(datetime.timedelta(hours=timezone))
        self.root_voice_channel = root_voice_channel
        self.afk_voice_channel = afk_voice_channel
        self.schedule: Dict[datetime.time, str] = {}
        self.haracho_voice_state = HarachoVoiceState()

    async def execute(self, params: discord.Message):
        pass

    async def _set_new_schedule(
        self,
        send_message_channel: discord.TextChannel,
        message_author_name: str,
        raw_date: str
    ):
        try:
            time = self._check_date_format(raw_date)
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

    def _join_to_voice_channel(self):
        pass
