"""
voice関連の処理を掌握するモジュール
"""
import asyncio

import discord

class VoiceManager():

    def __init__(self):
        self.member = None
        self.before = None
        self.after = None
        self.is_join = None

    def embed_generater(self):
        embed_in = discord.Embed(title="{}が{}に入りました".format(self.member.display_name, str(self.after.channel)),
                                 description="何かが始まる予感がする。", color=0x1e63e9)
        embed_in.set_author(name="はらちょからのおしらせ", icon_url="https://lohas.nicoseiga.jp/thumb/3877931i?")
        embed_in.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{}/{}.png".format(self.member.id, self.member.avatar))
        embed_out = discord.Embed(title="{}が{}から抜けました".format(self.member.display_name, str(self.before.channel)),
                                  description="あいつは良い奴だったよ...", color=0x1e63e9)
        embed_out.set_author(name="はらちょからのおしらせ", icon_url="https://lohas.nicoseiga.jp/thumb/3877931i?")
        embed_out.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{}/{}.png".format(self.member.id, self.member.avatar))

        if self.is_join:
            return embed_in
        return embed_out

    async def diff_embed(self, member, before, after):

        self.member = member
        self.before = before
        self.after = after

        if self.after.channel == self.before.channel or self.member.id in [684295118643265548]:
            return
        if not (self.after.channel is None):
            self.is_join = True
            await VoiceManager.KIKISEN_CHANNEL.send(embed=self.embed_generater())
            await self.role_manager()
            return
        self.is_join = False
        await VoiceManager.KIKISEN_CHANNEL.send(embed=self.embed_generater())
        await self.role_manager()

    async def role_manager(self):
        if self.is_join:
            await self.member.add_roles(VoiceManager.LISTENER_ROLE)
            return
        await self.member.remove_roles(VoiceManager.LISTENER_ROLE)

    @classmethod
    async def reset_roles(cls):
        await VoiceManager.KIKISEN_CHANNEL.send("通話中のロールを全員から削除します！")
        for each_member in cls.GUILD.members:
            if cls.LISTENER_ROLE in each_member.roles:
                await each_member.remove_roles(cls.LISTENER_ROLE)
                await asyncio.sleep(0.125)

    @classmethod
    def static_init(cls, guild: discord.Guild, kikisen_channel: discord.VoiceChannel):
        listener_role_id = 700565764117233685
        cls.GUILD = guild
        cls.LISTENER_ROLE = guild.get_role(listener_role_id)
        cls.KIKISEN_CHANNEL = kikisen_channel