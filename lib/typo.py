"""
!Typo周りの処理
"""
from lib.util import Singleton
import discord

class Typo(Singleton):
    """
    Typoを記録し、表示するクラス
    """
    def __init__(self, members: list):
        """
        メンバーリストを用いて初期化を行う
        Parameters
        ----------
        members: list<discord.Member>
            サーバーのメンバーリスト
        """
        self.typo_dict = {}
        for member in members:
            self.typo_dict[member.id] = []

    def append(self, member_id: int, message: str):
        """
        typoした単語をlistに追加
        Parameters
        ----------
        member_id: int
            typoしたメンバーのid
        message: str
            typoした言葉
        """
        if not member_id in self.typo_dict.keys():
            self.typo_dict[member_id] = []

        if message.replace(" ", "") == "":
            return

        self.typo_dict[member_id].append(message[:-3])

    def call(self, member_id: int, member_name: str):
        """
        typoした単語のリストをテンプレートをもとに返す
        Parameters
        ----------
        member_id: int
            呼び出したメンバーのid
        member_name: str
            呼び出したメンバーの名前
        """
        if not member_id in self.typo_dict.keys():
            self.typo_dict[member_id] = []

        user_typo = self.typo_dict[member_id]

        send_message = "***今日の{}のtypo***\n".format(member_name)

        display_typo = ""

        for typo in user_typo:
            display_typo += "・{}\n".format(typo)
        return send_message + display_typo

