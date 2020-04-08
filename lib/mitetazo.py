import discord
import asyncio

mitetazo_message = """\
{}さん、メッセージを削除しましたね？私は見ていましたよ。内容も知っています。
```
{}
```
"""


async def mitetazo(message: discord.message):
    if message.author.bot:
        return

    author_name = message.author.name

    await message.channel.send(
        mitetazo_message.format(author_name, message.content)
    )
