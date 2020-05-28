from typing import Union, List
import discord
import requests
from src.on_message.commands.git_utils.base import Base, Response


class Issue(Base):
    async def execute(
        self,
        orgs: str,
        repos: str,
        send_message_channel: discord.TextChannel,
        target: Union[str, int, None]
    ):
        issues: List[Response] = self._get(orgs, repos)
        if target is None:
            self.showAll(issues, send_message_channel)
            return

        if isinstance(target, str):
            self.searchIssue(
                issues,
                send_message_channel,
                target
            )
            return

        if isinstance(target, int):
            self.getIssue(
                issues,
                send_message_channel,
                target
            )

    async def showAll(
            self,
            issues: List[Response],
            send_message_channel: discord.TextChannel
    ):
        for issue in issues:
            message = \
                "```\ntitle: {}\nurl: {}```"\
                .format(issue["title"], issue["url"])
            await send_message_channel.send(message)

    async def searchIssue(
            self,
            issues: List[Response],
            send_message_channel: discord.TextChannel,
            keyword: str
    ):
        found_issues = [issue for issue in issues if keyword in issue["name"]]
        if len(found_issues) == 0:
            await send_message_channel.send("repository not found")
            return

        for issue in found_issues:
            message = \
                "```\nname: {}\nurl: {}```"\
                .format(issue["name"], issue["url"])

            await send_message_channel.send(message)

    async def getIssue(
        self,
        issues: List[Response],
        send_message_channel: discord.TextChannel,
        number: int
    ):
        for issue in issues:
            issue_id = issue["id"]
            if issue_id == number:
                message = \
                    "```\ntitle: {}\nurl: {}```"\
                    .format(issue["title"], issue["url"])
                await send_message_channel.send(message)
                return

        await send_message_channel.send(
            "issue request not found with given number"
        )

    def _get(self, orgs: str, repos: str) -> List[Response]:
        url_template = "/repos/{}/{}/issues".format(orgs, repos)
        response = requests.get(
            Issue.GITHUB_API_URL + url_template,
            auth=self.auth
        )
        result = response.json()
        return result
