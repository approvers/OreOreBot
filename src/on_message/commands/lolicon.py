import discord
from src.on_message.commands.util.command_base import CommandBase


class Lolicon(CommandBase):
    MESSAGE_TEMPLATE = "だから僕は{}を辞めた - {} (Music Video)"

    @staticmethod
    def get_command_name():
        return "lolicon"

    @staticmethod
    def get_help():
        return "lolicon\n" +\
                "{}の形式のメッセージを送信します".format(
                    Lolicon.MESSAGE_TEMPLATE.format(
                        "<message>",
                        "<author>"
                    )
                ) +\
                "コマンド:{}".format(Lolicon.get_command_template())

    @staticmethod
    def get_command_template():
        return "!lolicon <message>"

    async def execute(self, params: discord.Message):
        messages = params.content.split(" ")
        send_message = " ".join(messages[1:]) if len(messages) >= 2 else ""
        await params.channel(Lolicon.MESSAGE_TEMPLATE.format(
            send_message,
            params.author.display_name
        ))
