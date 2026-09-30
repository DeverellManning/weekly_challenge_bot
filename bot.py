from datetime import datetime, time
import os, json
from dotenv import load_dotenv

import discord
from discord.ext import tasks

from challenge_bot.guild_data import GuildData
from challenge_bot.challenge_bot_encoder import ChallengeBotEncoder

load_dotenv()

intents = discord.Intents.default()
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
    if ctx.guild_id is not None:
        json_str = json.dumps(guilds[ctx.guild_id].players, cls=ChallengeBotEncoder)
        print(json_str)
        print(json.loads(json_str))
        await ctx.respond(json_str, ephemeral=True)

@bot.application_command()
async def complete_quest(ctx : discord.ApplicationContext):
    pass

@bot.application_command()
async def abandon_quest(ctx : discord.ApplicationContext):
    pass

@bot.application_command(guild_only=True)
async def quest_status(ctx : discord.ApplicationContext):
    if ctx.guild_id is not None:
        await ctx.respond(guilds[ctx.guild_id].report_status(), ephemeral=True)
            





bot.run(os.getenv('TOKEN')) # run the bot with the token