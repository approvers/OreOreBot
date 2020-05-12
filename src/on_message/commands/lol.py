from typing import List, Dict
import discord

from src.on_message.commands.command_base import CommandBase
from src.on_message.commands.commands_parameter import CommandsParameter


class LoL(CommandBase):
    MESSAGE_HEADER_TEMPLATE = "***今日は草って{}回言ってるね***"

    def __init__(self):
        self.lol_dict: Dict[int, int] = {}

    @staticmethod
    def get_command_name():
        return "lol"

    @staticmethod
    def get_require_params():
        return ["author_id", "author_name", "message_send"]

    async def execute(self, params: CommandsParameter):
        author_id = params.author_id

        author_name = params.author_name

        message_send_channel = params.send_channel

        if author_id not in self.lol_count.keys():
            await message_send_channel.send("test")
            return

        lol_count = self.lol_dict[author_id]

        await message_send_channel.send(
            LoL.MESSAGE_HEADER_TEMPLATE.format(author_name)
        )

        await message_send_channel.send(
            LoL.MESSAGE_CONTENT_TEMPLATE.format(lol_count)
        )

    @staticmethod
    async def message_send(message: str, text_channel: discord.TextChannel):
        await text_channel.send(message)
