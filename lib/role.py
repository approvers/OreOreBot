"""
!role コマンドを処理してくれます
特にデータを保持することもないと思うので関数になりました
"""

import discord

async def role(commands, channel, member_name):
    """
    Parameters
    ----------
    commands: list
        commands[0]: str = "!role"
        commands[1]: str = 入力されたuser_idです
        commands[2]: str = 新しくつくる役職の名前です
        commands[3]: str = (任意)↑のカラーコードです"#ffffff"で指定します
    channel: discord.TextChannel
        messageを受け取ったチャンネルのオブジェクト
    member_name: str
        messageを発したユーザーのdisplay_name
    """

    if len(commands) < 3:
        await channel.send("引数は少なくとも2つは必要だよ...?")
        return

    if len(commands) >= 5:
        await channel.send("引数は2つか3つで指定してね")
        return

    user_id = commands[1]
    role_name = commands[2]
    target_user = channel.guild.get_member(int(user_id))

    if target_user is None:
        await channel.send("そんなユーザーIDのメンバーはいないよ...?")
        return

    if len(commands) == 3:
        color = discord.Colour.default()

    if len(commands) == 4:
        color_input = commands[3]

        if (not color_input.startswith("#") or len(color_input) != 7):
            await channel.send("カラーコードの形式が間違っているよ")
            return

        try:
            color_r = int(color_input[1:3], 16)
            color_g = int(color_input[3:5], 16)
            color_b = int(color_input[5:7], 16)
            color = discord.Colour.from_rgb(color_r, color_g, color_b)
        except ValueError:
            await channel.send("正しい16進数で指定してね")
            return

    created_role = await channel.guild.create_role(name=role_name, color=color,
                                                   reason="Created by {}".format(member_name),
                                                   mentionable=True)

    await target_user.add_roles(created_role)

    await channel.send("<@&{}>を作成して<@!{}>に付与しました！".format(created_role.id, target_user.id))
