from typing import Dict, Union
import discord
from src.on_message.commands.command_base import CommandBase
from src.on_message.commands.lol import LoL
from src.on_message.commands.role import Role
from src.on_message.commands.typo import Typo
from src.on_message.commands.haracyo import Haracyo


class CommandsManager:
    def __init__(
        self,
        client: discord.Client,
        config: Dict[str, Dict[str, Union[str, int]]]
    ):
        """
        全てのコマンドのインスタンスをここでdict[str, command_base]としてselfに渡す
        strにはcommand.get_command_name()の返り値が入る
        """
        base_text_channel_id = config["text_channel"]["base"]
        listen_text_channel_id = config["text_channel"]["listen"]
        base_voice_channel_id = config["voice_channel"]["base"]
        afk_voice_channel_id = config["voice_channel"]["afk"]

        self.base_text_channel = client.get_channel(base_text_channel_id)
        self.listen_text_channel = client.get_channel(listen_text_channel_id)
        self.base_voice_channel = client.get_channel(base_voice_channel_id)
        self.afk_voice_channel = client.get_channel(afk_voice_channel_id)

        self.commands = {
            LoL.get_command_name(): LoL(),
            Role.get_command_name(): Role(),
            Typo.get_command_name(): Typo()
        }

        self.commands[Haracyo.get_command_name()] = Haracyo(
            self.commands.keys()
        )

        self.message_command = {
            "lol_count_up": self.commands[LoL.get_command_name()].lol_count_up,
            "add_typo": self.commands[Typo.get_command_name()].add_typo
        }

    def search_command(self, keyword: str) -> Union[CommandBase, None]:
        """
        コマンドをkeywordから検索する
        ----------
        parameters
        ----------
        keyword: str
            検索に使用する文字列
        """
        if keyword in self.commands.keys():
            return self.commands[keyword]

        return None
