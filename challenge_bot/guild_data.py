import random
import tomllib
import discord, discord.ext.tasks
import datetime

from challenge_bot.player_data import PlayerData
from challenge_bot.quest import Quest, QuestDifficulty, QuestState, QuestType
from challenge_bot.dialogs import RevealQuestDialog

class GuildData:
    def __init__(self, bot : discord.Bot, 
                 guild_id : int, role_id : int, channel_id : int, 
                 round_start_time = datetime.time(19, 0),
                 round_start_day = 7,
                 round_end_time = datetime.time(16, 0),
                 round_end_day = 6) -> None:
        self.bot = bot

        self.guild_id = guild_id
        self.role_id = role_id
        self.channel_id = channel_id

        self.round_start_time = round_start_time
        self.round_end_time = round_end_time

        self.round_start_day = round_start_day
        self.round_end_day = round_end_day

        self.players : dict[int, PlayerData]= {}
        self.quest_pool : list[Quest] = []

    def on_ready(self):
        self.guild = self.bot.get_guild(self.guild_id)
        assert(self.guild is not None)
        self.guild_name = self.guild.name

        self.challenge_role = self.guild.get_role(self.role_id)
        assert(self.challenge_role is not None)

        channel = self.guild.get_channel(self.channel_id)
        assert(channel is not None)
        assert(isinstance(channel, discord.TextChannel))
        self.status_channel = channel

        registered_memebers = self.challenge_role.members
        for m in registered_memebers:
            self.players[m.id] = PlayerData(m)
            print(f"{m.name} added to system!")

        self.looped_status.change_interval(time=self.round_start_time)
        self.looped_status.start()

    def player_by_id(self, id : int) -> PlayerData | None:
        return self.players.get(id)
    
    def add_quest(self, q : Quest):
        self.quest_pool.append(q)

    def report_status(self):
        players_list = "\n- ".join([p.public_status() for p in self.players.values()])
        text = f"""Server Name: {self.guild_name} *({self.guild_id})*
Players:
- {players_list}
---
There are {len(self.quest_pool)} quests remaining.
{self.round_start_time}
{self.round_end_time}"""
        return text
    
    def assign_quests(self):
        for player in self.players.values():
            quest = random.choice(self.quest_pool)
            player.assign_quest(quest)
            self.quest_pool.remove(quest)
        
        print(f"There are {len(self.quest_pool)} quests left in the pool.")

    async def announce_quests(self):
        self.rqv = RevealQuestDialog(on_respond_callback=self.handle_reveal)
        self.msg = await self.status_channel.send("Hey everybody!  Quests have been assigned!", view=self.rqv)
        self.bot.add_view(self.rqv)

        print(f"Quests announced in {self.guild_name}.")

    async def handle_reveal(self, interaction : discord.Interaction):
        if interaction.user is None: return
        try:
            player = self.players[interaction.user.id]
        except IndexError:
            print(f"{interaction.user.id} is not a valid player!")
            return
        
        if not player.has_accepted_quest():
            await player.offer_quest(interaction)

            n_accept = 0
            n_reject = 0
            total = len(self.players)
            for p in self.players.values():
                if p.active_quest:
                    if p.active_quest == QuestState.ACCEPTED:
                        n_accept += 1
                    elif p.active_quest == QuestState.REJECTED:
                        n_reject += 1
                    
            text = self.msg.content + f"\n-# Out of {total} players, {n_accept} have accepted and {n_reject} have declined their quest."
            await self.msg.edit(content=text, view=self.rqv)
        else:
            await interaction.respond("-# *You have already accepted a quest!*", ephemeral=True, delete_after=6)

    def create_test_quests(self):
        self.quest_pool.extend([
            Quest("Build a Chicken", QuestType.BUILD, 10),
            Quest("Kill Deverell", QuestType.MURDER, 25),
            Quest("Steal Mark's Cheese.", QuestType.COLLECT, 100),
            Quest("Trap every player.", QuestType.SABOTAGE, 1000, QuestDifficulty.HARD)
        ])

    @discord.ext.tasks.loop()
    async def looped_status(self):
        await self.status_channel.send(self.report_status())