from typing import Dict, Union, List

import discord

from src.on_message.commands.util.commands_manager import CommandsManager
from src.on_message.commands.util.command_base import CommandBase


class MessageRoot:
    PREFIX = "!"
    PREFIX_LENGTH = len(PREFIX)

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
        if message.content[0] == MessageRoot.PREFIX:
            await self.execute_command(message[1:])
            return

        #TODO: 単一責任犯すな
        if "草" in message.content:
            self.commands_manager.message_command[
                "lol_count_up"
            ](message.author.id)
            return

        #TODO: 単一責任犯すな
        if len(message.content) > 3 and message.content[-3:] == "だカス":
            self.commands_manager.message_command[
                "add_typo"
            ](message.content, message.author.id)
            return

    async def execute_command(self, message: discord.Message):
        if len(message.content) == MessageRoot.PREFIX_LENGTH:
            return

        words: List[str] = message.content.split()
        command: str = words[0][MessageRoot.PREFIX_LENGTH:]
        command_instance = self.commands_manager.search_command(command)
        if command_instance is None:
            return

        await command_instance.execute(message)

    #TODO:CommandBaseに移そうぜ
    async def send_help(
            self,
            command: CommandBase,
            send_text_channel: discord.TextChannel
    ):
        help_message = command.HELP
        await send_text_channel.send(help_message)
