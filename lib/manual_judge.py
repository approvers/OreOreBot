"""
全手動 †JUDGEMENT SYSTEM† の処理
クラス化する必要はなかった気がするすまん (繰り返される歴史)
"""
import discord
import asyncio
import random

from lib.util import Singleton

class ManualJudge(Singleton):
    """
    !jd / !judge コマンドの処理をするクラス
    """
    _MANUAL_JUDGE_MESSAGE = {
        "invalid-command":"引数は少なくとも1つは必要だよ...?",
        "count error": "回数は1回から30回にしてね"
    }
    def __init__(self,abc_emojis : dict):
        """
        初期化を行う ABCの絵文字を保持しているだけ
        Parameters
        ----------
        abc_emojis: dict<str:discord.Emoji>
            ABCの絵文字の辞書
            keyは以下の通り:
            "AC","WA","CE","TLE"
        """
        self.abc_emoji_dict = abc_emojis

    async def call(self,commands : list, channel : discord.channel):
        """
        !jd / !judge コマンドを受け取って処理をする巻数
        ----------
        commands: list<str>
            ユーザーが実際に入力したコマンドが格納されているリスト
            !プレフィックスを消して空白で区切ったやつ
        """
        if len(commands) <= 1:
            await channel.send(ManualJudge._MANUAL_JUDGE_MESSAGE["invalid-command"])
            return

        if commands[1] > 30 or commands[1] < 1:
            await channel.send(ManualJudge._MANUAL_JUDGE_MESSAGE["count_error"])
            return

        is_all_error = True if "-all" in commands else False
        print(is_all_error)
        if len(commands) >= 3:
            mode = commands[2].upper() if(commands[2].upper() in self.abc_emoji_dict.keys() and len(commands) >= 3) else "AC"
        else:
            mode = "AC"

        await channel.send("***†HARACHO ONLINE JUDGEMENT SYSTEM†***")
        await asyncio.sleep(1)

        if is_all_error:
            for n in range(1,int(commands[1])+1):
                await channel.send("```\n"+str(n)+"/"+commands[1]+" "+(mode)+"\n```")

                if n == int(commands[1]):
                    break

                await asyncio.sleep(random.uniform(0, 4))

        else:
            error_occurs_at = random.sample(range(1,int(commands[1])+1),random.randint(1,int(commands[1])+1))
            for n in range(1,int(commands[1])+1):
                if n in error_occurs_at:
                    await channel.send("```\n"+str(n)+"/"+commands[1]+" "+(mode)+"\n```")
                else:
                    await channel.send("```\n"+str(n)+"/"+commands[1]+" "+"AC"+"\n```")

                if n == int(commands[1]):
                    break

                await asyncio.sleep(random.uniform(0, 4))

        await channel.send(self.abc_emoji_dict[mode])
