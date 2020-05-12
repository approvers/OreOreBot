from typing import Dict, Union

import discord

class MessageRoot:
    def __init__(
            self,
            client: discord.Client,
            config: Dict[str, Dict[str, Union[str, int]]]
    ):
        base_text_channel_id = config["text_channel"]["base"]
        listen_text_channel_id = config["text_channel"]["listen"]
        base_voice_channel_id = config["voice_channel"]["base"]
        afk_voice_channel_id = config["voice_channel"]["afk"]

        self.base_text_channel = client.get_channel(base_text_channel_id)
        self.listen_text_channel = client.get_channel(listen_text_channel_id)
        self.base_voice_channel = client.get_channel(base_voice_channel_id)
        self.afk_voice_channel = client.get_channel(afk_voice_channel_id)

    def get_command(self, message: str):
        

