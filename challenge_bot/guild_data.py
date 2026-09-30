import random
import tomllib
import discord

from challenge_bot.player_data import PlayerData
from challenge_bot.quest import Quest, QuestDifficulty, QuestState, QuestType
from challenge_bot.reveal_quest_view import RevealQuestView

class GuildData:
    def __init__(self, bot : discord.Bot, guild_id : int, role_id : int, channel_id : int) -> None:
        self.bot = bot

        self.guild_id = guild_id
        self.role_id = role_id
        self.channel_id = channel_id

        self.players : dict[int, PlayerData]= {}
        self.quest_pool : list[Quest] = []

    def on_ready(self):
        self.guild = self.bot.get_guild(self.guild_id)
        assert(self.guild is not None)
        self.guild_name = self.guild.name

        self.challenge_role = self.guild.get_role(self.role_id)
        assert(self.challenge_role is not None)

        self.status_channel = self.guild.get_channel(self.channel_id)
        assert(self.status_channel is not None)

        registered_memebers = self.challenge_role.members
        for m in registered_memebers:
            self.players[m.id] = PlayerData(m)
            print(f"{m.name} added to system!")

    def add_quest(self, q : Quest):
        self.quest_pool.append(q)

    def report_status(self):
        text = f"""Server Name: {self.guild_name} *({self.guild_id})*
Players:{"\n".join(t.get_quest_info() for t in self.players.values())}
---
{len(self.quest_pool)} quests available."""
    
    def assign_quests(self):
        for player in self.players.values():
            quest = random.choice(self.quest_pool)
            player.assign_quest(quest)
            self.quest_pool.remove(quest)

        print(f"There are {len(self.quest_pool)} quests left in the pool.")

    async def announce_quests(self):
        self.rqv = RevealQuestView(players=self.players)
        self.rqv.orig_mesg = "Hey everybody!  Quests have been assigned!"
        self.msg = await self.status_channel.send(self.rqv.orig_mesg, view=self.rqv)
        self.bot.add_view(self.rqv)

        print(f"Quests announced in {self.guild_name}.")

    def create_test_quests(self):
        self.quest_pool.extend([
            Quest("Build a Chicken", QuestType.BUILD, 10),
            Quest("Kill Deverell", QuestType.MURDER, 25),
            Quest("Steal Mark's Cheese.", QuestType.COLLECT, 100),
            Quest("Trap every player.", QuestType.SABOTAGE, 1000, QuestDifficulty.HARD)
        ])



    
                