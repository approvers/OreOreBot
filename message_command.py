"""
ユーザーのメッセージから実行するコマンド群
"""
import re
import codecs
import json
import datetime
import os

import requests
import discord

from lib.lol_counter import LolCounter
from lib.typo import Typo
from lib.manual_judge import ManualJudge
from lib.party_ichiyo import PartyIchiyo
from lib.kaere import Kaere
from lib.role import role
from lib.kokusei_chousa import number
from lib.voiceman import VoiceRole


class MessageCommands:
    """
    こいつをもとにメッセージコマンドを実行します
    """
    REGEXES = {
        "GitHub"      : re.compile(r".*?\#(.+?)\/([^\s]+).*?"),
        "Channel"     : re.compile(r"^<#([0-9]+?)>$"),
        "Util Command": re.compile(r"^!(\w+?)*(\s\w+)*"),
        "Typo"        : re.compile(r"^.*だカス$")
    }

    HARASYO = None
    ISSO = None

    MESSAGE_COMMANDS = {
        "ハラショー": None,
        "いっそう"  : None,
        "疲れた"    : "大丈夫?司令官\n開発には休息も必要だよ。しっかり休んでね",
        "おやすみ"  : "おやすみ、司令官。"
    }


    def __init__(self, message: str, channel: discord.TextChannel, member: discord.Member):
        """
        インスタンス化の際に必要インスタンスを受け取る
        message: str
            メッセージの文章
        channel: discord.Channel
            メッセージ送信先のチャンネル
        member: discord.Member
            発言者のMemberインスタンス
        """
        if MessageCommands.LOL_COUNTER is None:
            return

        self.message     = message
        self.channel     = channel
        self.member_id   = member.id
        self.member_name = member.display_name

        with codecs.open(os.getcwd() + "/messages.json", 'r', 'utf-8') as json_file:
            self.response_dict = json.loads(json_file.read())

    async def execute(self):
        """
        __init__で渡された情報をもとにコマンドを実行
        """
        if "草" in self.message or "くさ" in self.message:
            MessageCommands.LOL_COUNTER.count(self.message, self.member_id)

        if self.message.count("***") >= 2:
            await self.channel.send(
                self.response_dict["bold-italic-cop"]["message"].format(MessageCommands.MESSAGE_COMMANDS["ハラショー"])
            )

        for content in MessageCommands.MESSAGE_COMMANDS.keys():
            if content in self.message:
                await self.channel.send(MessageCommands.MESSAGE_COMMANDS[content])
                if content == "おやすみ":
                    await self.channel.send(MessageCommands.goodnight_time())

        command_type = None

        for (key, regex) in MessageCommands.REGEXES.items():
            if regex.match(self.message):
                command_type = key
                command      = regex.match(self.message)
                break

        if not command_type:
            return

        commands_list = {
            "GitHub"      : self.github,
            "Util Command": self.util_command,
            "Typo"        : self.typo
        }

        await commands_list[command_type](command)

    @staticmethod
    def goodnight_time():
        """
        時間によってコマンドの内容を変える
        """
        time = datetime.datetime.now()
        if 7 > time.hour > 0:
            return "こんな時間まで何してたんだい？\n風邪引いちゃうから明日は早めに寝なよ?"
        return "また明日"


    async def github(self, raw_command):
        """
        GitHubのリポジトリ参照などのコマンド
        Parameters
        ----------
        raw_command: re.Match
            正規表現に引っかかったコマンド達
        """
        repo_name = raw_command[1]
        command   = raw_command[2]
        message = self.response_dict["repo"]
        channel = self.channel

        converter = {
            "t": "top",
            "i": "issues",
            "pr": "pull",
            "p": "pull"
        }


        res = requests.get("https://github.com/brokenManager/" + repo_name)
        if res.status_code == 404:
            await self.try_connect_other_repo(repo_name, command, message)
            return

        if command in converter.keys():
            command = converter[command]

        if command in message.keys():
            await channel.send(message[command].format(repo_name))
            return

        if command.isdecimal():
            response_issue = requests.get("https://github.com/brokenManager/{}/issues/{}".format(repo_name, command))
            if response_issue.status_code == 404:
                await channel.send(message["issue-not-found"])
            else:
                await channel.send(message["issue-found"].format(repo_name, command))
            return

        branch = requests.get(
            "https://github.com/brokenManager/{}/tree/{}".format(repo_name, command)
        )
        master = requests.get(
            "https://github.com/brokenManager/{}/tree/master/{}".format(repo_name, command)
        )

        if branch.status_code != 404:
            await channel.send(message["branch-selected"].format(repo_name, command))
            return
        if master.status_code != 404:
            await channel.send(message["master-suggested"].format(repo_name, command))
            return
        await channel.send(message["file-not-found"])

    async def try_connect_other_repo(self, user_name: str, repo_name: str, message: dict):
        """
        他のユーザーやグループのリポジトリにアクセスを試みる
        Parameters
        ----------
        user_name: str
            アクセス先のユーザー/グループ名
        repo_name: str
            アクセス先のリポジトリの名前
        message: dict<str, str>
            送信するメッセージのテンプレートの辞書
        """
        res = requests.get("https://github.com/{}/{}".format(user_name, repo_name))
        if res.status_code == 404:
            await self.channel.send(message["not-found"])
        else:
            await self.channel.send(message["other_repo"].format(user_name, repo_name))

    async def util_command(self, _):
        """
        lolやtypoなどのコマンドを処理する
        """
        user_message = self.message[1:]
        commands = user_message.split()

        if commands[0] == "lol":
            await MessageCommands.LOL_COUNTER.output(self.channel, self.member_id)
            return

        if commands[0] == "typo":
            await self.channel.send(
                MessageCommands.TYPO_COUNTER.call(self.member_id, self.member_name)
            )
            return

        if commands[0].lower() in ["jd" or "judge"]:
            await MessageCommands.MANUAL_JUDGE.call(commands, self.channel)
            return

        if commands[0].lower() == "partyichiyo":
            await MessageCommands.PARTY_ICHIYO.change_command(commands, self.channel)
            return

        if commands[0].lower() == "kaere":
            await MessageCommands.KAERE.command_controller(commands, self.member_name)
            return

        if commands[0].lower() in ["number", "zinnkou", "zinkou", "population"]:
            await number(self.channel)
            return

        if commands[0].lower() == "role":
            await role(commands, self.channel, self.member_name)
            return

        if commands[0].lower() == "reset" and commands[1].lower() == "rold":
            await VoiceRole.reset_roles(members=MessageCommands.members, respond_ch=self.channel)
            return

    async def typo(self, raw_command: list):
        """
        typoを記録するコマンド
        Parameters
        ----------
        raw_command: list<str>
            コマンドの入ったリスト
        """
        command = raw_command.group()
        MessageCommands.TYPO_COUNTER.append(self.member_id, command)

    @staticmethod
    def static_init(members: list, harasyo: discord.Emoji, isso: discord.Emoji, abc_emojis: dict,
                    base_voice_channel: discord.TextChannel, kikisen_channel: discord.VoiceChannel,
                    hakaba_voice_channel: discord.VoiceChannel):
        """
        lol_counterをこのインスタンスに渡す処理
        Parameters
        ----------
        members: List<discord.Member>
            メンバーのリスト
        harasyo: discord.Emoji
            ハラショーって言った際に返信するemoji
        isso: discord.Emoji
            いっそうって言った際に返信するemoji
        base_voice_channel: discord.VoiceChannel
            一般ボイスチャンネル PartyIchiyoはここに出てくる
        kikisen_channel: discord.TextChannel
            聞き専のテキストチャンネル PartyIchiyoのテキスト通知もここ
        """
        if hasattr(MessageCommands, "LOL_COUNTER"):
            return
        MessageCommands.MESSAGE_COMMANDS["ハラショー"] = harasyo
        MessageCommands.MESSAGE_COMMANDS["いっそう"] = isso
        MessageCommands.members = members
        MessageCommands.LOL_COUNTER = LolCounter(members)
        MessageCommands.TYPO_COUNTER = Typo(members)
        MessageCommands.MANUAL_JUDGE = ManualJudge(abc_emojis)
        MessageCommands.PARTY_ICHIYO = PartyIchiyo(base_voice_channel, kikisen_channel)
        MessageCommands.KAERE = Kaere(base_voice_channel, kikisen_channel, hakaba_voice_channel)
