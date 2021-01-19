from typing import List
import re
import discord

from src.on_message.commands.util.command_base import CommandBase
from src.on_message.commands.util.commands_parameter import CommandsParameter


class Role(CommandBase):
    COMMAND = "role"
    COMMAND_TEMPLATE = \
        "{{prefix}}{command} <target_user_id> <new_role_name> (<color>)" \
        .format(command=COMMAND)
    HELP = "role\n" + \
           "roleを作成して自動で付与する\n" + \
           "コマンド: {}".format(
               COMMAND_TEMPLATE
           ) + "colorは#から始まる6桁の16進数"

    REASON_TEMPLATE = "Created by {}"
    SEND_MESSAGE_TEMPLATE = "<@&{}>を作成して<@!{}>に付与しました！"

    async def execute(self, params: CommandsParameter):
        messages: List[str] = params.author_name.split(" ")
        command_length = len(messages)

        message_send_channel = params.send_channel
        if command_length < 3:
            await message_send_channel.send("引数が少なすぎます。")
            return

        if not messages[1].isdecimal():
            await message_send_channel.send("ユーザIDは数値で指定してください。")
            return

        target_user: discord.Member = message_send_channel.guild \
            .get_member(int(messages[1]))

        role_name = messages[2]

        if target_user is None:
            await message_send_channel.send("ユーザーがいないです。")
            return

        if command_length == 3:
            color = discord.Color.default()
        else:
            try:
                color = self.get_color(messages[3])
            except ValueError:
                await message_send_channel.send("カラーコードが変です。")
                return

        new_role = await message_send_channel.guild.create_role(
            name=role_name,
            color=color,
            reason=Role.REASON_TEMPLATE.format(params.author_name),
            mentionable=True
        )

        await target_user.add_roles(new_role)

        await message_send_channel.send(
            Role.SEND_MESSAGE_TEMPLATE.format(
                new_role.id, target_user.id
            )
        )

    def get_color(self, raw_color_code: str) -> discord.Color:
        if not raw_color_code.startswith("#") or len(raw_color_code) != 7:
            raise ValueError("invalid color code patarn")

        color_code = raw_color_code[1:]
        m = re.match(r"[0-9A-Fa-f]", color_code)
        if not m:
            raise ValueError("invalid Hexadecimal patarn")
        red = int(color_code[0:2], 16)
        green = int(color_code[2:4], 16)
        blue = int(color_code[4:6], 16)

        return discord.Color.from_rgb(red, green, blue)
