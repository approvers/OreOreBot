"""
!role コマンドを処理してくれます
特にデータを保持することもないと思うので関数になります
"""

import discord

class Role():
    def __init__(self):
        pass

    async def role(self, commands, channel, member_name):

        if len(commands) < 3:
            await channel.send("引数は少なくとも2つは必要だよ...?")
            return

        if channel.guild.get_member(int(commands[1])) == None:
            await channel.send("そんなユーザーIDのメンバーはいないよ...?")

        if len(commands) == 3:
            target = channel.guild.get_member(int(commands[1]))
            name = commands[2]
            color = discord.Colour.default()

        if len(commands) == 4:
            try:
                color = discord.Colour.from_rgb(int(commands[3][1:3],16),int(commands[3][3:5],16),int(commands[3][5:7],16))
                target = channel.guild.get_member(int(commands[1]))
                name = commands[2]
            except:
                await channel.send("そんな色はないよ...?")
                return

        created_role = await channel.guild.create_role(name=name, color=color, reason="Created by {}".format(member_name), mentionable=True)

        await target.add_roles(created_role)

        await channel.send("<@&{}>を作成して<@!{}>に付与しました！".format(str(created_role.id),str(target.id)))