from typing import Dict

from src.on_message.commands.util.command_base import CommandBase
from src.on_message.commands.util.commands_parameter import CommandsParameter


class LoL(CommandBase):
    COMMAND = "lol"
    COMMAND_TEMPLATE = "!{}".format(COMMAND)
    HELP = "{}\n".format(COMMAND) +\
           "草って言った回数をカウントします\n" +\
           "コマンド: {}".format(COMMAND_TEMPLATE)

    MESSAGE_CONTENT_TEMPLATE = "***今日は草って{}回言ってるね***"

    def __init__(self):
        self.lol_dict: Dict[int, int] = {}

    async def execute(self, params: CommandsParameter):
        author_id = params.author_id

        message_send_channel = params.send_channel

        if author_id not in self.lol_dict.keys():
            await message_send_channel.send("test")
            return

        lol_count = self.lol_dict[author_id]

        await message_send_channel.send(
            LoL.MESSAGE_CONTENT_TEMPLATE.format(lol_count)
        )

    def lol_count_up(self, author_id: int):
        if author_id not in self.lol_dict.keys():
            self.lol_dict[author_id] = 1
            return
        self.lol_dict[author_id] += 1
