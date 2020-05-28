from typing import Tuple, Dict, Union, List
import discord
import requests
from src.on_message.commands.git_utils.base import Base, Response


class Branch(Base):
    async def execute(
            self,
            orgs: str,
            repos: str,
            send_message_channel: discord.TextChannel,
            target: Union[str, int, None]
    ):
        branches: Response = self._get(orgs, repos)
        if target is None:
            await self.showAll(branches, send_message_channel)

        if isinstance(target, str):
            self.searchRepo(branches, send_message_channel, target)

    async def showAll(
        self,
        branches: List[Response],
        send_message_channel: discord.TextChannel
    ):
        for branch in branches:
            message = \
                "```\nname: {}\nurl: {}```"\
                .format(branch["name"], branch["url"])
            await send_message_channel.send(message)

    async def searchRepo(
        self,
        branches: List[Response],
        send_message_channel: discord.TextChannel,
        keyword: str
    ):
        found_branches = [
            branch for branch in branches if keyword in branch["name"]
        ]

        if len(found_branches) == 0:
            await send_message_channel.send("branch not found with keyword")
            return

        for branch in found_branches:
            message = \
                "```\nname: {}\nurl: {}```"\
                .format(branch["name"], branch["url"])
            await send_message_channel.send(message)

    def _get(self, orgs: str, repos: str) -> List[Response]:
        url_template = "/repos/{}/{}/branches".format(orgs, repos)
        response = requests.get(
            Branch.GITHUB_API_URL + url_template,
            auth=self.auth
        )
        if response.status_code != 200:
            raise RuntimeError("なんかバグった: {}".format(response.status_code))
        result = response.json()
        return result
