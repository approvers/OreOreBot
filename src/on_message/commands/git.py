from typing import List, Dict, Union, Tuple
import requests
import discord
from src.on_message.commands.util.command_base import CommandBase

REPO_URL_TEMPLATE = "/repos/{}/{}/"

class Git(CommandBase):
    COMMAND = "git"
    COMMAND_TEMPLATE = \
        "!{} <scope> <orgs> (<repos> <number/name>)".format(COMMAND)
    HELP = None

    def __init__(self, username: str, token: str):
        self.token: str = token
        auth = (username, token)
        self.get_func = {
            "repo": Repo(auth),
            "issue": Issue(auth),
            "pull": Pull(auth),
            "branch": Branch(auth)
        }

    async def execute(self, params: discord.Message):
        messages = params.content.split(" ")
        send_message_send: discord.TextChannel = params.channel
        if len(messages) < 3:
            await send_message_send.send("not enought args")
            return

        scope = messages[1]
        orgs = messages[2]
        if scope not in self.get_func.keys():
            await send_message_send.send("invalid scope")
            return

    def _get_issues(self, orgs: str, repos: str) -> List[Response]:
        url_template = Git.GITHUB_API_URL.format(orgs, repos) + "issues"
        response = requests.get(
            Git.GITHUB_API_URL + url_template,
            auth=self.auth
        )
        result = response.json()
        return result

    def _get_pull_requests(self, orgs: str, repos: str) -> List[Response]:
        url_template = Git.GITHUB_API_URL.format(orgs, repos) + "pulls"
        response = requests.get(
            Git.GITHUB_API_URL + url_template,
            auth=self.auth
        )
        result = response.json()
        return result

    def _get_branches(self, orgs: str, repos: str) -> List[Response]:
        url_template = Git.GITHUB_API_URL.format(orgs, repos) + "branches"
        response = requests.get(
            Git.GITHUB_API_URL + url_template,
            auth=self.auth
        )
        result = response.json()
        return result
