import discord

from src.on_message.commands.util.command_base import CommandBase


class Debug(CommandBase):
    COMMAND = "debug"
    COMMAND_TEMPLATE = "{{prefix}}{command}".format(command=COMMAND)
    HELP = "{}".format(COMMAND) + \
           "メッセージの実態を表示します" + \
           "コマンド: {}".format(COMMAND_TEMPLATE)

    DEBUG_TEMPLATE = "これがメッセージの実態だよ\n```{}```"

    async def execute(self, params: discord.Message):
        message = params.content.replace("`", "'")
        send_message_channel = params.channel
        await send_message_channel.send(Debug.DEBUG_TEMPLATE.format(message))
