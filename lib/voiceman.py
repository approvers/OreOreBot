"""
Voice関連の処理をするモジュール
"""
import asyncio

import discord

class VoiceEmbed:
    """
    メンバーの出入りによってembedを送信する機能を司るクラス
    """

    def embed_generate(self):
        """
        Parameters
        ----------

        Returns
        ----------
        embed_output: discord.Embed
            実際に生成されたEmbedオブジェクト
        """

        user_icon_url = "https://cdn.discordapp.com/avatars/{}/{}.png".format("HERE","HERE")

        if True == True:
            embed_title = "{}が{}に入りました"
            embed_message = "何かが始まる予感がする。"
        if True == False:
            embed_title = "{}が{}にから抜けました"
            embed_message = "あいつは良い奴だったよ…"

        embed_output = discord.Embed(title=embed_title.format(self.member.display_name, str(self.before.channel)), description=embed_message, color=0x1e63e9)
        embed_output.set_author(name="はらちょからのおしらせ", icon_url="https://lohas.nicoseiga.jp/thumb/3877931i?")
        embed_output.set_thumbnail(url=user_icon_url)

class VoiceRole:
    """
    通話の状況に応じて権限を付与/剥奪する
    """

    async def update_roles(member: discord.Member):
        pass

    async def reset_roles(members: list[discord.Member], respond_ch: discord.TextChannel):
        """
        Parameters
        ----------
        members: List[discord.Member]
            ギルド内のメンバー一覧をメンバーオブジェクトで受け取る
        respond_ch: discord.TextChannel
            メッセージを返信するテキストチャンネル
            コマンドが発行されたテキストちゃんねるのオブジェクト
        """
        await respond_ch.send("<@&700565764117233685>を全員から剥奪します！")
        for member in members:
            if None in member.roles:
                await member.remove_roles(VoiceRole.LISTENER_ROLE)
                await asyncio.sleep(0.125)

    @classmethod
    def static_init(cls, listener_role: discord.Role):
        """
        初期化 やることはRoleのオブジェクトを受け取るだけが関の山
        Parameters
        ----------
        listener_role: discord.Role
            mainから渡される<@&700565764117233685>のロールオブジェクト
        """
        cls.LISTENER_ROLE = listener_role