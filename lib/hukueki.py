"""
ねぇ、将来に何してるだろうね
服役はしてないと良いね
困らないでよ
"""
import discord


HUKUEKI_MESSAGES = {
"hukueki": """\
```
ねぇ、将来何してるだろうね
{}はしてないと良いね
困らないでよ
```
""",

"lolicon": """\
```
だから僕は{}を辞めた - {} (Music Video)
```
"""
}


async def hukueki(raw_content: str, respond_ch: discord.TextChannel):
    """
    ねぇ、将来何してるだろうね
    服役はしてないと良いね
    困らないでよ
    Parameters
    ----------
    content: str
        服役の部分
    respond_ch: discord.TextChannel
        返信するチャンネルのオブジェクト メッセージが送信されたチャンネルと同じ
    """
    parsed_content = text_parser(raw_content)
    await respond_ch.send(HUKUEKI_MESSAGES["hukueki"].format(parsed_content))


async def lolicon(raw_content: str, member_name: str, respond_ch: discord.TextChannel):
    """
    だから僕はロリコンを辞めた - こるく (Music Video)
    Parameters
    ----------
    content: str
        ロリコンの部分
    member_name: str
        こるくの部分
    respond_ch: discord.TextChannel
        返信するチャンネルのオブジェクト メッセージが送信されたチャンネルと同じ

    """
    parsed_content = text_parser(raw_content)
    await respond_ch.send(HUKUEKI_MESSAGES["lolicon"].format(parsed_content, member_name))


def text_parser(raw_text: str):
    """
    `が含まれている場合は'に置換して返す
    Parameters
    ----------
    raw_text: str
        パースしたいテキスト
    Returns
    ----------
    parsed_text: str
        `を'に置換した結果
    """
    if "`" in raw_text:
        parsed_text = raw_text.replace("`", "'")
        return parsed_text

    return raw_text
