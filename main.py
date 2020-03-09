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

import lib.scraping

import re

client = discord.Client()
token = os.environ["TOKEN"]
first_channel = 684289417682223150
lol_count = {}

github_cmd_regex = re.compile(r".*?\#(.+?)\/([^\s]+).*?")
channel_id_regex = re.compile(r"^<#([0-9]+?)>$")
usr_cmd_regex = re.compile(r"^!(\w+?)*(\s\w+)*")

jtc_tz = datetime.timezone(datetime.timedelta(hours=9))

try:
    # mesm_json_syntax_conceal = 0sages.json (時報json) の読み込みを試みる
    # msg_dictのkeyはstr型です、int型で呼び出そうとしないで()
    with codecs.open("messages.json", 'r', 'utf-8') as f:
        msg_dict = json.loads(f.read())
except:
    print("File doesn't exist or it is incorrect!")



@client.event
async def on_ready():
    channel = client.get_channel(int(first_channel))
    await channel.send(msg_dict["login"])
    asyncio.ensure_future(ziho(channel))



async def ziho(channel):
    while True:
        time = datetime.datetime.now(tz=jtc_tz)
        if int(str(time.minute)) == 0:
            h = str(time.hour)
            await channel.send(msg_dict["ziho"][h])
            await asyncio.sleep(15)
        await asyncio.sleep(50)

async def lol_counter(is_count,message):
    channel = message.channel
    if is_count:
        if message.author.id in lol_count:
            lol_count[message.author.id] += message.content.count("草")
        else:
            lol_count[message.author.id] = 1
    else:
        await channel.send(get_message("lol-counter", "counter-value").format(lol_count[message.author.id]))
        if lol_count[message.author.id] > 10:
            await channel.send(get_message("lol-counter", "too-many"))

async def generate_random(message, parentList):
    channel = message.channel
    result = randint(0, len(parentList))
    await channel.send(get_message("random-list", "message").format(parentList[result])) # TODO
    # 文字列の中に変数入れるやり方忘れたのでhibikiness追加するときやって下さ

def get_message(scope, name):
    """
    Get message from JSON.
    :param scope: test
    """
    msg_data = msg_dict[scope][name]
    
    message = ""
    if isinstance(msg_data, list):
        message = msg_data[randint(0, len(msg_data))]
    else:
        message = msg_data

    return message


@client.event
async def on_message(message):
    channel = message.channel
    m = message.content

    matches = github_cmd_regex.match(m)
    usr_cmd_matches = usr_cmd_regex.match(m)

    if not message.author.bot or message.author.id == 684655652182032404:

        if matches is not None:

            # matches[0]だとmatch関数にかけた文字列が全部返ってくる(なぜ)
            repo_name = matches[1]
            cmd = matches[2]

            if repo_name.endswith(">"):
                repo_name = client.get_channel(int(repo_name[:-1])).name
            print("repo_name:{}\ncmd:{}".format(repo_name, cmd))

            res = requests.get("https://github.com/brokenManager/" + repo_name)
            if res.status_code == 404:
                await channel.send(get_message("repo", "not-found"))
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
                issue_list = lib.scraping.get_issues()
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

        elif "ハラショー" in message.content:
            emoji = client.get_emoji(684424533997912096)
            await channel.send(emoji)
        elif "おやすみ" == message.content:
            n = datetime.datetime.now(tz=jtc_tz)
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
            await channel.send(client.get_emoji(685162743317266645))
        if message.content.count("***") >= 2:
            emoji = client.get_emoji(684424533997912096)
            await channel.send(get_message("bold-italic-cop", "message").format(emoji))

client.run(token)
