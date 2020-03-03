import discord
import sys
import requests

import re

client = discord.Client()
token = sys.argv[1]

github_cmd_regex = re.compile(r".*?\#(.+?)\/([^\s]+).*?")
channel_id_regex = re.compile(r"^<#([0-9]+?)>$")

@client.event
async def on_ready():
    channel = client.get_channel(606107143879524374)
    await channel.send("やあ")


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
            await channel.send("エラー：リポがないんだけど")
            return

        if cmd == "top" or cmd == "t":
            await channel.send("https://github.com/brokenManager/" + repo_name)
        elif cmd == "issues" or cmd == "i":
            await channel.send("https://github.com/brokenManager/{}/issues".format(repo_name))
        elif cmd == "issue":
            await channel.send("エラー：知ってるか? issueは一つだけじゃないんだ")
        elif cmd == "pull" or cmd == "pr" or cmd == "p":
            await channel.send("https://github.com/brokenManager/{}/pulls".format(repo_name))
        elif not cmd.isnumeric():
            branch_sel = requests.get("https://github.com/brokenManager/{}/tree/{}".format(repo_name, cmd))
            auto_master_sel = requests.get("https://github.com/brokenManager/{}/tree/master/{}".format(repo_name, cmd))
            if branch_sel.status_code != 404:
                await channel.send("https://github.com/brokenManager/{}/tree/{}".format(repo_name, cmd))
            elif auto_master_sel.status_code != 404:
                await channel.send("masterブランチだよな? 違ったらちゃんと指定しろカス")
                await channel.send("https://github.com/brokenManager/{}/tree/master/{}".format(repo_name, cmd))
            else:
                await channel.send("エラー：そんなものはない")

                return
        else:
            res = requests.get("https://github.com/brokenManager/{}/issues/{}".format(repo_name, cmd))
            if res.status_code == 404:
                await channel.send("エラー：なんか違う")
                return
            await channel.send("https://github.com/brokenManager/{}/issues/{}".format(repo_name, cmd))

client.run(token)




