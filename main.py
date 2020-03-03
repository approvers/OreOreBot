import discord
import sys

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
    print(m)
    if "#" in message.content:
        start_index = m.find("#")
        end_index = m[start_index:].find(" ")
        if end_index == -1:
            keys = m[start_index + 1:].split("/")
        else:
            keys = m[start_index + 1: end_index].split("/")
        repo_name = keys[0]
        if ">" in repo_name:
            i = int(repo_name[:-1])
            ch = client.get_channel(i)
            repo_name = ch.name
        command = ""
        if keys[1] in ["pr", "PR"]:
            command = "pulls"
        elif keys[1] in ["Issue", "issue", "is"]:
            command = "issues"
        else:
            channel.send("コマンドミスっとるで")
        num = keys[2]
        await channel.send("https://github.com/brokenManager/{}/{}/{}".format(repo_name, command, num))

client.run(token)




