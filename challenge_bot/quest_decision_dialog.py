import discord

from challenge_bot.player_data import PlayerData

class EntryView(discord.ui.View):
    """The public, persistent message."""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Reveal your Quest", style=discord.ButtonStyle.green, custom_id="entry:open")
    async def open_panel(self, button, interaction: discord.Interaction):
        # Look up per-user data here (DB, roles, etc.)
        text = f"Hi {interaction.user.display_name}! Your personal options:"
        await interaction.response.send_message(text, view=PanelView(interaction.user), ephemeral=True)


class RevealQuestView(discord.ui.View):
    """The public, persistent message."""
    def __init__(self, players : list[PlayerData]):
        super().__init__(timeout=None)

        self.players = players

    @discord.ui.button(label="Reveal your Quest", style=discord.ButtonStyle.green, custom_id="entry:open")
    async def open_panel(self, button, interaction: discord.Interaction):
        player = self.players[interaction.user.id]
        if not player.has_quest():
            await player.display_quest(interaction)
        else:
            await interaction.respond("-# *You have already received a quest!*", ephemeral=True)
        

        
class PanelView(discord.ui.View):
    """The personalized, ephemeral part."""
    def __init__(self, user: discord.abc.User):
        super().__init__(timeout=180)
        self.user = user

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.primary)
    async def accept_challenge(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f"Done, {self.user.name}.", view=None)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger)
    async def reject_challenge(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f"Done, {self.user.name}.", view=None)