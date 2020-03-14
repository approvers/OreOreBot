import discord
import datetime
import asyncio
import sys
import os
import subprocess
import requests
import json
import codecs
from random import randint

from lib import scraping
from lib.weather import get_weather
from lib.util import Singleton
from lib.lol_counter import LolCounter

from message_command import MessageCommands

import re

CLIENT = discord.Client()
TOKEN = os.environ["TOKEN"]
lol_count = {}
typos = {}


async def typo_core(arg,typo_matches_text,message):
    author = message.author.id
    if not (author in typos.keys()):
        typos[author] = []
    if arg == "append" and not (typo_matches_text[:-3] == ""):
        typos[author].append(message.content[:-3])
    elif arg == "call":
        return typos[author]

async def generate_random(message, parentList):
    channel = message.channel
    result = randint(0, len(parentList))
    await channel.send(get_message("random-list", "message").format(parentList[result]))


@CLIENT.event
async def on_message(message):
    channel = message.channel
    m = message.content

    matches = GITHUB_CMD_REGEX.match(m)
    usr_cmd_matches = USER_CMD_REGEX.match(m)
    typo_matches = TYPO_REGEX.match(m)

    if not message.author.bot or message.author.id in ID_EXCEPTIONS:

        if matches is not None:

            # matches[0]だとmatch関数にかけた文字列が全部返ってくる(なぜ)
            repo_name = matches[1]
            cmd = matches[2]

            if repo_name.endswith(">"):
                repo_name = CLIENT.get_channel(int(repo_name[:-1])).name
            print("repo_name:{}\ncmd:{}".format(repo_name, cmd))

            res = requests.get("https://github.com/brokenManager/" + repo_name)
            if res.status_code == 404:
                res = requests.get("https://github.com/{}/{}".format(repo_name, cmd))
                if res.status_code == 404:
                    await channel.send(get_message("repo", "not-found"))
                else:
                    await channel.send(get_message("repo", "other_repo").format(repo_name, cmd))
                return
            if cmd == "top" or cmd == "t":
                await channel.send(get_message("repo", "repo-top").format(repo_name))
            elif cmd == "issues" or cmd == "i":
                await channel.send(get_message("issue-found", "issue-found").format(repo_name))
            elif cmd == "issue":
                await channel.send(get_message("repo", "single-issue"))
            elif cmd == "pull" or cmd == "pr" or cmd == "p":
                await channel.send(get_message("repo", "pullreq-found").format(repo_name))
            elif not cmd.isnumeric():
                branch_sel = requests.get("https://github.com/brokenManager/{}/tree/{}".format(repo_name, cmd))
                auto_master_sel = requests.get("https://github.com/brokenManager/{}/tree/master/{}".format(repo_name, cmd))
                if branch_sel.status_code != 404:
                    await channel.send(get_message("repo", "branch-selected").format(repo_name, cmd))
                elif auto_master_sel.status_code != 404:
                    await channel.send(get_message("repo", "master-suggested").format(repo_name, cmd))
                else:
                    await channel.send(get_message("repo", "file-not-found"))

                    return
            else:
                res = requests.get("https://github.com/brokenManager/{}/issues/{}".format(repo_name, cmd))
                if res.status_code == 404:
                    await channel.send(get_message("repo", "issue-not-found"))
                    return
                await channel.send(get_message("repo", "issue-found").format(repo_name, cmd))

        elif usr_cmd_matches is not None:
            usr_cmd_text = usr_cmd_matches.group().split()
            usr_cmd_text[0] = usr_cmd_text[0][1:]

            # /で実行される処理をこれの下に書いて下しあ
            # (例) !help a b c をユーザーが実行した場合 → usr_cmd_text = ["help","a","b","c"]となります

            if usr_cmd_text[0] == "lol":
                await lol_counter(is_count=False,message=message)

            if usr_cmd_text[0] == "stop":
                if len(usr_cmd_text) == 2:
                    if usr_cmd_text[1] == "confirm":
                        await channel.send(get_message("stop", "confirmed"))
                        sys.exit()
                else:
                    await channel.send(get_message("stop", "confirmation"))

            if usr_cmd_text[0] == "random":
                if len(usr_cmd_text[1:]) > 1:
                    await generate_random(message, usr_cmd_text[1:])
                else:
                    await channel.send(get_message("random", "no-lists-given"))

            if usr_cmd_text[0] == "help":
                await channel.send(r"""***はらちょhelp***
                ```!lol``` : 私が起動してから司令官が「草」って言った回数を伝えるよ
                ```!stop``` : 私が休憩してくるよ
                ```!random```: 指揮官の指定したものからランダムでうんたらかんたら # TODO
                ```#<リポジトリ名>/<top(p)|issues(i)|pull(pr | p)|>``` : 言われたように書類を持ってくるよ
                ```ハラショー``` : 秘密だよ
                ```おやすみ``` : 秘密だよ
                ```疲れた``` : 秘密だよ""")

            if usr_cmd_text[0] == "randomIssue":
                issue_list = scraping.get_issues()
                n = randint(0, len(issue_list))
                url = "https://github.com/brokenManager/{}/issues/{}".format(
                    issue_list[n]["repo"], issue_list[n]["id"]
                )
                mess = get_message("random-issue", "message")
                await channel.send(mess.format(url))

            if usr_cmd_text[0] == "upgrade":
                if os.name == "nt":
                    subprocess.call(os.path.dirname(__file__)+ r"/scripts/upgrade.bat" + " " + os.path.dirname(__file__)[0:2])
                if os.name == "posix":
                    subprocess.call(["sh", os.getcwd() + r"/scripts/upgrade.sh", os.getcwd()])

            if usr_cmd_text[0] == "typo":
                usr_typo_dict = await typo_core("call","",message)
                disp_typos = ""
                for one_typo in usr_typo_dict:
                    disp_typos += "・" + one_typo + "\n"
                await channel.send(get_message("typo-text","message").format(message.author.display_name,disp_typos))

        elif typo_matches is not None:
            typo_matches_text = typo_matches.group()
            await typo_core("append",typo_matches_text,message)

        elif "ハラショー" in message.content:
            emoji = CLIENT.get_emoji(684424533997912096)
            await channel.send(emoji)
        elif "おやすみ" == message.content:
            n = datetime.datetime.now(tz=JTC_TZ)
            await channel.send(get_message("goodnight", "common"))
            if str(n.hour) in ["0", "1", "2", "3", "4", "5", "6"]:
                await channel.send(get_message("goodnight", "unhealthy-time"))
            else:
                await channel.send(get_message("goodnight", "healthy-time"))
        elif "疲れた" in message.content:
            await channel.send(get_message("goodnight", "tired"))
        elif "草" in message.content:
            await lol_counter(is_count=True, message=message)
        elif "いっそう" in message.content:
            await channel.send(CLIENT.get_emoji(685162743317266645))
        if message.content.count("***") >= 2:
            await channel.send(get_message("bold-italic-cop", "message").format(HARASYO))

CLIENT.run(TOKEN)


class MainClient(discord.Client, Singleton):
    """
    Discordクライアント(多重起動防止機構付き)
    """
    CLI_BOTS = [
        685429240908218368, 
        684655652182032404, 
        685457071906619505        
    ]
    def __init__(self, token, base_channel_id):
        """
        クライアントを起動する前の処理
        tokenとか最初にメッセージ送信するチャンネルの指定をしたりする
        Parameters
        ----------
        token: str
            discordのBotのトークン
        base_channel_id: int
            ログインをし、時報を送信するチャンネルのid
        """
        super(MainClient, self).__init__()
        self.token = token
        self.base_channel_id = base_channel_id

        # Initialize in on_ready()
        # Because use value in client
        self.base_channel = None
        self.lol_counter  = None
        self.HARASYO      = None

        # mesm_json_syntax_conceal = 0sages.json (時報json) の読み込みを試みる
        # msg_dictのkeyはstr型です、int型で呼び出そうとしないで()
        with codecs.open("messages.json", 'r', 'utf-8') as f:
            self.msg_dict = json.loads(f.read())


    async def on_ready(self):
        """
        Clientの情報をもとにした初期化と時報の起動
        """
        if len(self.guilds) == 1:
            self.base_channel = self.get_channel(self.base_channel_id)
            self.lol_counter = LolCounter(self.guilds[0].members)
            self.HARASYO = CLIENT.get_emoji(684424533997912096)
            asyncio.ensure_future(self.ziho())

    async def on_message(self, message):
        if message.author.bot and not message.author.id in MainClient.CLI_BOTS:
            return
        channel = message.channel
        message_str = message.content
        command = MessageCommands(message_str, channel)
        command.execute()

    async def ziho(self):
        """
        時報を制御する関数
        """
        timezone = datetime.timezone(datetime.timedelta(hours=9))
        messages = self.msg_dict["ziho"]
        while True:
            time = datetime.datetime.now(tz=timezone)
            if time.minute == 0:
                hour = str(time.hour)
                await self.base_channel.send(messages[hour])
                if hour == "6":
                    weather = get_weather()["today"]
                    await home_channel.send(
                        "今日の天気は{}\n最高気温は{}℃で昨日と{}℃違うよ\n最低気温は{}℃で昨日と{}℃違うよ\n今日も頑張ってね"\ .format(
                            weather["weather"],
                            weather["high"],
                            weather["high_diff"][1:-1],
                            weather["low"],
                            weather["low_diff"][1:-1]
                        )
                    )
            if hour == "19":
                weather = get_weather()["tomorrow"]
                await home_channel.send(
                    "明日の天気は{}\n最高気温は{}℃で今日と{}℃違うよ\n最低気温は{}℃で今日と{}℃違うよ\n今日も1日お疲れ様"\
                    .format(
                        weather["weather"],
                        weather["high"],
                        weather["high_diff"][1:-1],
                        weather["low"],
                        weather["low_diff"][1:-1]
                    )
                )
            await asyncio.sleep(15)
        await asyncio.sleep(50)

    def launch(self):
        self.run(self.token)

