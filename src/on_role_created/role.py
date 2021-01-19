import discord


class KawaemonRoleAdder:

    ROLE_ADD_MESSAGE_TEMPLATE = "{}ですが、{}にも追加しておきました"

    def __init__(
            self,
            kawae_member: discord.Member,
            announce_text_channel: discord.TextChannel
    ):
        self.kawae_member: discord.Member = kawae_member
        self.notify_channel: discord.TextChannel = announce_text_channel

    async def add_role(
        self,
        role_to_add: discord.Role
    ):
        await self.kawae_member.add_roles(role_to_add)
        await self.notify_channel.send(
            self.ROLE_ADD_MESSAGE_TEMPLATE.format(
                role_to_add.mention, self.kawae_member.mention)
        )
