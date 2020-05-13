from typing import List

import discord

from src.on_message.commands.command_base import CommandBase


class Haracyo(CommandBase):
    MESSAGE_TEMPLATE = "このBOTのコマンドの一覧です\n`{}`"

    def __init__(self, commands: List[str]):
        self.commands = commands

    @staticmethod
    def get_command_name():
        return "haracyo"

    @staticmethod
    def get_help():
        return "haracyo" +\
                "このBotのコマンド一覧を表示します\n{}".format(Haracyo.COMMANDS) + \
                "{}".format(Haracyo.get_command_template())

    @staticmethod
    def get_command_template():
        return "!haracyo"

    async def execute(self, params: discord.Message):
        await params.channel.send(
            Haracyo.MESSAGE_TEMPLATE.format(self.MESSAGE_TEMPLATE)
        )
