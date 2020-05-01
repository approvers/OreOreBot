"""
message_debug関連の処理がなされます
実装してみたら一つしか関数ができなかったので関数での実装となります
"""
import discord


async def debug_on_edit(debug_text: str, respond_channel: discord.TextChannel):
    """
    編集でデバッグを表示したいときに呼び出される関数
    send_resultに必要なパラメーターを渡す
    Parameters
    ----------
    debug_text: str
        デバッグ表示するテキスト
    respond_channel: discord.TextChannel
        返答するチャンネルのオブジェクト
    """
    await send_result(debug_text, respond_channel)


async def debug_on_message(target_message_id: str, respond_channel: discord.TextChannel):
    """
    コマンドによってデバッグを表示したいときに呼び出される関数
    send_resultに必要なパラメーターを渡す
    Parameters
    ----------
    target_message_id: str
        ユーザーが指定したid
    respond_channel: discord.TextChannel
        コマンドが発行されたチャンネルのオブジェクト
        ここに返信する
    """

    # コマンドの書式チェック
    if len(target_message_id) < 2:
        await respond_channel.send("メッセージのidを指定してね")
        return

    if not target_message_id.isdecimal():
        await respond_channel.send("正しい数字でidを教えてね")
        return

    target_message_id = int(target_message_id)

    # メッセージの存在を確認
    try:
        target_message = await respond_channel.fetch_message(target_message_id)

    except discord.errors.NotFound:
        await respond_channel.send("このチャンネルにはそのidのメッセージは存在しないよ...?\nそのメッセージのあるチャンネルで試してみてね")
        return

    except Exception as caught_exception:
        await respond_channel.send("例外が発生したよ\n内容は{}だよ".format(caught_exception))
        return

    # 送信！
    await send_result(debug_text=target_message.content, respond_channel=respond_channel)


async def send_result(debug_text: str, respond_channel: discord.TextChannel):
    """
    渡された情報を基に実際にメッセージを送る関数
    Parameters
    ----------
    debug_text: str
        実際に送信する本文のテキスト
    respond_channel: discord.TextChannel
        メッセージを送信するチャンネルのオブジェクト
    """
    await respond_channel.send("メッセージのデバッグを表示するよ")

    if "`" in debug_text:
        await respond_channel.send("\\`が含まれているので'で置換するよ")
        debug_text = debug_text.replace("`", "'")

    await respond_channel.send("```\n{}\n```".format(debug_text))
