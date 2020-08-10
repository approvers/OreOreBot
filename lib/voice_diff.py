"""
voice diff の処理 メインからバインドされる
無駄にクラス化してもしゃーないかーってことで関数になりました
"""
import discord
import datetime

from typing import Dict

class VoiceDiffHandler:
    TIME_INTERVAL_LIMIT = datetime.timedelta(microseconds=500)

    def __init__(self):
        self.hisotry: Dict[int, int] = {}

    async def handle(self, base_channel, member, before, after):
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

        prev_time = self.hisotry.setdefault(member.id, datetime.datetime.now())
        self.hisotry[member.id] = datetime.datetime.now()

        if (datetime.datetime.now() - prev_time) <= VoiceDiffHandler.TIME_INTERVAL_LIMIT:
            return

        embed_in = discord.Embed (title="{}が{}に入りました".format(member.display_name,str(after.channel)),
                                       description="何かが始まる予感がする。",
                                       color=0x1e63e9)
        embed_in.set_author(name="はらちょからのおしらせ",icon_url="https://lohas.nicoseiga.jp/thumb/3877931i?")
        embed_in.set_thumbnail(url="https://cdn.discordapp.com/avatars/{}/{}.png".format(member.id,member.avatar))

        embed_out = discord.Embed (title="{}が{}から抜けました".format(member.display_name,str(before.channel)),
                                       description="あいつは良い奴だったよ...",
                                       color=0x1e63e9)
        embed_out.set_author(name="はらちょからのおしらせ", icon_url="https://lohas.nicoseiga.jp/thumb/3877931i?")
        embed_out.set_thumbnail(url="https://cdn.discordapp.com/avatars/{}/{}.png".format(member.id,member.avatar))

        if after.channel == before.channel or member.bot:
            return

        if not (after.channel is None):
            await base_channel.send(embed=embed_in)
            return

        await base_channel.send(embed=embed_out)

    def is_in_interval(self, member_id: int):
        """
        前回の通知との時間間隔がTIME_INTERVAL_LIMIT以内かを判定する。

        Parameters
        ----------
        member_id: int
            判定対象のメンバーID。

        Return
        ------
        TIME_INTERVAL_LIMIT以内だった場合はTrue
        """
        delta = 
        if 
            return True

        return False

    

