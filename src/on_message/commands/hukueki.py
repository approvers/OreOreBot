import discord
from src.on_message.commands.util.command_base import CommandBase


class Hukueki(CommandBase):
    MESSAGE_TEMPLATE = \
        "```" +\
        "ねぇ、将来何してるだろうね\n" +\
        "{}はしてないと良いね" +\
        "困らないでよ{}はしてないといいね" +\
        "```"

    @staticmethod
    def get_command_name():
        return "hukueki"

    @staticmethod
    def get_help():
        return "hukueki\n" +\
                "「S(任意の文字列)はしてないといいね」形式の文字列を返します\n" +\
                "コマンド:{}".format(Hukueki.get_command_template())

    @staticmethod
    def get_command_template():
        return "!hukueki <message>"

    async def execute(self, params: discord.Message):
        messages = params.content.split(" ")
        send_message = " ".join(messages[1:]) if len(messages) >= 2 else ""
        await params.channel(Hukueki.MESSAGE_TEMPLATE.format(send_message))
