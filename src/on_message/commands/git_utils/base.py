from abc import ABCMeta, abstractmethod
from typing import Tuple, Dict, Union

import discord

ResponseDetail = Dict[str, Union[str, int, bool]]
Response = Dict[str, Union[str, int, bool, ResponseDetail]]


class Base(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, auth: Tuple[str, str]):
        """
        Git周りの基底
        認証情報
        """

    @abstractmethod
    def execute(
            self,
            orgs: str,
            repos: str,
            send_message_send: discord.TextChannel,
            mode: str,
            target: Union[str, int, None]
    ):
        """
        実際に呼び出す関数
        """

    @abstractmethod
    def _get(self, orgs: str, repos: str):
        """
        orgsとreposを受け取ってデータを取ってくる
        """
