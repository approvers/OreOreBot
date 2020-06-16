import discord


class VoiceStateNotifier:
    JOIN_TITLE = "{}が{}に入りました"
    JOIN_DESCRIPTION = "何かが始まる予感がする"

    LEAVE_TITLE = "{}が{}から抜けました"
    LEAVE_DESCRIPTION = "あいつは良い奴だったよ..."

    EMBED_COLOR = 0x1e63e9
    EMBED_ICON = "https://lohas.nicoseiga.jp/thumb/4804258i?"
    EMBED_AUTHOR = "はらちょからのお知らせ"
    AVATAR_ICON = "https://cdn.discordapp.com/avatars/{}/{}.png"

    def __init__(self, root_channel: discord.TextChannel):
        self.root_channel = root_channel

    async def notify(
        self,
        member: discord.Member,
        before: discord.TextChannel,
        after: discord.TextChannel
    ):
        if after == before or member.bot:
            return
        embed = VoiceStateNotifier._create_embed(member, before, after)

        await self.root_channel.send(embed=embed)

    @staticmethod
    def _create_embed(
        member: discord.Member,
        before: discord.TextChannel,
        after: discord.TextChannel
    ) -> discord.Embed:
        if after is None:
            embed = discord.Embed(
                title=VoiceStateNotifier.LEAVE_TITLE.format(
                    member.display_name,
                    after.name
                ),
                description=VoiceStateNotifier.LEAVE_DESCRIPTION,
                color=VoiceStateNotifier.EMBED_COLOR
            )

            embed.set_author(
                name=VoiceStateNotifier.EMBED_AUTHOR,
                icon_url=VoiceStateNotifier.EMBED_ICON
            )

            embed.set_thumbnail(
                url=VoiceStateNotifier.AVATAR_ICON.format(
                    member.id,
                    member.avatar
                ),
            )
            return embed
        embed = discord.Embed(
            title=VoiceStateNotifier.JOIN_TITLE.format(
                member.display_name,
                after.name
            ),
            description=VoiceStateNotifier.JOIN_DESCRIPTION,
            color=VoiceStateNotifier.EMBED_COLOR
        )

        embed.set_author(
            name=VoiceStateNotifier.EMBED_AUTHOR,
            icon_url=VoiceStateNotifier.EMBED_ICON
        )

        embed.set_thumbnail(
            url=VoiceStateNotifier.AVATAR_ICON.format(
                member.id,
                member.avatar
            ),
        )
        return embed
