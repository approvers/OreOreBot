import discord
import sys
import requests

import re

client = discord.Client()
token = sys.argv[1]

github_cmd_regex = re.compile(r".*?\#(.+)\/([^\s][0-9]+).*?")

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
        repo_name, num = matches[1:]

        res = requests.get("https://github.com/brokenManager/{}/issue/{}".format(repo_name, num))
        if res.status_code == 404:
            await channel.send("エラー：なんか違う")
        else:
            await channel.send("https://github.com/brokenManager/{}/issue/{}".format(repo_name, num))

client.run(token)




