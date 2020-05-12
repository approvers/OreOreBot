from abc import ABCMeta, abstractstaticmethod, abstractmethod
from typing import List

from src.on_message.commands.commands_parameter import CommandsParameter


class CommandBase(metaclass=ABCMeta):
    """
    コマンドの基底クラス
    """
    @staticmethod
    @abstractstaticmethod
    def get_command_name() -> str:
        """
        コマンドの名称(識別用)を返します
        -------
        returns
        -------
        str: コマンドの名前
        """

    @abstractmethod
    async def execute(self, params: CommandsParameter):
        """
        実際に実行する関数
        ----------
        Parameters
        ----------
        params: List[str]
            関数に渡す
        """
