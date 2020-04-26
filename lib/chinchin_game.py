"""
ちんちん侍ゲームを司るファイルです
"""
import re
import discord

from lib.util import Singleton


class ChinchinGame(Singleton):
    """
    ちんちん侍ゲームを提供するシングルトンのクラスです。
    ちんちん侍ゲームは以下のフローで実施されます:

    はらちょ「ちんちん」　ーー＞はらちょが指定したプレイヤー「ちんちん」
    はらちょ「おちんちん」ーー＞はらちょが指定したプレイヤー「びろーん」
    はらちょ「さむらい」　ーー＞はらちょが指定したプレイヤー「さむらい」
    はらちょ「ちんちん侍」ーー＞全員のプレイヤー「ちんちん侍」

    この際、誤ったレスポンスをすることでそのユーザーは失格となります。
    (「ちんちん」に対し、「びろーん」と返すとそのユーザーは失格です)

    このソースコードでははらちょが発するメッセージを「コール(call)」、
    プレイヤーが発するメッセージを「レスポンス(response)」と呼称しています。
    """

    # ----------- 定数たち --------------

    STATUS_NOT_STARTED = 0
    STATUS_RECRUITING = 1
    STATUS_GAME_STARTED = 2

    """
    「!」を付けずにトリガーされるコマンドの正規表現です
    """
    PREFIXLESS_COMMANDS_REGEX = {
        "chinchin_respond": "(ちんちん|チンチン)",
        "ochinchin_respond": "(びろーん|ビローン)",
        "samurai_respond": "(しゃきーん|シャキーン)",
        "chinchin_samurai_respond": "(ちんちん侍|チンチン侍)",
    }

    """
    「!」を付けて発火するコマンドです
    """
    COMMANDS = {
        "open_session": "open",
        "start_session": "start",
        "join_session": "join",
        "finish_session": "finish",
    }

    """
    送信するメッセージです
    TODO: 可能であればhibikinessの実装が必要です
    """
    MESSAGES = {
        "too_few_args": "ちんちんはもっと多くの引数を欲しています！",
        "unknown_command": "どういう意味だかわかりませんでした…",
        "not_usable_now": "今は使えないコマンドです！",
        "session_suggestion": "もしちんちん侍ゲームを開始したいのであれば、`!chinchin {}`を叩いてみてください。",
        "opened": "ちんちん侍ゲームの参加者の募集を開始しました！\nちなみにあなたは***†ちんちんマスター†***です",
        "already_opened": "すでに募集を開始しているか、ゲーム中です。",
        "joined": "参加を受け付けました！ありがとうございます！",
        "already_joined": "すでに参加しています。",
        "left": "ちんちん侍ゲームから辞退しました！",
        "already_left": "すでに辞退しているかそもそも登録していません。",
        "started": "募集を締め切りました。\nちんちん侍ゲームを執り行います！",
        "finished": "一人になった！終わりました！\n優勝は{}です！！！！！！！！！！！！！",
        "manually_finished": "あっ、***†ちんちんマスター†***が終了コマンドを叩きました\nこれにて強制終了とさせていただきます",
        "chinchin_call": "{}さん、***ちんちん***",
        "ochinchin_call": "{}さん、***おちんちん***",
        "samurai_call": "{}さん、***さむらい***",
        "chinsamurai_call": "***ちんちん侍***！",
        "miss": "あぁーっ！ミスったぁー！失格です！カス！うんち！",
        "not_master": "***†ちんちんマスター†***しか実行できないコマンドです、権力の差というのはときに悲しいね",
    }

    # ----------- 関数たち --------------

    def __init__(self):
        """
        初期化処理を行う
        """
        self.game_status = self.STATUS_NOT_STARTED

        self.chinchin_master_id = -1
        self.session_channel: discord.TextChannel = None
        self.joined_users = []

    # ----------- コマンドたち --------------

    def parse_prefixless_command(self, msg: str, user: discord.Member, channel_id: int):
        """
        「!」を付けずに発火されたコマンドを実行する
        :param msg: メッセージ
        :param user: 発言したユーザー
        :param channel_id: 発言したチャンネルのID
        """
        print("Not implemented yet, but i think this will be easy")

    async def parse_prefix_command(self, message: list, user_id: int, channel: discord.TextChannel):
        """
        「!」を付けて発火されたコマンドを実行する
        :param message: メッセージ
        :param user_id: 発言したユーザーのID
        :param channel: 発言したチャンネル
        """

        if len(message) < 2:
            await channel.send(self.MESSAGES["too_few_args"])
            return
        sub_command: str = message[1]

        if sub_command not in self.COMMANDS.values():
            await channel.send(self.MESSAGES["unknown_command"])
            return

        if self.game_status == self.STATUS_NOT_STARTED:
            await self.parse_no_session_command(sub_command, user_id, channel)
            return

        if channel.id != self.session_channel.id:
            return

        if self.game_status == self.STATUS_RECRUITING:
            await self.parse_recruit_command(sub_command, user_id)
            return

        if self.game_status == self.STATUS_GAME_STARTED:
            await self.parse_game_command(sub_command, user_id)
            return

    async def parse_no_session_command(
            self, sub_command: str, user_id: int, channel: discord.TextChannel):
        """
        STATUSがSTATUS_NOT_STARTED(まだ誰もセッションを開いていない)のときに
        発火されるコマンドを実行する
        :param sub_command: ユーザーに指定されたサブコマンド
        :param user_id: 発言したユーザー
        :param channel: 発言したチャンネル
        """

        if sub_command == self.COMMANDS["open_session"]:
            await self.open_game_session(user_id, channel)
            return

        await channel.send(
            self.MESSAGES["not_usable_now"] + "\n" +
            self.MESSAGES["session_suggestion"].format(self.COMMANDS["open_session"])
        )

    async def parse_recruit_command(self, sub_command: str, user_id: int):
        """
        STATUSがSTATUS_RECRUITING(プレイヤーを募集中)のときに
        発火されるコマンドを実行する
        :param sub_command: ユーザーに指定されたサブコマンド
        :param user_id: 発言したユーザー
        """
        if sub_command == self.COMMANDS["join_session"]:
            await self.join_game_session(user_id)
            return

        if sub_command == self.COMMANDS["start_session"]:
            await self.start_game_session(user_id)
            return

        await self.session_channel.send(self.MESSAGES["not_usable_now"])

    async def parse_game_command(self, sub_command: str, user_id: int):
        """
        STATUSがSTATUS_GAME_STARTED(プレイヤーを募集中)のときに
        発火されるコマンドを実行する
        :param sub_command: ユーザーに指定されたサブコマンド
        :param user_id: 発言したユーザー
        """
        if sub_command == self.COMMANDS["finish_session"]:
            await self.finish_game_session(user_id)
            return

        await self.session_channel.send(self.MESSAGES["not_usable_now"])

    # ----------- サブコマンドたち --------------

    async def open_game_session(self, user_id: int, channel: discord.TextChannel):
        """
        セッションを開始する。
        :param user_id: 発言したユーザー(ちんちんマスターとなる)
        :param channel: 発言したユーザー
        """
        self.game_status = self.STATUS_RECRUITING
        self.joined_users = [user_id]
        self.chinchin_master_id = user_id
        self.session_channel = channel
        await channel.send(self.MESSAGES["opened"])

    async def join_game_session(self, user_id: int):
        """
        セッションに参加する
        :param user_id: 参加するユーザー
        """
        if user_id in self.joined_users:
            await self.session_channel.send(self.MESSAGES["already_joined"])
            return

        self.joined_users.append(user_id)

        await self.session_channel.send(self.MESSAGES["joined"])

    async def start_game_session(self, user_id: int):
        """
        募集を終了し、ゲームを開始する
        :param user_id: 発言したユーザー
        """
        if self.chinchin_master_id != user_id:
            await self.session_channel.send(self.MESSAGES["not_master"])
            return

        self.game_status = self.STATUS_GAME_STARTED
        await self.session_channel.send(self.MESSAGES["started"])

    async def finish_game_session(self, user_id: int):
        """
        ゲームを強制終了する
        :param user_id: 発言したユーザー
        """
        if self.chinchin_master_id != user_id:
            await self.session_channel.send(self.MESSAGES["not_master"])
            return

        self.game_status = self.STATUS_NOT_STARTED
        await self.session_channel.send(self.MESSAGES["manually_finished"])

    # ----------- クラスメソッドたち --------------

    @classmethod
    def get_summarized_regex(cls):
        """
        ちんちん侍ゲームのレスポンスすべてにマッチする正規表現を返す。
        """
        return re.compile("^(" + "|".join(cls.PREFIXLESS_COMMANDS_REGEX.values()) + ")$")
