from datetime import datetime, time
import os
from dotenv import load_dotenv

import discord
from discord.ext import tasks

from challenge_bot.quest_decision_dialog import EntryView
from challenge_bot.guild_data import GuildData

load_dotenv() # load all the variables from the env file

intents = discord.Intents.default()  # Allow the use of custom intents
intents.members = True

bot = discord.Bot(intents=intents)

guilds : dict[int, GuildData] = {}

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

    for g in bot.guilds:
        print(g.name)
        guilds[g.id] = GuildData(g)

        

    for g in guilds.values():
        print(g.id)
        g.create_test_quests()
        g.assign_quests()
        await g.announce_quests(bot)

    
    
    
    
    await bot.sync_commands()
    print("Commands Synced.")

@bot.application_command()
async def my_quest(ctx : discord.ApplicationContext):
    if ctx.guild_id is not None:
        guild = guilds[ctx.guild_id]
        player = guild.players[ctx.author.id]
        if player:
            await player.display_quest(ctx.interaction)
            





bot.run(os.getenv('TOKEN')) # run the bot with the token