#from asyncio import tasks
from discord.ext import tasks
import discord
from datetime import datetime, time
import os # default module
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file

class PanelView(discord.ui.View):
    """The personalized, ephemeral part."""
    def __init__(self, user: discord.abc.User):
        super().__init__(timeout=180)
        self.user = user

    @discord.ui.button(label="Do thing", style=discord.ButtonStyle.primary)
    async def do_thing(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f"Done, {interaction.user.name}.", view=None)

class EntryView(discord.ui.View):
    """The public, persistent message."""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open my panel", style=discord.ButtonStyle.primary, custom_id="entry:open")
    async def open_panel(self, button, interaction: discord.Interaction):
        # Look up per-user data here (DB, roles, etc.)
        text = f"Hi {interaction.user.display_name}! Your personal options:"
        await interaction.response.send_message(text, view=PanelView(interaction.user), ephemeral=True)

bot = discord.Bot()
#bot.__setattr__("views_added", False)

@bot.event
async def on_ready():
    guild = bot.guilds[0]
    
    status_channel : discord.TextChannel = guild.get_channel(1455729620275167345)
    await status_channel.send("Click below to see your personal panel.", view=EntryView())
    
    bot.add_view(EntryView())
    
    #if not getattr(bot, "views_added", False):
    #    bot.add_view(EntryView())   # re-attach persistent view after restarts
    #    bot.__setattr__("views_added", True)

#@bot.slash_command()
#async def post_entry(ctx: discord.ApplicationContext):
#    await ctx.respond("Click below to see your personal panel.", view=EntryView())


bot.run(os.getenv('TOKEN')) # run the bot with the token