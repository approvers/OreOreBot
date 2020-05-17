from typing import List, Dict, Union, Tuple
import requests
import discord
from src.on_message.commands.util.command_base import CommandBase
from src.on_message.commands.git_utils.base import Base
from src.on_message.commands.git_utils.repo import Repo
from src.on_message.commands.git_utils.issue import Issue
from src.on_message.commands.git_utils.pull import Pull
from src.on_message.commands.git_utils.branch import Branch

REPO_URL_TEMPLATE = "/repos/{}/{}/"


class Git(CommandBase):
    COMMAND = "git"
    COMMAND_TEMPLATE = \
        "{{prefix}}{command} <scope> <orgs> (<repos> <number/name>)"\
        .format(command=COMMAND)
    HELP = None

    def __init__(self, username: str, token: str):
        self.token: str = token
        auth = (username, token)
        self.get_func: Dict[str, Base] = {
            "repo": Repo(auth),
            "issue": Issue(auth),
            "pull": Pull(auth),
            "branch": Branch(auth)
        }

    async def execute(self, params: discord.Message):
        words: List[str] = params.content.split(" ")
        send_message_channel: discord.TextChannel = params.channel
        if len(words) < 3:
            await send_message_channel.send("not enought args")
            return

        scope = words[1]

        if scope not in self.get_func.keys():
            await send_message_channel.send("invalid scope")
            return

        orgs = words[2]

        if scope == "repos":
            repos = ""
            target = words[3] if len(words) >= 4 else ""

        if scope != "repos":
            if len(words) == 3:
                await send_message_channel.send("have to specify")
            repos = words[3]
            target = words[4] if len(words) >= 5 else ""

        self.get_func[scope].execute(
            orgs,
            repos,
            send_message_channel,
            target
        )

    def _get_pull_requests(self, orgs: str, repos: str) -> List[Response]:
        url_template = Git.GITHUB_API_URL.format(orgs, repos) + "pulls"
        response = requests.get(
            Git.GITHUB_API_URL + url_template,
            auth=self.auth
        )
        result = response.json()
        return result

