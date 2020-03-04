import discord
import datetime
import asyncio
import sys
import requests
import json
import codecs

import re

client = discord.Client()
token = sys.argv[1]
first_channel = sys.argv[2]
msg_dict = {}

github_cmd_regex = re.compile(r".*?\#(.+?)\/([^\s]+).*?")
channel_id_regex = re.compile(r"^<#([0-9]+?)>$")

try:
    # messages.json (時報json) の読み込みを試みる
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
        time = datetime.datetime.now()
        if int(str(time.minute)) == 0:
            h = str(time.hour)
            await channel.send(msg_dict[h])
        await asyncio.sleep(50)


@client.event
async def on_message(message):
    channel = message.channel
    m = message.content

    matches = github_cmd_regex.match(m)

    if matches is not None:

        # matches[0]だとmatch関数にかけた文字列が全部返ってくる(なぜ)
        repo_name = matches[1]
        cmd = matches[2]

        if repo_name.endswith(">"):
            repo_name = client.get_channel(int(repo_name[:-1])).name
        print("repo_name:{}\ncmd:{}".format(repo_name, cmd))

        res = requests.get("https://github.com/brokenManager/" + repo_name)
        if res.status_code == 404:
            await channel.send("司令官、そんなリポジトリはないよ...？")
            return

        if cmd == "top" or cmd == "t":
            await channel.send("司令官、頼まれていたリポジトリを持ってきたよ\nhttps://github.com/brokenManager/" + repo_name)
        elif cmd == "issues" or cmd == "i":
            await channel.send("司令官、このリポジトリで起きている問題のリストだよ\nhttps://github.com/brokenManager/{}/issues".format(repo_name))
        elif cmd == "issue":
            await channel.send("司令官、問題は一つじゃないんだよ?")
        elif cmd == "pull" or cmd == "pr" or cmd == "p":
            await channel.send("ぷるりくえすと...?\nよくわからないけどそれのリストだよ\nhttps://github.com/brokenManager/{}/pulls".format(repo_name))
        elif not cmd.isnumeric():
            branch_sel = requests.get("https://github.com/brokenManager/{}/tree/{}".format(repo_name, cmd))
            auto_master_sel = requests.get("https://github.com/brokenManager/{}/tree/master/{}".format(repo_name, cmd))
            if branch_sel.status_code != 404:
                await channel.send("https://github.com/brokenManager/{}/tree/{}".format(repo_name, cmd))
            elif auto_master_sel.status_code != 404:
                await channel.send("masterでいいんだよね?")
                await channel.send("https://github.com/brokenManager/{}/tree/master/{}".format(repo_name, cmd))
            else:
                await channel.send("???それはどういう意味だい?")

                return
        else:
            res = requests.get("https://github.com/brokenManager/{}/issues/{}".format(repo_name, cmd))
            if res.status_code == 404:
                await channel.send("司令官、そこには何もないよ?")
                return
            await channel.send("司令官、頼まれていた書類だよ\nhttps://github.com/brokenManager/{}/issues/{}".format(repo_name, cmd))
    elif "ハラショー" in message.content:
        emoji = client.get_emoji(684424533997912096)
        await channel.send(emoji)
    elif "おやすみ" == message.content:
        await channel.send("おやすみ、司令官。また明日")

client.run(token)




