from typing import Dict, Union, List

import discord

from src.on_message.commands.commands_manager import CommandsManager
from src.on_message.commands.commands_parameter import CommandsParameter


class MessageRoot:
    def __init__(
            self,
            client: discord.Client,
            config: Dict[str, Dict[str, Union[str, int]]]
    ):
        self.commands_manager = CommandsManager(client, config)

    async def anarysis_message(
        self,
        message: discord.Message,
    ):
        if message.content[0] == "!":
            await self.get_command(message[1:])

    async def get_command(self, message: discord.Message):
        messages: List[str] = message.content.split(" ")
        command: str = messages[0][1:]
        command_instance = self.commands_manager(command)
        if command_instance is None:
            await message.channel.send("commandNotFound")
        command_param = CommandsParameter(
            author_id=message.author.id,
            author_name=message.author.display_name,
            send_channel=message.channel,
            message=message.content
        )
        await command_instance.execute(command_param)
