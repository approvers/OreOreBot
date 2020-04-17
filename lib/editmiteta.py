"""
クライアントがメッセージの変更を検知したときの処理をします
例のごとくまたもや関数になりました
"""
import difflib

import discord


async def mitetazo_edit(before: discord.Message, after: discord.Message):
    """
    実際に編集を感知したときに呼ばれる関数
    編集前のメッセージを送信します
    Parameters
    ----------
    before: discord.Message
        編集前のMessageオブジェクト
    after: discord.Message
        変更後のMessageオブジェクト
    """
    before_text = before.content.split("\n")
    after_text = after.content.split("\n")
    composed_text = diff_composer(before_text, after_text)
    if composed_text.strip() == "":
        return
    await after.channel.send("見てたぞ\n```diff\n{}\n```".format(composed_text))


def diff_composer(before_text: list, after_text: list):
    """
    beforeとafterのテキストを比較して
    結果に - + が含まれる行のみをstrで返しますね
    Parameters
    ----------
    before_text: list
        編集前のMessageオブジェクトのテキストの改行ごとのリスト
    after_text: list
        編集後のMessageオブジェクトのテキストの改行ごとのリスト
    Returns
    ----------
    composed_text: str
        改行なども含め処理をした最終成果物
    """
    composed_text = ""
    diff_object = difflib.Differ()
    diff = diff_object.compare(before_text, after_text)
    diff_list = list(diff)
    diff_text_list = [i for i in diff_list if i.startswith("+") or i.startswith("-")]

    for n in range(len(diff_text_list)):
        composed_text += diff_text_list[n] + "\n"
        if n % 2 == 1 and not n == len(diff_text_list) - 1:
            composed_text += "---------------------------------\n"
    return composed_text
