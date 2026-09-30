from datetime import datetime, time
import os
from dotenv import load_dotenv

import discord
from discord.ext import tasks

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
        guilds[g.id] = GuildData(bot, g.id, role_id=1554254770083069973, channel_id=1455729620275167345)

    for g in guilds.values():
        g.on_ready()
        g.create_test_quests()
        g.assign_quests()
        await g.announce_quests()

    
    await bot.sync_commands()
    print("Commands Synced.")

@bot.application_command()
async def my_quest(ctx : discord.ApplicationContext):
    if ctx.guild_id is not None:
        guild = guilds[ctx.guild_id]
        player = guild.players[ctx.author.id]
        if player:
            await player.display_quest(ctx.interaction)

@bot.application_command()
async def dump_json(ctx : discord.ApplicationContext):
    await ctx.respond("\n".join([q.to_json() for q in guilds[ctx.guild.id].quest_pool]))

@bot.application_command()
async def complete_quest(ctx : discord.ApplicationContext):
    pass

@bot.application_command()
async def abandon_quest(ctx : discord.ApplicationContext):
    pass

@bot.application_command()
async def quest_status(ctx : discord.ApplicationContext):
    await ctx.respond(guilds[ctx.guild.id].report_status())
            





bot.run(os.getenv('TOKEN')) # run the bot with the token