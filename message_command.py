"""
ユーザーのメッセージから実行するコマンド群
"""
import re
import codecs
import json
import requests
from lib.lol_counter import LolCounter
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

    def __init__(self, message, channel, member_id):
        """
        インスタンス化の際に必要インスタンスを受け取る
        message: str
            メッセージの文章
        channel: discord.Channel
            メッセージ送信先のチャンネル
        lol_counter: LolCounter
            草カウンターのインスタンスを受け取る
        member_id: int
            発言者のid
        """
        if MessageCommands.LOL_COUNTER is None:
            return

        self.message     = message
        self.channel     = channel
        self.lol_counter = lol_counter
        self.member      = member

        with codecs.open("messages.json", 'r', 'utf-8') as f:
            self.response_dict = json.loads(f.read())
        for (key, regex) in MessageCommands.REGEXES.items():
            if regex.match(message):
                self.command_type = key
                self.command      = regex.match(message)
                return
        if self.command_type is None:
            self.command_type = ""

    def execute(self):
        if not self.command_type:
            return
        commands_list = {
            "GitHub"      : self.github(),
            "Util Command": self.util_command(),
            "Typo"        : self.typo()
        }
        commands_list[self.command_type]

    def github(self):
        repo_name, command = self.command[1: 3]
        message = self.response_dict["repo"]
        channel = self.channel

        converter = {
            "t": "top",
            "i": "issues",
            "pr": "pull",
            "p": "pull"
        }


        if repo_name.endswith(">"):
            repo_name = channel.get_channel(int(repo_name[:-1])).name

        res = requests.get("https://github.com/brokenManager/" + repo_name)
        if res.status_code == 404:
            self.try_connect_other_repo(repo_name, command, message)
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

    def try_connect_other_repo(self, user_name, repo_name, message):
        res = requests.get("https://github.com/{}/{}".format(user_name, repo_name))
        if res.status_code == 404:
            await self.channel.send(message["not-found"])
        else:
            await self.channel.send(message["other_repo"].format(user_name, repo_name))

    def util_command(self):
        user_message = self.message[1:]        
        commands = user_message.split()
        
        if commands[0] == "lol":
            await MessageCommands.LOL_COUNTER.output(self.channel, self.member)
            return

        

    def typo(self):
        return
    
    @staticmethod
    def get_lol_counter(members):
        """
        lol_counterをこのインスタンスに渡す処理
        Parameters
        ----------
        members: List<discord.Member>
            メンバーのリスト
        """
        if MessageCommands.LOL_COUNTER:
            return
        MessageCommands.LOL_COUNTER = LolCounter(members)

