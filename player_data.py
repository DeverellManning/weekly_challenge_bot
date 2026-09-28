import discord

from quest import *

class PlayerData:
    def __init__(self, member : discord.Member) -> None:
        self.guild_id = member.guild.id
        self.id = member.id
        self.name = member.nick or member.name

        self.registered = True

        self.active_quest : Quest|None = None

    def get_active_quest_info(self):
        if self.active_quest is not None:
            return f"{self.active_quest.goal}"
        else:
            return ""
