from datetime import datetime, time
import os, json
from dotenv import load_dotenv

import discord
from discord.ext import tasks

import challenge_bot.config as configurer
from challenge_bot.guild_data import GuildData
from challenge_bot.challenge_bot_encoder import ChallengeBotEncoder

load_dotenv()
config = configurer.load("./config.toml")

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

guilds : dict[int, GuildData] = {}

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

    # Look through guilds the bot's a member of.
    for g in bot.guilds:
        print(g.name)
        guild_conf = config.get(str(g.id))
        if guild_conf == None:
            # As the guild is not configured, do not load it.
            # Just add it to the file to be configured.
            configurer.add_guild(g.id, g.name)
            print(f"Guild {g.name} has been added to config.  Please enter values in config.toml and restart!")
            #guilds[g.id] = GuildData(bot, g.id, role_id=1554254770083069973, channel_id=1455729620275167345)
        else:
            guilds[g.id] = GuildData(bot, g.id, role_id=int(guild_conf["role_id"]), 
                                     channel_id=int(guild_conf["channel_id"]))
        

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
        player = guild.player_by_id(ctx.author.id)
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

@bot.slash_command()
async def join(ctx : discord.ApplicationContext):
    if isinstance(ctx.author, discord.Member):
        guild_data = guilds[ctx.author.guild.id]
        if guild_data is not None:
            await ctx.author.add_roles(guild_data.challenge_role)

@bot.slash_command()
async def leave(ctx : discord.ApplicationContext):
    if isinstance(ctx.author, discord.Member):
        guild_data = guilds[ctx.author.guild.id]
        if guild_data is not None:
            await ctx.author.remove_roles(guild_data.challenge_role)



bot.run(os.getenv('TOKEN')) # run the bot with the token