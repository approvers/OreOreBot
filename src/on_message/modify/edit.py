import difflib
import discord
from typing import List


MESSAGE_TEMPLATE = "見てたぞ\n```diff\n{}```"
DIFF_PAIR_TEMPLATE = "{}\n{}\n{}"
HORIZONTAL_LINE = "------------------------------\n"


async def edit_notify(
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
    modified_diff = [x for x in raw_diff if x[:1] in "+-"]

    generated_diff_text = ""
    for i in range(0, len(modified_diff), 2):
        generated_diff_text += DIFF_PAIR_TEMPLATE.format(
            modified_diff[i],
            modified_diff[i + 1],
            HORIZONTAL_LINE if (i + 1) != len(modified_diff) - 1 else ""
        )

    return generated_diff_text.strip()
