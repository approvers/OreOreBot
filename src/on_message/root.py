from typing import Dict, Union, List

import discord

from src.on_message.commands.commands_manager import CommandsManager
from src.on_message.commands.command_base import CommandBase


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
            await self.execute_command(message[1:])

        if "草" in message.content:
            self.commands_manager.message_command[
                "lol_count_up"
            ](message.author.id)

        if len(message.content) > 3 and message.content[-3:] == "だカス":
            self.commands_manager.message_command[
                "add_typo"
            ](message.content, message.author.id)

    async def execute_command(self, message: discord.Message):
        messages: List[str] = message.content.split(" ")
        command: str = messages[0][1:]
        command_instance = self.commands_manager(command)
        if command_instance is None:
            await message.channel.send("commandNotFound")
            return

        await command_instance.execute(message)

    async def send_help(
        self,
        command: CommandBase,
        send_text_channel: discord.TextChannel
    ):
        help_message = command.get_help
        await send_text_channel.send(help_message)
