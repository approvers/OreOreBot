import discord


class HarachoVoiceState:
    voice_state: bool = False

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(HarachoVoiceState, cls).__new__(cls)
        return cls._instance

    def turnOnVoiceState(self, state: discord.VoiceState):
        if state.channel is not None or HarachoVoiceState.voice_state:
            raise RuntimeError("Haracho already join to voice channel")
        HarachoVoiceState.voice_state = True

    def turnOffVoiceState(self, state: discord.VoiceState):
        if state.channel is None or not HarachoVoiceState.voice_state:
            raise RuntimeError("Haracho did not join to voice channel")
        HarachoVoiceState.voice_state = False
