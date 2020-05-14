import discord

from src.on_message.commands.util.command_base import CommandBase


class Judge(CommandBase):
    EMOJI_KINDS = ["AC", "WA", "TLE", "RE", "CE"]

    def __init__(
        self,
        AC: discord.Emoji,
        WA: discord.Emoji,
        TLE: discord.Emoji,
        RE: discord.Emoji,
        CE: discord.Emoji
    ):
        self.AC = AC
        self.WA = WA
        self.TLE = TLE
        self.RE = RE
        self.CE = CE

    @staticmethod
    def get_command_name():
        return "judge"

    @staticmethod
    def get_help():
        return "judge\n" +\
                "競プロ風にジャッジします\n" +\
                "コマンド:{}".format(Judge.get_command_template())

    @staticmethod
    def get_command_template():
        return "!judge <>"

    async def execute(self, params: discord.Message):
        messages = params.content.split(" ")
        if messages < 2:
            await params.channel.send("invalid parameters")
            return
        raw_judge_number = messages[1]
        judge_result = messages[2] if len(messages) > 3 else "AC"
        try:
            self._check_parameters(raw_judge_number, judge_result)
        except ValueError as e:
            raise e

    def _check_parameters(
        self,
        raw_judge_number: str,
        judge_result: str
    ):
        if not raw_judge_number.isdecimal():
            raise ValueError("judge number have to be unsigned int")

        judge_number = int(raw_judge_number)

        if judge_number > 30:
            raise ValueError("judge number is under 30")

        if judge_result not in Judge.EMOJI_KINDS:
            raise ValueError(
                "judge result is only {}".format(Judge.EMOJI_KINDS)
            )
