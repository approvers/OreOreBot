import asyncio
import random
from typing import List

import discord

from src.on_message.commands.util.command_base import CommandBase


class Judge(CommandBase):
    COMMAND = "judge"
    COMMAND_TEMPLATE = "{{prefix}}{command} <number> (<judge_result(emoji)>)".format(command=COMMAND)
    HELP = "{}\n".format(COMMAND) +\
           "競プロ風にジャッジします\n" +\
           "コマンド:{}".format(COMMAND_TEMPLATE)

    JUDGE_COUNT_LIMIT = 30
    JUDGE_START_MESSAGE = "***HARACHO ONLINE JUDGEMENT SYSTEM***"
    JUDGE_MESSAGE_TEMPLATE = "{}/{} {}"

    def __new__(
        cls,
        AC: discord.Emoji,
        WA: discord.Emoji,
        TLE: discord.Emoji,
        RE: discord.Emoji,
        CE: discord.Emoji
    ):
        

    def __init__(
            self,
            AC: discord.Emoji,
            WA: discord.Emoji,
            TLE: discord.Emoji,
            RE: discord.Emoji,
            CE: discord.Emoji
    ):
        self.EMOJI_DICT = {
            "AC": AC,
            "WA": WA,
            "TLE": TLE,
            "RE": RE,
            "CE": CE
        }

    async def execute(self, params: discord.Message):
        messages = params.content.split(" ")
        send_message_channel: discord.TextChannel = params.channel
        if messages < 2:
            await params.channel.send("invalid parameters")
            return
        raw_judge_number = messages[1]
        judge_result = messages[2] if len(messages) > 3 else "AC"

        try:
            self._check_parameters(
                raw_judge_number,
                judge_result,
                list(self.EMOJI_DICT.keys())
            )
        except ValueError as value_error:
            await send_message_channel.send(value_error)

        judge_number = int(raw_judge_number)

        await send_message_channel.send(Judge.JUDGE_START_MESSAGE)

        await asyncio.sleep(1)

        await Judge._send_judge(
            judge_number,
            judge_result,
            send_message_channel,
            self.EMOJI_DICT[judge_result]
        )

    @staticmethod
    async def _send_judge(
            judge_number: int,
            judge_result: str,
            send_message_channel: discord.TextChannel,
            send_role: discord.Role
    ):
        channge_timing = random.randint(1, judge_number)
        message: discord.Message = Judge.generate_first_message(
            judge_number,
            judge_result,
            send_message_channel
        )
        for i in range(2, channge_timing):
            await message.edit(content=Judge.JUDGE_MESSAGE_TEMPLATE.format(
                i,
                judge_number,
                "WJ"
            ))
            await asyncio.sleep(1)

        for i in range(channge_timing, judge_number + 1):
            await message.edit(
                content=Judge.JUDGE_MESSAGE_TEMPLATE.format(
                    i,
                    judge_number,
                    judge_result
                )
            )
            await asyncio.sleep(1)
        await send_message_channel.send(send_role)

    @staticmethod
    async def generate_first_message(
            judge_number: int,
            judge_result: str,
            send_message_channel: discord.TextChannel
    ) -> discord.Message:
        if judge_number == 1:
            return await send_message_channel.send(
                Judge.JUDGE_MESSAGE_TEMPLATE.format(
                    1,
                    judge_number,
                    judge_result
                    )
                )
        return await send_message_channel.send(
            Judge.JUDGE_MESSAGE_TEMPLATE.format(
                1,
                judge_number,
                "WJ"
            )
        )

    @staticmethod
    def _check_parameters(
            raw_judge_number: str,
            judge_result: str,
            emoji_kind: List[str]
    ):
        if not raw_judge_number.isdecimal():
            raise ValueError("judge number have to be unsigned int")

        judge_number = int(raw_judge_number)

        if judge_number > Judge.JUDGE_COUNT_LIMIT:
            raise ValueError("judge number is under 30")

        if judge_result not in emoji_kind:
            raise ValueError(
                "judge result is only {}".format(emoji_kind)
            )
