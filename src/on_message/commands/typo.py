from typing import Dict, List
import discord

from src.on_message.commands.command_base import CommandBase
from src.on_message.commands.commands_parameter import CommandsParameter


class Typo(CommandBase):
    MESSAGE_HEADER_TEMPLATE = "***†{}の今日のTYPO†***"
    MESSAGE_CONTENT_TEMPLATE = "*・{}*"

    def __init__(self):
        self.typo_dict: Dict[int, List[str]] = {}

    @staticmethod
    def get_command_name():
        return "typo"

    async def execute(self, params: CommandsParameter):
        author_id = params.author_id

        message_send_channel = params.send_channel

        if author_id not in self.typo_dict.keys():
            await message_send_channel.send("test")
            return

        author_name = params.author_name

        await message_send_channel.send(
            Typo.MESSAGE_HEADER_TEMPLATE.format(author_name)
        )

        typo_list = self.typo_dict[author_id]

        for typo in typo_list:
            await message_send_channel.send(
                Typo.MESSAGE_CONTENT_TEMPLATE.format(typo)
            )

    def add_typo(self, message: str, author_id: int):
        if author_id not in self.typo_dict.keys():
            self.typo_dict[author_id] = [message]
            return
        self.typo_dict[author_id].append(message)
