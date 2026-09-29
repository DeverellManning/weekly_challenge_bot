import random

import discord
from discord import Guild

from challenge_bot.player_data import PlayerData
from challenge_bot.quest import Quest, QuestDifficulty, QuestType
from challenge_bot.quest_decision_dialog import RevealQuestView

class GuildData:
    def __init__(self, guild : Guild) -> None:
        self.id = guild.id
        self.guild = guild

        self.challenge_role = guild.get_role(1554254770083069973)
        assert(self.challenge_role is not None)

        self.status_channel = guild.get_channel(1455729620275167345)
        assert(self.status_channel is not None)

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
            Quest("Steal Mark's Cheese.", QuestType.COLLECT, 100),
            Quest("Trap every player.", QuestType.SABOTAGE, 1000, QuestDifficulty.HARD)
        ])

    def assign_quests(self):
        for p in self.players.values():
            quest = random.choice(self.quest_pool)
            p.active_quest = quest
            self.quest_pool.remove(quest)

        print(f"There are {len(self.quest_pool)} quests left in the pool.")

    async def announce_quests(self, bot : discord.Bot):
        rqv = RevealQuestView(players=self.players)
        await self.status_channel.send("Hey everybody!  Quests have been assigned!", view=rqv)
        bot.add_view(rqv)


    
                