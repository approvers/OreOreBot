import discord


class KawaemonRoleAdder:

    def __init__(self, client: discord.Client, kawae_user_id: int, announce_text_channel_id: int):
        self.kawae_member: discord.Member = client.get_user(kawae_user_id)
        self.notify_channel: discord.TextChannel = client.get_channel(announce_text_channel_id)

    async def add_role(
        self,
        role_to_add: discord.Role
    ):
        await self.kawae_member.add_roles(role_to_add)
        await self.notify_channel.send(
            "{}ですが、{}にも追加しておきました".format(role_to_add.mention, self.kawae_member.mention)
        )

