import discord
import os

from src.on_message.root import MessageRoot
from src.config.load import load_config


class MainClient(discord.Client):
    def __init__(self) -> None:
        super().__init__()
        config = load_config()
        self.message_manager = MessageRoot(
            self,
            config
        )

    def run(self) -> None:
        super().run(os.environ["TOKEN"])

    async def on_ready(self) -> None:
        if len(self.guilds) == 1:
            pass

    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        self.message_manager.anarysis_message(message)

    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState
    ) -> None:
        pass

    async def on_message_edit(
        self,
        before: discord.Message,
        after: discord.Message
    ) -> None:
        pass

    async def on_message_delete(self, message: discord.Message) -> None:
        pass

    async def on_guild_role_create(self, role):
        pass

