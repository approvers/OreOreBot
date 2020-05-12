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

    @staticmethod
    @abstractstaticmethod
    def get_require_params() -> List[str]:
        """
        一定の形式をもとに必要な値をList[str]形式で返す
        """

    @abstractmethod
    def execute(self, params: CommandsParameter):
        """
        実際に実行する関数
        ----------
        Parameters
        ----------
        params: List[str]
            関数に渡す
        """
