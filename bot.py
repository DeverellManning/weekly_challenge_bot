import os, json
from dotenv import load_dotenv

import discord

import challenge_bot.config as configurer
from challenge_bot.guild_data import GuildData
from challenge_bot.challenge_bot_encoder import ChallengeBotEncoder

# Load configuration, enviroment variables:
load_dotenv()
config_path = "./config.toml"
config = configurer.load(config_path)

# Attempt to load saved data
data = json.loads("""{
"guilds": []
}"""
)

# Intialize discord bot with needed attempts.
intents = discord.Intents.default()
intents.members = True
guilds : dict[int, GuildData] = {}
bot = discord.Bot(intents=intents)


# The big initiation of eveything (tm)
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

    #Load individual guild data instances
    for g in bot.guilds:
        print(g.name)

        # First, load guild configuration info
        guild_conf = config.get(str(g.id))
        if guild_conf == None:
            # As the guild is not configured, do not load it.
            # Just add it to the config file to be configured.
            configurer.add_guild(config_path, g.id, g.name)
            print(f"Guild {g.name} has been added to config.  Please enter values in {config_path} and restart!")
            #guilds[g.id] = GuildData(bot, g.id, role_id=1554254770083069973, channel_id=1455729620275167345)
        else:
            if not "disabled" in config.keys():
                print(f"Guild {g.name} loaded from config.")
                guilds[g.id] = GuildData(bot, g.id, role_id=int(guild_conf["role_id"]), 
                                        channel_id=int(guild_conf["channel_id"]))

        # Second, we need to restore saved data from the json file.
        #if data["guilds"]:
        #    saved_guild_data = data["guilds"][g.id]
        #    if saved_guild_data is not None:
        #        # We need to give Guild Data access to this information somehow.
        #        pass

    # Set up and start each guild
    for g in guilds.values():
        g.on_ready()
        g.create_test_quests()
        g.assign_quests()
        await g.announce_quests()

    # Make sure commands are synced
    await bot.sync_commands()
    print("Commands Synced.")


# Command Checks
# (Not fully sure how these are used?)
def user_is_player(ctx : discord.ApplicationContext):
    if isinstance(ctx.author, discord.Member):
        guild_data = guilds[ctx.author.guild.id]
        if guild_data is not None:
            return True
    return False

def user_has_accepted_quest(ctx : discord.ApplicationContext):
    if isinstance(ctx.author, discord.Member):
        guild_data = guilds[ctx.author.guild.id]
        if guild_data is not None:
            player = guild_data.player_by_id(ctx.author.id)
            if player:
                return player.has_accepted_quest()
    return False


###
### Bot Commands
###

### Player Commands
@bot.slash_command(checks=[user_is_player])
async def my_quest(ctx : discord.ApplicationContext):
    if ctx.guild_id is not None:
        guild = guilds[ctx.guild_id]
        player = guild.player_by_id(ctx.author.id)
        if player:
            await player.display_quest(ctx.interaction)

@bot.slash_command(checks=[user_is_player, user_has_accepted_quest])
async def complete_quest(ctx : discord.ApplicationContext):
    pass

@bot.slash_command(checks=[user_is_player, user_has_accepted_quest])
async def abandon_quest(ctx : discord.ApplicationContext):
    pass

@bot.slash_command(guild_only=True)
async def join(ctx : discord.ApplicationContext):
    if isinstance(ctx.author, discord.Member):
        guild_data = guilds[ctx.author.guild.id]
        await ctx.author.add_roles(guild_data.challenge_role)
        guild_data.add_player(ctx.author)

@bot.slash_command(guild_only=True)
async def leave(ctx : discord.ApplicationContext):
    if isinstance(ctx.author, discord.Member):
        guild_data = guilds[ctx.author.guild.id]
        await ctx.author.remove_roles(guild_data.challenge_role)


# Admin Commands
@bot.slash_command(checks=[])
async def quest_status(ctx : discord.ApplicationContext):
    if ctx.guild_id is not None:
        await ctx.respond(guilds[ctx.guild_id].report_status(), ephemeral=True)

# Utility Commands
@bot.slash_command(guild_only=True)
async def dump_json(ctx : discord.ApplicationContext):
    if ctx.guild_id is not None:
        json_str = json.dumps(guilds, cls=ChallengeBotEncoder, sort_keys=True, indent=4)
        print(json_str)
        print(json.loads(json_str))
        await ctx.respond("```\n" + json_str + "\n```", ephemeral=True)


# Actually run the bot, with the towoken
bot.run(os.getenv('TOKEN'))