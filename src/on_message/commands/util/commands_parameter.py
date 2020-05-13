import discord


class CommandsParameter:
    def __init__(
        self,
        author_id: int = 0,
        author_name: str = "",
        send_channel: discord.TextChannel = None,
        message: str = ""
    ):
        self.author_id: int = author_id
        self.author_name: str = author_name
        self.send_channel: discord.TextChannel = send_channel
        self.message: str = message
