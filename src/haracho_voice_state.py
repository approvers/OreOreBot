import discord


class HarachoVoiceState:
    """
    はらちょのVoiceStateの状態を管理する
    シングルトンなのでその場でインスタンス作っても値が共有される
    """
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super(HarachoVoiceState, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.voice_state = False

    def turnOnVoiceState(self, state: discord.VoiceState):
        """
        はらちょがVCに入る際の前処理
        先にvoice_stateをTrueにしておく
        ------
        Params
        ------
        state: discord.VoiceState
            はらちょのVoiceState
        """
        if state.channel is not None or self.voice_state:
            raise RuntimeError("Haracho already join to voice channel")
        self.voice_state = True

    def turnOffVoiceState(self, state: discord.VoiceState):
        """
        はらちょがVCから抜けたあとの後処理
        抜けてからvoice_stateをFalseにする
        ------
        Params
        ------
        state: discord.VoiceState
            はらちょのVoiceState
        """
        if state.channel is None or not self.voice_state:
            raise RuntimeError("Haracho did not join to voice channel")
        self.voice_state = False
