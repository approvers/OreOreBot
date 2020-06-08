import difflib
<<<<<<< HEAD
import discord
=======
>>>>>>> 986e4cfffd032159806106082717090a0746078d
from typing import List


class EditNotifier:
    MESSAGE_TEMPLATE = "見てたぞ\n```diff\n{}```"
    DIFF_PAIR_TEMPLATE = "{}\n{}\n{}"
    HORIZONTAL_LINE = "------------------------------\n"

    def notify(
        self,
<<<<<<< HEAD
        before: discord.Message,
        after: discord.Message,
    ):
        before_lines = before.content.split("\n")
        after_lines = after.content.split("\n")
=======
        before: str,
        after: str,
    ):
        before_lines = before.split("\n")
        after_lines = after.split("\n")
>>>>>>> 986e4cfffd032159806106082717090a0746078d

        diff_str = EditNotifier.generateDiff(
            before_lines, after_lines
        )
        if diff_str == "":
            return

        await after.channel.send(
            EditNotifier.MESSAGE_TEMPLATE.format(diff_str)
        )

    @staticmethod
    def generateDiff(
        before_lines: List[str],
        after_lines: List[str]
    ):
        raw_diff = list(difflib.Differ().compare(before_lines, after_lines))
        modified_diff = [x for x in raw_diff if x[:1] in "+-"]

        generated_diff_text = ""
        for i in range(0, len(modified_diff), 2):
            generated_diff_text += EditNotifier.DIFF_PAIR_TEMPLATE.format(
                modified_diff[i],
                modified_diff[i + 1],
                EditNotifier.HORIZONTAL_LINE if (i + 1) != len(modified_diff) else ""
            )

        return generated_diff_text.strip()
