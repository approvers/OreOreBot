import discord
import sys
import requests

client = discord.Client()
token = sys.argv[1]


@client.event
async def on_ready():
    channel = client.get_channel(684289417682223150)
    await channel.send("やあ")


@client.event
async def on_message(message):
    channel = message.channel
    m = message.content
    if "#" in message.content:
        start_index = m.find("#")
        end_index = m[start_index:].find(" ")
        if end_index == -1:
            keys = m[start_index + 1:].split("/")
        else:
            keys = list(m[start_index + 1: end_index + start_index].split("/"))
        print(keys)
        repo_name = keys[0]
        if ">" in repo_name:
            i = int(repo_name[:-1])
            ch = client.get_channel(i)
            repo_name = ch.name
        command = ""
        num = keys[1]
        for s in ["issues", "pull"]:
            res = requests.get("https://github.com/brokenManager/{}/{}/{}".format(repo_name, s, num))
            if res.status_code != "404":
                command = s
                break
        if command == "":
            await channel.send("エラー：なんか違う")
        else:
            await channel.send("https://github.com/brokenManager/{}/{}/{}".format(repo_name, command, num))

client.run(token)




