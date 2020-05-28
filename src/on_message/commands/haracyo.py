from typing import List

import discord

from src.on_message.commands.util.command_base import CommandBase


class Haracyo(CommandBase):
    COMMAND = "haracyo"
    COMMAND_TEMPLATE = "{{prefix}}{command}".format(command=COMMAND)
    HELP = "{}".format(COMMAND) +\
           "このBotのコマンド一覧を表示します\n" + \
           "コマンド:{}".format(COMMAND_TEMPLATE)

    MESSAGE_TEMPLATE = "このBOTのコマンドの一覧です\n`{}`"

    def __init__(self, commands: List[str]):
        self.commands = commands

    async def execute(self, params: discord.Message):
        await params.channel.send(
            Haracyo.MESSAGE_TEMPLATE.format(self.commands)
        )
