import discord
import sys
import requests

import re

client = discord.Client()
token = sys.argv[1]

github_cmd_regex = re.compile(r".*?\#(.+)\/([^\s].+).*?")
channel_id_regex = re.compile(r"^<#([0-9]+?)>$")

@client.event
async def on_ready():
    channel = client.get_channel(684289417682223150)
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

        if channel_id_regex.match(repo_name[1:]) is not None:
            repo_name = client.get_channel(int(channel_id_regex.match(repo_name[1:])[1]))
        print("repo_name:{}\ncmd:{}".format(repo_name, cmd))

        res = requests.get("https://github.com/brokenManager/" + repo_name)
        if res.status_code == 404:
            await channel.send("エラー：リポがないんだけど")

        if cmd is "top" or cmd is "t":
            await channel.send("https://github.com/brokenManager/" + repo_name)
        elif cmd is "issues" or cmd is "i":
            await channel.send("https://github.com/brokenManager/{}/issues".format(repo_name))
        elif cmd is "issue":
            await channel.send("エラー：知ってるか? issueは一つだけじゃないんだ")
        elif not cmd.isnumeric():
            branch_sel = requests.get("https://github.com/brokenManager/{}/tree/{}".format(repo_name, cmd))
            if branch_sel.status_code == 404:
                auto_master_sel = requests.get("https://github.com/brokenManager/{}/tree/master/{}".format(repo_name, cmd))
                if auto_master_sel.status_code == 404:
                    await channel.send("エラー：そんなものはない\nもしパスの途中に半角スペースがあったら†悔い改めて†\nあとブランチ名も確かめて、どうぞ")
                return
        else:
            res = requests.get("https://github.com/brokenManager/{}/issues/{}".format(repo_name, cmd))
            if res.status_code == 404:
                await channel.send("エラー：なんか違う")
            await channel.send("https://github.com/brokenManager/{}/issues/{}".format(repo_name, cmd))

client.run(token)




