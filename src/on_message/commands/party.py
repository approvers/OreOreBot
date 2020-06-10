from typing import Dict, Callable, List
import random
import os
import asyncio
import datetime

import discord
from mutagen.mp3 import MP3

from src.on_message.commands.util.command_base import CommandBase
from src.haracho_voice_state import HarachoVoiceState


class Party(CommandBase):
    COMMAND = "party"
    COMMAND_TEMPLATE = "{{prefix}}{command} [guerrilla | status | play]"\
        .format(command=COMMAND)
    HELP = "{}".format(COMMAND) + \
           "はらちょがパーティーします\n" + \
           "コマンド:{}".format(COMMAND_TEMPLATE)

    MUSIC_DIR_PATH = "ast/snd/party/"

    STATUS_TEMPLATE = "ゲリラの今の状態は{}だよ"
    PARTY_START = "パーティー Nigth"

    ALREADY_JOIN_TO_VOICE_CHANNEL = "もうVCに接続してるよ"
    SUBCOMMAND_NOTFOUND = "サブコマンドが見つからないよ"
    GUERRILLA_STATUS_SWICHED = "ゲリラの状態を切り替えたよ: {}"
    INVALID_SUBCOMMAND = "そのサブコマンドは無効だよ"

    SUBCOMMAND_TYPE = Callable[[discord.TextChannel], None]

    def __init__(
            self,
            party_channel: discord.VoiceChannel,
            guerrilla_notify_channel: discord.TextChannel
    ):
        self.party_channel = party_channel
        self.guerrilla_notify_channel = guerrilla_notify_channel

        self.haracho_voice_state = HarachoVoiceState()

        self.ready_to_guerrilla = False

        self.subcommand_list: Dict[str, Party.SUBCOMMAND_TYPE] = {
            "status": self._status,
            "guerrilla": self._guerrilla,
            "play": self._play
        }
        self.music_list = Party._load_musics()

        self.guerrilla_timing = random.randint(0, 59)
        self.timezone = 9

        self.loop_guerrilla()

    async def execute(self, params: discord.Message):
        words = params.content.split()
        send_message_channel = params.channel
        if len(words) == 1:
            await send_message_channel.send(Party.SUBCOMMAND_NOTFOUND)
            return

        subcommand = words[1]

        if subcommand not in self.subcommand_list.keys():
            await send_message_channel.send(Party.INVALID_SUBCOMMAND)
            return
        self.subcommand_list[subcommand](params.channel)

    async def _status(self, send_message_channel: discord.TextChannel):
        await send_message_channel.send(
            Party.STATUS_TEMPLATE.format(self.ready_to_guerrilla)
        )

    async def _guerrilla(self, send_message_channel: discord.TextChannel):
        self.ready_to_guerrilla = not self.ready_to_guerrilla
        await send_message_channel.send(
            Party.GUERRILLA_STATUS_SWICHED.format(
                self.ready_to_guerrilla
            )
        )

    async def _play(self, send_message_channel: discord.TextChannel):
        chosen_music = Party.MUSIC_DIR_PATH + random.choice(self.music_list)

        try:
            self.haracho_voice_state.turnOnVoiceState()
        except RuntimeError:
            await send_message_channel.send(
                Party.ALREADY_JOIN_TO_VOICE_CHANNEL
            )
        voice_client = await self.party_channel.connect(reconnect=False)
        voice_client.play(discord.FFmpegAudio(chosen_music))

        await send_message_channel.send(Party.PARTY_START)

        music_length = MP3(chosen_music).info.length
        await asyncio.sleep(music_length + 0.5)
        await voice_client.disconnect(force=True)

        self.haracho_voice_state.turnOffVoiceState()

    async def loop_guerrilla(self):
        while True:
            now_minute = datetime.datetime.now().minute
            if now_minute == self.guerrilla_timing and self.ready_to_guerrilla:
                await self._play(self.guerrilla_notify_channel)
            await asyncio.sleep(50)

    @staticmethod
    def _load_musics() -> List[str]:
        files = os.listdir(Party.MUSIC_DIR_PATH)
        return files
