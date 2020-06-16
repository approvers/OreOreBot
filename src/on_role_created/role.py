import discord
from typing import Dict, Union


async def add_role_to_kawae(
    config: Dict[str, Dict[str, Union[str, int]]],
    role: discord.Role
):
    user: discord.Member = role.guild.get_member(config["role"]["user_id"])
    notify_channel: discord.TextChannel = role.guild.get_channel(config["role"]["user_id"])
    await user.add_roles(role)
    await notify_channel.send(role.mention + "ですが、かわえにも追加しておきました")

