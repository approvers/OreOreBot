from typing import Dict, Union, List

import discord

from src.on_message.commands.util.commands_manager import CommandsManager
from src.on_message.commands.util.command_base import CommandBase


class MessageRoot:
    def __init__(
            self,
            client: discord.Client,
            config: Dict[str, Dict[str, Union[str, int]]]
    ):
        self.commands_root = CommandsRoot(client, config)

    async def anarysis_message(
            self,
            message: discord.Message,
    ):
        if message.content[0] == CommandsRoot.PREFIX:
            await self.commands_root.execute_command(message)
            return

class CommandsRoot:
    PREFIX = "!"
    PREFIX_LENGTH = len(PREFIX)

    def __init__(
            self,
            client: discord.Client,
            config: Dict[str, Dict[str, Union[str, int]]]
    ):
        self.commands_manager = CommandsManager(client, config)

    async def execute_command(self, message: discord.Message):
        if len(message.content) == CommandsRoot.PREFIX_LENGTH:
            return

        words: List[str] = message.content.split()
        command: str = words[0][CommandsRoot.PREFIX_LENGTH:]
        command_instance = self.commands_manager.search_command(command)
        if command_instance is None:
            return
        if self._judge_help(words):
            command_instance.send_help(
                message.channel,
                CommandsRoot.PREFIX
            )

        await command_instance.execute(message)

    async def _judge_help(
            self,
            words: List[str]
    ) -> bool:
        return len(words) > 1 and words[1] == "help"
