from typing import Dict, Union, List

import discord

from src.on_message.commands.commands_manager import CommandsManager

class MessageRoot:
    def __init__(
            self,
            client: discord.Client,
            config: Dict[str, Dict[str, Union[str, int]]]
    ):
        self.commands_manager = CommandsManager(client, config)

    def anarysis_message(
        self,
        message: discord.Message,
    ):
        if message.content[0] == "!":
            self.get_command(message)

    async def get_command(self, message: discord.Message):
        messages: List[str] = message.content.split(" ")
        command: str = messages[0]
        command_instance = self.commands_manager(command)
        if command_instance is None:
            await message.channel.send("commandNotFound")

