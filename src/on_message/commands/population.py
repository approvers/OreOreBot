import discord
from src.on_message.commands.util.command_base import CommandBase


class Population(CommandBase):
    MESSAGE_TEMPLATE = "***†只今の限界開発鯖の人口†***\n" +\
                        "```\n" +\
                        "・通常ユーザー: {} 人\n" +\
                        "・Botユーザー: {} 人\n" +\
                        "・Bot率: {}%```"

    @staticmethod
    def get_command_name():
        return "population"

    @staticmethod
    def get_help():
        return "population\n" +\
            "サーバーの人口を表示します" +\
            "コマンド:{}".format(Population.get_command_template())

    @staticmethod
    def get_command_template():
        return "!population"

    async def execute(self, params: discord.Message):
        guild: discord.Guild = params.guild
        all_users = guild.members
        bots = len([v for v in all_users if v.bot])
        users = len(all_users) - bots

        await params.channel.send(
            Population.MESSAGE_TEMPLATE.format(
                users,
                bots,
                bots / users
            )
        )
