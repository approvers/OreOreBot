from lib.util import Singleton
import discord

class Typo(Singleton):
    def __init__(self, members):
        self.typo_dict = {}
        for member in members:
            self.typo_dict[member.id] = []

    def append(self, member_id, message):
        if not member_id in self.typo_dict.keys():
            self.typo_dict[member_id] = []

        if message.replace(" ", "") == "":
            return

        self.typo_dict[member_id].append(message[:-3])

    def call(self, member_id, member_name):
        if not member_id in self.typo_dict.keys():
            self.typo_dict[member_id] = []

        user_typo = self.typo_dict[member_id]
        
        send_message = "今日の{}typo\n".format(member_name)

        display_typo = ""

        for typo in user_typo:
            display_name += "・{}\n".format(typo)
        return send_message + display_typo

