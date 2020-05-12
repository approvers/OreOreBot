from typing import List, Dict
import discord

from src.on_message.commands.command_base import CommandBase
from src.on_message.commands.commands_parameter import CommandsParameter


class LoL(CommandBase):
    MESSAGE_HEADER_TEMPLATE = "***{}'s GRASS COUNT***"
    MESSAGE_CONTENT_TEMPLATE = "・{}"

    def __init__(self):
        self.lol_dict: Dict[int, List[str]] = {}

    @staticmethod
    def get_command_name():
        return "lol"

    @staticmethod
    def get_require_params():
        return ["author_id", "author_name", "message_send"]

    def execute(self, params: CommandsParameter):
        author_id = params.author_id

        author_name = params.author_name

        message_send_channel = params.send_channel

        if author_id not in self.lol_count.keys():
            LoL.message_send("test", message_send_channel)
            return

        lol_count = self.lol_dict[author_id]

        LoL.notify_lol_count(author_name, lol_count, message_send_channel)

    @staticmethod
    async def notify_lol_count(
        author: str,
        messages: List[str],
        text_channel: discord.TextChannel
    ):
        await LoL.message_send(
            LoL.MESSAGE_HEADER_TEMPLATE.format(author),
            text_channel
        )

        for message in messages:
            await LoL.message_send(
                LoL.MESSAGE_CONTENT_TEMPLATE.format(message),
                text_channel
            )

    @staticmethod
    async def message_send(message: str, text_channel: discord.TextChannel):
        await text_channel.send(message)
