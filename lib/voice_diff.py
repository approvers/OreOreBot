"""
voice diff の処理 メインからバインドされる
無駄にクラス化してもしゃーないかーってことで関数になりました
"""
import discord


class VoiceDiffManager:

    VoiceDiffManager.embed_in = discord.Embed(title="{}が{}に入りました".format(member.display_name, str(after.channel)),
                             description="何かが始まる予感がする。",
                             color=0x1e63e9)
    VoiceDiffManager.embed_in.set_author(name="はらちょからのおしらせ", icon_url="https://lohas.nicoseiga.jp/thumb/3877931i?")
    VoiceDiffManager.embed_in.set_thumbnail(url="https://cdn.discordapp.com/avatars/{}/{}.png".format(member.id, member.avatar))

    VoiceDiffManager.embed_out = discord.Embed(title="{}が{}から抜けました".format(member.display_name, str(before.channel)),
                              description="あいつは良い奴だったよ...",
                              color=0x1e63e9)
    VoiceDiffManager.embed_out.set_author(name="はらちょからのおしらせ", icon_url="https://lohas.nicoseiga.jp/thumb/3877931i?")
    VoiceDiffManager.embed_out.set_thumbnail(url="https://cdn.discordapp.com/avatars/{}/{}.png".format(member.id, member.avatar))

    async def role_controller(self, member, is_join):
        if is_join:
            await member.add_roles(VoiceDiffManager.ROLE)
            return

        await member.remove_roles(VoiceDiffManager.ROLE)

    async def voice_diff(base_channel, member, before, after):
        """
        voice diffの処理をする
        Parameters
        ----------
        base_channel: discord.Channel
            ディスコードのチャンネル 聞き専チャンネルがわたされる
        member: discord.Member
            受け取ったメッセージのデータ
        before: discord.VoiceState
            変更前のVoiceState
        after: discord.VoiceState
            変更後のVoiceState
        """

        if after.channel == before.channel or member.id in [684295118643265548]:
            return

        if not (after.channel is None):
            await base_channel.send(embed=VoiceDiffManager.embed_in)
            await self.
            return

        await base_channel.send(embed=VoiceDiffManager.embed_out)

    @staticmethod
    async def resset_roles(self):
        for each_member in VoiceDiffManager.guild.members:
            if VoiceDiffManager.ROLE in each_member.roles:
                await each_member.remove_roles(VoiceDiffManager.ROLE)
                await asyncio.sleep(0.5)

    @staticmethod
    def static_init(guild: discord.Guild):
        listener_role_id = 700565764117233685
        VoiceDiffManager.GUILD = guild
        VoiceDiffManager.ROLE = guild.get_role(listener_role_id)

