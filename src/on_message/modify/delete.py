import discord


MESSAGE_TEMPLATE = """
        {}さん、メッセージを削除しましたね？
        私は見ていましたよ。内容も知っています。
        ```
        {}
        ```
    """.replace(" ", "")


def delete_notify(self, message: discord.Message):
    if message.author.bot:
        return

    await message.channel.send(
        MESSAGE_TEMPLATE.format(
            message.author.display_name,
            message.content
        )
    )
