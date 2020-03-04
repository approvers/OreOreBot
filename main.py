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
lol_count = {}

github_cmd_regex = re.compile(r".*?\#(.+?)\/([^\s]+).*?")
channel_id_regex = re.compile(r"^<#([0-9]+?)>$")
usr_cmd_regex = re.compile(r"^!(\w+?)*(\s\w+)*")

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

async def lol_counter(is_count,message):
    channel = message.channel
    if is_count:
        if message.author.id in lol_count:
            lol_count[message.author.id] += message.content.count("草")
        else:
            lol_count[message.author.id] = 1
    else:
        await channel.send("私が起きてから、司令官は{}回「草」って言ってるね".format(lol_count[message.author.id]))
        if lol_count[message.author.id] > 10:
            await channel.send("...いくら何でも多すぎないかい?")




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
                        await channel.send("司令官、先に休ませてもらうね。\nお疲れ様")
                        sys.exit()
                else:
                    await channel.send("私がいなくても大丈夫かい?")
                    await channel.send("大丈夫だったら,```/stop confirm```って言ってね。")

            if usr_cmd_text[0] == "help":
                await channel.send(r"""***はらちょhelp***
                ```/lol``` : 私が起動してから司令官が「草」って言った回数を伝えるよ
                ```/stop``` : 私が休憩してくるよ
                ```#<リポジトリ名>/<top(p)|issues(i)|pull(pr | p)|>``` : 言われたように書類を持ってくるよ
                ```ハラショー``` : 秘密だよ
                ```おやすみ``` : 秘密だよ
                ```疲れた``` : 秘密だよ""")

        elif "ハラショー" in message.content:
            emoji = client.get_emoji(684424533997912096)
            await channel.send(emoji)
        elif "おやすみ" == message.content:
            n = datetime.datetime.now()
            if str(n.hour) in ["0", "1", "2", "3", "4", "5", "6"]:
                await channel.send("おやすみ、司令官。\nこんな時間まで何してたんだい？\n風邪引いちゃうから明日は早めに寝なよ?")
            else:
                await channel.send("おやすみ、司令官。また明日")
        elif "疲れた" in message.content:
            await channel.send("大丈夫?司令官\n開発には休息も必要だよ。しっかり休んでね")
        elif "草" in message.content:
            await lol_counter(is_count=True, message=message)

client.run(token)
