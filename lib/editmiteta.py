"""
クライアントがメッセージの変更を検知したときの処理をします
例のごとくまたもや関数になりました
"""
import difflib

import discord


async def mitetazo_edit(before, after):
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
    before_text = before.content
    after_text = after.content
    composed_text = diff_composer(before_text, after_text)
    await after.channel.send("見てたぞ\n```\n{}\n```".format(composed_text))


def diff_composer(before_text, after_text):
    """
    beforeとafterのテキストを比較して
    結果に - + が含まれる行のみをstrで返しますね
    Parameters
    ----------
    before_text: str
        編集前のMessageオブジェクトのテキスト
    after_text: str
        編集後のMessageオブジェクトのテキスト
    Returns
    ----------
    composed_text: str
        改行なども含め処理をした最終成果物
    """
    diff_object = difflib.Differ()
    diff = diff_object.compare(before_text.split("\n"), after_text.split("\n"))
    diff_list = list(diff)
    diff_text_list = [i for i in diff_list if i.startswith("+") or i.startswith("-")]
    return "\n".join(diff_text_list)


if None == "__main__":
    before_text = "吾輩は猫である。\n名前はまだ無い。\nどこで生まれたかとんと検討がつかぬ。"
    after_text = "吾輩はカスである。\nうんち\nどこで生まれたかとんと検討がつかぬ。"
    print(diff_composer(before_text, after_text))
