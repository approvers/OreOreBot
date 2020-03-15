from lib.util import Singleton


class LolCounter(Singleton):
    """
    「草」をカウントしてくれるクラス
    """
    _LOL_MESSAGE = {
        "counter-value": "私が起きてから、司令官は{}回「草」って言ってるね",
        "too-many"     : "...いくらなんでも多すぎないかい?",
        "no-lol"       : "まだ「草」って言ってないみたいだね"
    }
    def __init__(self, members):
        """
        変数の初期化を行う
        Parameters
        ----------
        members : List<discord.member>
            サーバーのメンバーのリスト
        """
        self.lol_count = {}
        for member in members:
            self.lol_count[member.id] = 0

    def count(self, message, author_id):
        """
        草を行った回数をlol_countに追加する
        Parameters
        ----------
        message  : str
            実際に発言されたメッセージ
        author_id: int
            発言者のid
        """
        if author_id in self.lol_count.keys():
            self.lol_count[author_id] += message.count("草")
            return
        self.lol_count[author_id] = message.count("草")

    async def output(self, channel, author_id):
        """
        現在の草の数を出力する
        channel: discord.Channel
            コマンドを入力されたチャンネル
        author_id: int
            発言者のid
        """
        if not author_id in self.lol_count.keys():
            await channel.send(LolCounter._LOL_MESSAGE["no-lol"])
            return

        count = self.lol_count[author_id]
        if count == 0:
            await channel.send(LolCounter._LOL_MESSAGE["no-lol"])
            return
        await channel.send(LolCounter._LOL_MESSAGE["counter-value"].format(count))
        if count >= 10:
            await channel.send(LolCounter._LOL_MESSAGE["too-many"])

