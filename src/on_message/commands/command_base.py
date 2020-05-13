from abc import ABCMeta, abstractstaticmethod, abstractmethod

import discord


class CommandBase(metaclass=ABCMeta):
    """
    コマンドの基底クラス
    """
    @abstractstaticmethod
    @staticmethod
    def get_command_name() -> str:
        """
        コマンドの名称(識別用)を返します
        -------
        returns
        -------
        str: コマンドの名前
        """

    @abstractstaticmethod
    @staticmethod
    def get_help() -> str:
        """
        コマンドのヘルプを返します
        -------
        returns
        -------
        str: コマンドのヘルプ
        """

    @abstractstaticmethod
    @staticmethod
    def get_command_template() -> str:
        """
        コマンドの使い方のテンプレートを返します
        -------
        returns
        -------
        str: コマンドのテンプレート
        """

    @abstractmethod
    async def execute(self, params: discord.Message):
        """
        実際に実行する関数
        ----------
        Parameters
        ----------
        params: discord.Message
            関数に渡す
        """
