"""
message_debug関連の処理がなされます
実装してみたら一つしか関数ができなかったので関数での実装となります
"""
import discord


async def debug_on_edit(message: discord.Message):
    await send_result(debug_text=message.content, respond_channel=message.channel)


async def debug_on_message(message_id: int, respond_channel: discord.TextChannel):
    try:
        target_message = await respond_channel.fetch_message(message_id)
    except discord.errors.NotFound:
        await respond_channel.send("そんなidのメッセージは存在しないよ...?\nそのメッセージのあるチャンネルで試してみてね")
        return
    except Exception as e:
        await respond_channel.send("例外が発生したよ\n内容は{}だよ".format(e))
    await send_result(debug_text=target_message.content, respond_channel=respond_channel)


async def send_result(debug_text: str, respond_channel: discord.TextChannel):
    await respond_channel.send("メッセージのデバッグを表示するよ")
    if debug_text.count("`") >= 1:
        await respond_channel.send("\`が含まれているので'で置換するよ")
        debug_text = debug_text.replace("`", "'")
    await respond_channel.send("```\n{}\n```".format(debug_text))
