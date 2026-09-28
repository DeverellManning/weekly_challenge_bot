import random

import discord
from discord import Guild

from player_data import PlayerData
from quest import Quest, QuestType

class GuildData:
    def __init__(self, guild : Guild) -> None:
        self.id = guild.id
        self.guild = guild

        self.challenge_role = guild.get_role(1554254770083069973)
        assert(self.challenge_role is not None)

        self.players : dict[int, PlayerData]= {}
        registered_memebers = self.challenge_role.members
        for m in registered_memebers:
            self.players[m.id] = PlayerData(m)
            print(f"{m.name} added to system!")

        self.quest_pool : list[Quest] = []

    def create_test_quests(self):
        self.quest_pool.extend([
            Quest("Build a Chicken", QuestType.BUILD, 10),
            Quest("Kill Deverell", QuestType.MURDER, 25),
            Quest("Steal Mark's Cheese.", QuestType.COLLECT, 100)
        ])

    def assign_quests(self):
        for p in self.players.values():
            quest = random.choice(self.quest_pool)
            p.active_quest = quest
            self.quest_pool.remove(quest)

        print(f"There are {len(self.quest_pool)} quests left in the pool.")
                