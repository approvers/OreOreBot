from typing import Union, List
import discord
import requests
from src.on_message.commands.git_utils.base import Base, Response


class Pull(Base):
    async def execute(
        self,
        orgs: str,
        repos: str,
        send_message_channel: discord.TextChannel,
        target: Union[str, int, None]
    ):
        pulls: List[Response] = self._get(orgs, repos)
        if target is None:
            self.showAll(pulls, send_message_channel)
            return

        if isinstance(target, str):
            self.searchPull(
                pulls,
                send_message_channel,
                target
            )
            return

        if isinstance(target, int):
            self.getPull(
                pulls,
                send_message_channel,
                target
            )
            return

    async def showAll(
            self,
            pulls: List[Response],
            send_message_channel: discord.TextChannel
    ):
        for pull in pulls:
            message = \
                "```\ntitle: {}\nurl: {}```"\
                .format(pull["title"], pull["url"])
            await send_message_channel.send(message)

    async def searchPull(
            self,
            pulls: List[Response],
            send_message_channel: discord.TextChannel,
            keyword: str
    ):
        found_pulls = [pull for pull in pulls if keyword in pull["title"]]
        if len(found_pulls) == 0:
            await send_message_channel.send("repository not found")
            return

        for pull in found_pulls:
            message = \
                "```\ntitle: {}\nurl: {}```"\
                .format(pull["title"], pull["url"])

            await send_message_channel.send(message)

    async def getPull(
            self,
            pulls: List[Response],
            send_message_channel: discord.TextChannel,
            number: int
    ):
        for pull in pulls:
            pull_id = pull["id"]
            if pull_id == number:
                message = \
                    "```\ntitle: {}\nurl: {}```"\
                    .format(pull["title"], pull["url"])
                await send_message_channel.send(message)
                return

        await send_message_channel.send(
            "pull request not found with given number"
        )

    def _get(self, orgs: str, repos: str) -> List[Response]:
        url_template = "/repos/{}/{}/pulls".format(orgs, repos)
        response = requests.get(
            Pull.GITHUB_API_URL + url_template,
            auth=self.auth
        )
        if response.status_code == 200:
            raise RuntimeError("なんかばぐった:{}".format(response.status_code))
        result = response.json()
        return result
