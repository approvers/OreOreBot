import discord
import datetime
import asyncio
import sys
import requests

import re

client = discord.Client()
token = sys.argv[1]

github_cmd_regex = re.compile(r".*?\#(.+?)\/([^\s]+).*?")
channel_id_regex = re.compile(r"^<#([0-9]+?)>$")

ziho_list = [
    "Полночь.…失礼、マルマルマルマル。",
    "マルヒトマルマル。深夜だね。",
    "マルフタマルマル。静かな海は…嫌いじゃない。",
    "マルサンマルマル。眠かったらどうぞ。私の膝を貸そうか。",
    "マルヨンマルマル。私は任務中に眠くならない。",
    "マルゴーマルマル。空の色が変わる頃だ。…綺麗だな。",
    "マルロクマルマル。司令官、悪いがちょっと重い…。",
    "マルナナマルマル、朝だ。朝食を摂ろう。",
    "マルハチマルマル。任務を始めようか。",
    "マルキュウマルマル。艦隊に、遠征の指示を。",
    "ヒトマルマルマル。司令官、残った艦は、私が引き受けよう。",
    "ヒトヒトマルマル。皆を連れて、演習してこようか。",
    "Полдень.…失礼、ヒトフタマルマル。気を抜くと言葉が…。気をつける。",
    "ヒトサンマルマル。今日のランチは…ハイ、これ。ピロシキだ。",
    "ヒトヨンマルマル。午後の艦隊勤務を始めよう。疲れてはいない。",
    "ヒトゴーマルマル。引き続き、訓練だ。疲労の溜まっている艦は休ませよう。",
    "ヒトロクマルマル。全艦隊戻ったら、反省会だ。",
    "ヒトナナマルマル。司令官、さぁ皆に一言を。",
    "ヒトハチマルマル。何？司令官。これから演習の予定だけど。",
    "ヒトキュウマルマル。訓練がきついって？それは済まなかった。",
    "フタマルマルマル。司令官、カレーは…ちょっとわからない。",
    "フタヒトマルマル。今夜はボルシチでどう？私のは美味い。",
    "フタフタマルマル。ボルシチ、皆も喜んでくれた。嬉しいな。",
    "フタサンマルマル。司令官、今日も一日、お疲れ様。"
]

@client.event
async def on_ready():
    channel = client.get_channel(684289417682223150)
    await channel.send("響だよ。その活躍ぶりから不死鳥の通り名もあるよ。")
    asyncio.ensure_future(zijo(channel))


async def zijo(channel):
    while True:
        time = datetime.datetime.now()
        print("hey")
        if int(str(time.minute)) == 0:
            h = str(time.hour)
            await channel.send(ziho_list[int(h)])
        await asyncio.sleep(5)


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




