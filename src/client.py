import discord


class MainClient(discord.Client):
    def __init__(self, token: str) -> None:
        self.token = token

    def run(self) -> None:
        super().run(self.token)

    async def on_ready(self) -> None:
        if len(self.guilds) == 1:
            pass

    async def on_message(self, message: discord.Message) -> None:
        pass

    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState
    ) -> None:
        pass

    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        pass

    async def on_message_delete(self, message: discord.Message) -> None:
        pass

    async def on_guild_role_create(self, role):
        pass

