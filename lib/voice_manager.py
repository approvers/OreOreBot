"""
voice関連の処理を掌握するモジュール
"""
import asyncio

import discord

class VoiceManager():
    """
    音声関連の処理をするクラス
    """

    def __init__(self):
        """
        初期化処理
        """
        self.member = None
        self.before = None
        self.after = None
        self.is_join = None

        ignore_members = [684295118643265548]

    async def diff_embed(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """
        embedを送信する関数
        Parameters
        ----------
        member: discord.Member
            該当するメンバーののオブジェクト
        before: discord.VoiceState
            変更前のVoiceStateオブジェクト
        after: discord.VoiceState
            変更後のVoiceStateオブジェクト
        """
        self.member = member
        self.before = before
        self.after = after

        if after.channel == before.channel or member.id in VoiceManager.ignore_members:
            return
        self.is_join = after.channel is not None
        await VoiceManager.KIKISEN_CHANNEL.send(embed=self.embed_generater())
        await self.role_manager()

    def embed_generater(self):
        """
        instanceの状況に応じてembedを返す関数
        """
        if self.is_join:
            embed_title = "{}が{}に入りました"
            embed_message = "何かが始まる予感がする。"
        else: #<--- !!!!!!!!!!!!!!!!!!!!!!!!!
            embed_title = "{}が{}にから抜けました"
            embed_message = "あいつは良い奴だったよ…"
        embed_out = discord.Embed(title=embed_title.format(self.member.display_name, str(self.before.channel)), description=embed_message, color=0x1e63e9)
        embed_out.set_author(name="はらちょからのおしらせ", icon_url="https://lohas.nicoseiga.jp/thumb/3877931i?")
        embed_out.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/{}/{}.png".format(self.member.id, self.member.avatar))
        return embed_out

    async def role_manager(self):
        """
        instanceの状況に応じて@通話中Roleの操作をするクラス
        """
        if self.is_join:
            await self.member.add_roles(VoiceManager.LISTENER_ROLE)
            return
        await self.member.remove_roles(VoiceManager.LISTENER_ROLE)

    @classmethod
    async def reset_roles(cls):
        """
        @通話中をすべて剥奪するクラスメソッド
        """
        await VoiceManager.KIKISEN_CHANNEL.send("通話中のロールを全員から削除します！")
        for each_member in cls.GUILD.members:
            if cls.LISTENER_ROLE in each_member.roles:
                await each_member.remove_roles(cls.LISTENER_ROLE)
                await asyncio.sleep(0.125)

    @classmethod
    def static_init(cls, guild: discord.Guild, kikisen_channel: discord.TextChannel):
        """
        初期化をするクラス関数
        Parameters
        ----------
        guild: discord.Guild
            接続しているギルドのオブジェクト
        kikisen_channel: discord.TextChannel
            聞き専チャンネルのオブジェクト
        """
        listener_role_id = 700565764117233685
        cls.GUILD = guild
        cls.LISTENER_ROLE = guild.get_role(listener_role_id)
        cls.KIKISEN_CHANNEL = kikisen_channel
