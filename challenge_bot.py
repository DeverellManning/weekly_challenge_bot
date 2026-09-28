from datetime import datetime, time
import os
from dotenv import load_dotenv

import discord
from discord.ext import tasks

from quest_decision_dialog import EntryView
from guild_data import GuildData

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

        status_channel = g.guild.get_channel(1455729620275167345)
        assert(type(status_channel == discord.TextChannel))

        await status_channel.send("Click below to see your personal panel.", view=EntryView())
        bot.add_view(EntryView())

    
    
    
    
    await bot.sync_commands()
    print("Commands Synced.")

@bot.application_command()
async def my_quest(ctx : discord.ApplicationContext):
    if ctx.guild_id is not None:
        guild = guilds[ctx.guild_id]
        player = guild.players[ctx.author.id]
        if player:
            await ctx.respond(f"{player.name}, your active quest is: \n\"{player.get_active_quest_info()}\"")
            





bot.run(os.getenv('TOKEN')) # run the bot with the token