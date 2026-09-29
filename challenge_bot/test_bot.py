#from asyncio import tasks
from discord.ext import tasks
import discord
from datetime import datetime, time
import os # default module
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file
bot = discord.Bot()
guild = None

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

    for g in bot.guilds:
        print(g.name)

    guild = bot.guilds[0]

    status_channel = guild.get_channel(1455729620275167345)
    print(type(status_channel))
    if isinstance(status_channel, discord.TextChannel): 
        print("started status message!")
        test.start(status_channel)
    
    await bot.sync_commands()

@bot.slash_command()
async def sync(ctx: discord.ApplicationContext):
    guild = ctx.guild
    if guild is None: return

    await bot.sync_commands(guild_ids=[guild.id])
    print("Commands Synced!")

@bot.slash_command(name="load", description="Load user info")
async def joie(ctx: discord.ApplicationContext):
    members = ctx.guild.members
    names = [m.name for m in members]
    print(names)
    await ctx.respond(str(names))


@tasks.loop(seconds=5)
async def test(channel : discord.TextChannel):
    await channel.send(content="annoy")
    print("annoy")



bot.run(os.getenv('TOKEN')) # run the bot with the token