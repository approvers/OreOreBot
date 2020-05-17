from abc import ABCMeta, abstractmethod
from typing import Union

import discord


class CommandBase(metaclass=ABCMeta):
    """
    コマンドの基底クラス
    """
    COMMAND: Union[str, None] = None
    HELP: Union[str, None] = None
    COMMAND_TEMPLATE: Union[str, None] = None

    def __new__(cls, *_, **__):
        if cls.COMMAND is None:
            raise ValueError("COMMAND is undefined")
        if cls.HELP is None:
            raise ValueError("HELP is undefined")
        if cls.COMMAND_TEMPLATE is None:
            raise ValueError("COMMAND_TEMPLATE is undefined")
        self = super().__new__(cls)
        return self

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

    async def send_help(self, send_message_channel: discord.TextChannel, prefix: str):
        if CommandBase.HELP is None:
            raise RuntimeError("ちね")
        await send_message_channel.send(CommandBase.HELP.format(prefix=prefix))
