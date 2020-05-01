"""
message_debug関連の処理がなされます
実装してみたら一つしか関数ができなかったので関数での実装となります
"""
import discord


async def debug_on_edit(message: discord.Message):
    """
    編集でデバッグを表示したいときに呼び出される関数
    send_resultに必要なパラメーターを渡す
    Parameters
    ----------
    message: discord.Message
        ターゲットメッセージのオブジェクト
    """
    debug_text = message.content
    respond_channel = message.channel

    await send_result(debug_text=debug_text, respond_channel=respond_channel)


async def debug_on_message(commands: list, respond_channel: discord.TextChannel):
    """
    コマンドによってデバッグを表示したいときに呼び出される関数
    send_resultに必要なパラメーターを渡す
    Parameters
    ----------
    commands: list[str]
        発行されたコマンド
    respond_channel: discord.TextChannel
        コマンドが発行されたチャンネルのオブジェクト
        ここに返信する
    """

    # コマンドの書式チェック
    try:
        target_message_id = int(commands[1])

    except IndexError:
        await respond_channel.send("メッセージのidを指定してね")
        return

    except ValueError:
        await respond_channel.send("正しい数字でidを教えてね")
        return

    except Exception as caught_exception:
        await respond_channel.send("例外が発生したよ\n内容は{}だよ".format(caught_exception))
        return

    # メッセージの存在を確認
    try:
        target_message = await respond_channel.fetch_message(target_message_id)

    except discord.errors.NotFound:
        await respond_channel.send("そんなidのメッセージは存在しないよ...?\nそのメッセージのあるチャンネルで試してみてね")
        return

    except Exception as caught_exception:
        await respond_channel.send("例外が発生したよ\n内容は{}だよ".format(caught_exception))

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
