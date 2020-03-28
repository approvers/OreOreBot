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
        "invalid-argument":"引数の形式がまちがっているよ...?",
        "invalid-command":"引数は少なくとも1つは必要だよ...?",
        "too-many-judges":"回数は1回から30回にしてね",
        "no-such-error":"そんなエラーはないよ...?"
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

    async def checker(self,commands : list, channel : discord.channel):
        """
        !jd / !judge コマンドの書式を確認して実行の可否を判断する関数
        ただし実際は可否を判断しているだけで実行する機能自体はない
        エラーメッセージは送信するようになっている
        Parameters
        ----------
        commands: list<str>
            ユーザーが実際に入力したコマンドが格納されているリスト
            !プレフィックスを消して空白で区切ったやつ
        Returns
        ----------
        allow_or_not: bool
            コマンドに問題がないかを格納している
            問題があればTrue問題がなければFalse
        """

        # I.第二引数がint型にキャスト可能かどうか
        try:
            int(commands[1]) # 変更可能性あり
        except:
            await channel.send(ManualJudge._MANUAL_JUDGE_MESSAGE["invalid-argument"])
            return True

        # II.第二引数が0より大きく30以下かどうか
        if not (0 < int(commands[1]) <= 30):
            await channel.send(ManualJudge._MANUAL_JUDGE_MESSAGE["too-many-judges"])
            return True

        # 此処から先は任意で引数の有無が決まるのでチェックするかどうかを判定
        if len(commands) >= 3:

            # III.第三引数が正しいオプションか判定
            if not (commands[2] in self.abc_emoji_dict.keys()):
                await channel.send(ManualJudge._MANUAL_JUDGE_MESSAGE["no-such-error"])
                return True

        return False

    async def call(self,commands : list, channel : discord.channel):
        """
        !jd / !judge コマンドを受け取って処理をする関数
        ----------
        commands: list<str>
            ユーザーが実際に入力したコマンドが格納されているリスト
            !プレフィックスを消して空白で区切ったやつ
        """

        # checkerに通す ダメならブロック
        if (await self.checker(commands, channel)):
            return

        if int(commands[1]) > 30 or int(commands[1]) < 1:
            await channel.send(ManualJudge._MANUAL_JUDGE_MESSAGE["count_error"])
            return

        is_all_error = True if "-all" in commands else False

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
