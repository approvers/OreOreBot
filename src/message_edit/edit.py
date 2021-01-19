import difflib
import discord
from typing import List


MESSAGE_TEMPLATE = "見てたぞ\n```diff\n{}```"
DIFF_PAIR_TEMPLATE = "{}\n{}\n{}"
HORIZONTAL_LINE = "------------------------------\n"


async def notify_message_edit(
    before: discord.Message,
    after: discord.Message,
):
    before_lines = before.content.split("\n")
    after_lines = after.content.split("\n")
    diff_str = generateDiff(
        before_lines, after_lines
    )
    if diff_str == "":
        return

    await after.channel.send(
        MESSAGE_TEMPLATE.format(diff_str)
    )


def generateDiff(
    before_lines: List[str],
    after_lines: List[str]
):
    raw_diff = list(difflib.Differ().compare(before_lines, after_lines))

    diff_dict = {
        "+": [x for x in raw_diff if x[:1] == "+"],
        "-": [x for x in raw_diff if x[:1] == "-"],
    }

    generated_diff_text = ""

    diff_length = max(len(diff_dict["+"]), len(diff_dict["-"]))
    for i in range(diff_length):
        generated_diff_text += DIFF_PAIR_TEMPLATE.format(
            diff_dict["-"][i] if i < len(diff_dict["-"]) else "",
            diff_dict["+"][i] if i < len(diff_dict["+"]) else "",
            HORIZONTAL_LINE if i != diff_length - 1 else ""
        )

    return generated_diff_text.strip()
