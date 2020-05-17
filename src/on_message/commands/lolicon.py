import discord
from src.on_message.commands.util.command_base import CommandBase


class Lolicon(CommandBase):
    MESSAGE_TEMPLATE = "だから僕は{}を辞めた - {} (Music Video)"

    COMMAND = "lolicon"
    COMMAND_TEMPLATE = "{{prefix}}{command}".format(command=COMMAND)
    HELP = "{}\n".format(COMMAND) +\
           "{}の形式のメッセージを送信します".format(
               MESSAGE_TEMPLATE.format(
                   "<message>",
                   "<author>"
               )
           ) + "コマンド:{}".format(COMMAND_TEMPLATE)

    async def execute(self, params: discord.Message):
        messages = params.content.split(" ")
        send_message = " ".join(messages[1:]) if len(messages) >= 2 else ""
        await params.channel(Lolicon.MESSAGE_TEMPLATE.format(
            send_message,
            params.author.display_name
        ))
