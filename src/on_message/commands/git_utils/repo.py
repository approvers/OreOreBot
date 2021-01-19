from typing import List, Tuple, Union
import requests

import discord

from src.on_message.commands.git_utils.base import Base, Response


class Repo(Base):
    def __init__(self, auth: Tuple[str, str]):
        super().__init__(auth)
        self.auth = auth

    async def execute(
            self,
            orgs: str,
            _: str,
            send_message_channel: discord.TextChannel,
            target: Union[str, int, None]
    ):
        repos: List[Response] = self._get(orgs, "")
        if target is None:
            await self.showAll(repos, send_message_channel)
            return

        if isinstance(target, str):
            await self.searchRepo(
                repos,
                send_message_channel,
                target
            )
            return

    async def showAll(
            self,
            repos: List[Response],
            send_message_channel: discord.TextChannel
    ):
        for repo in repos:
            message = \
                "```\nname: {}\nurl: {}```"\
                .format(repo["name"], repo["url"])
            await send_message_channel.send(message)

    async def searchRepo(
            self,
            repos: List[Response],
            send_message_channel: discord.TextChannel,
            keyword: str
    ):
        found_repos = [repo for repo in repos if keyword in repo["name"]]
        if len(found_repos) == 0:
            await send_message_channel.send("repository not found")
            return

        for repo in found_repos:
            message = \
                "```\nname: {}\nurl: {}```"\
                .format(repo["name"], repo["url"])

            await send_message_channel.send(message)

    def _get(self, orgs: str, _: str) -> List[Response]:
        url_template = "/orgs/{}/repos".format(orgs)
        response = requests.get(
            Repo.GITHUB_API_URL + url_template,
            auth=self.auth
        )
        if response.status_code != 200:
            raise RuntimeError("なんかばぐった:{}".format(response.status_code))
        result = response.json()
        return result
