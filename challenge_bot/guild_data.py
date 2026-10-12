import random
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

    def on_ready(self) -> None:
        self.guild = self.bot.get_guild(self.guild_id)
        assert(self.guild is not None)
        self.guild_name = self.guild.name

        role = self.guild.get_role(self.role_id)
        if role is None:
            raise RuntimeError(f"Role not found: (ID {self.role_id}) ")
        self.challenge_role = role

        channel = self.guild.get_channel(self.channel_id)
        if not type(channel) == discord.TextChannel:
            raise RuntimeError(f"Channel not found, or is not a TextChannel: (ID {self.channel_id}) ")
        self.status_channel = channel

        # Add all members that have challenge role:
        registered_memebers = self.challenge_role.members
        for m in registered_memebers:
            self.add_player(m)

        self.looped_status.change_interval(time=self.round_start_time)
        self.looped_status.start()

    def is_ready(self):
        assert isinstance(self.challenge_role, discord.Role)
        assert isinstance(self.status_channel, discord.TextChannel)
        

    def player_by_id(self, id : int) -> PlayerData | None:
        return self.players.get(id)

    def add_player(self, m : discord.Member):
        if not self.challenge_role in m.roles:
            print(f"Can not add member as player, {m.name} does not have needed role.")

        # Check if player data exists from last save:
        if False:
            pass
        # Create player from scratch.
        else:
            self.players[m.id] = PlayerData(m)
        print(f"{m.name} added to system!")
    
    def add_quest(self, q : Quest):
        self.quest_pool.append(q)

    def report_status(self):
        players_list = "\n- ".join([p.get_public_status() for p in self.players.values()])
        status_counts, total_players = self.calc_stats()
        text = f"""Server Name: {self.guild_name} *({self.guild_id})*
Players: ({total_players} total)
- {players_list}
---
There are {len(self.quest_pool)} unassigned quests remaining.
Quests announed at {self.round_start_time}, Day {self.round_start_day}
Round ends at {self.round_end_time}, Day {self.round_end_day}
---
{"\n,".join([str(v) + " " + str(k) for k, v in status_counts.items()])}
"""

        return text
    
    def assign_quests(self):
        for player in self.players.values():
            if len(self.quest_pool) <= 0:
                print("There are no quests left in the pool!")
                continue
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
        if not isinstance(interaction.user, discord.member.Member): 
            return
        if not self.challenge_role in interaction.user.roles:
            await interaction.respond("You are not a participant in server quests.  Please use `/join` to opt-in to quests.", ephemeral=True)
            return
        try:
            player = self.players[interaction.user.id]
        except IndexError:
            print(f"{interaction.user.id} is not a valid player!")
            return
        
        if not player.has_accepted_quest():
            print(f"Offering quest to {player.name}...")
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


    # Demo / Testing
    def create_test_quests(self):
        self.quest_pool.extend([
            Quest("Build a Chicken", QuestType.BUILD, 10),
            Quest("Kill Deverell", QuestType.MURDER, 25),
            Quest("Steal Mark's Cheese.", QuestType.COLLECT, 100),
            Quest("Trap every player.", QuestType.SABOTAGE, 1000, QuestDifficulty.HARD)
        ])

    def calc_stats(self):
        total = len(self.players)
        statuses = [p.active_quest.status for p in self.players.values()]

        counted = Counter(statuses)
        return counted, total

    # Looped Tasks
    @discord.ext.tasks.loop()
    async def looped_status(self):
        await self.status_channel.send(self.report_status())

    @discord.ext.tasks.loop()
    async def challenge_start(self):
        pass