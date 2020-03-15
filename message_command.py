"""
ユーザーのメッセージから実行するコマンド群
"""
import re
import codecs
import json
import requests
import datetime
from lib.lol_counter import LolCounter
from lib.typo import Typo

import discord

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

    MESSAGE_COMMANDS ={
        "ハラショー": HARASYO,
        "いっそう"  : ISSO,
        "疲れた"    : "大丈夫?司令官\n開発には休息も必要だよ。しっかり休んでね",
        "おやすみ"  : "おやすみ司令官、ゆっくり休んでね"
    }


    def __init__(self, message, channel, member):
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
        self.member_id   = member.author.id
        self.member_name = member.author.display_name

        with codecs.open("messages.json", 'r', 'utf-8') as f:
            self.response_dict = json.loads(f.read())

    async def execute(self):
        if "草" in self.message:
            MessageCommands.LOL_COUNTER.count(self.message, self.member_id)
        
        if self.message.count("***") >= 2:
            await self.channel.send(self.response_dict["bold-italic-cop"]["message"].format(MessageCommands.HARASYO))

        for content in MessageCommands.MESSAGE_COMMANDS.keys():
            if content in self.message:
                await self.channel(MessageCommands.MESSAGE_COMMANDS[content])
                if content == "おやすみ":
                    await self.channel.send(MessageCommands.goodnight_time())

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
        time = datetime.datetime.now()
        if time.hour in [x for x in range(7)]:
            return "こんな時間まで何してたんだい？\n風邪引いちゃうから明日は早めに寝なよ?"
        return "また明日"


    async def github(self, raw_command):
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
            response_issue = requests.get("https://github.com/brokenManager/{}/issues/{}")
            if res.status_code == 404:
                await channel.send(message["issue-not-found"])
            else:
                await channel.send(message["issue-found"].format(repo_name, command))
            return

        branch = requests.get("https://github.com/brokenManager/{}/tree/{}".format(repo_name, command))
        master = requests.get("https://github.com/brokenManager/{}/tree/master/{}".format(repo_name, command))

        if branch.status_code != 404:
            await channel.send(message["branch-selected"].format(repo_name, command))
        elif master.status_code != 404:
            await channel.send(message["master-suggested"].format(repo_name, command))
        else:
            await channel.send(message["file-not-found"])
        return

    async def try_connect_other_repo(self, user_name, repo_name, message):
        res = requests.get("https://github.com/{}/{}".format(user_name, repo_name))
        if res.status_code == 404:
            await self.channel.send(message["not-found"])
        else:
            await self.channel.send(message["other_repo"].format(user_name, repo_name))

    async def util_command(self, raw_command):
        user_message = self.message[1:]        
        commands = user_message.split()
        
        if commands[0] == "lol":
            await MessageCommands.LOL_COUNTER.output(self.channel, self.member_id)
            return
        
        if commands[0] == "typo":
            await self.channel.send(
                MessageCommands.TYPO_COUNTER.call(self.member_id, self.member_name)
            )

    async def typo(self, raw_command):
        command = raw_command.group()
        MessageCommands.TYPO_COUNTER.append(self.member_id, command)
    
    @staticmethod
    def static_init(members, harasyo, isso):
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
        """
        if hasattr(MessageCommands, "LOL_COUNTER"):
            return
        MessageCommands.LOL_COUNTER = LolCounter(members)
        MessageCommands.HARASYO = harasyo
        MessageCommands.ISSO    = isso
        MessageCommands.TYPO_COUNTER = Typo(members)
