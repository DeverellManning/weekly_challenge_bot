import discord

class EntryView(discord.ui.View):
    """The public, persistent message."""
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open my panel", style=discord.ButtonStyle.primary, custom_id="entry:open")
    async def open_panel(self, button, interaction: discord.Interaction):
        # Look up per-user data here (DB, roles, etc.)
        text = f"Hi {interaction.user.display_name}! Your personal options:"
        await interaction.response.send_message(text, view=PanelView(interaction.user), ephemeral=True)

class PanelView(discord.ui.View):
    """The personalized, ephemeral part."""
    def __init__(self, user: discord.abc.User):
        super().__init__(timeout=180)
        self.user = user

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.primary)
    async def accept_challenge(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f"Done, {interaction.user.name}.", view=None)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger)
    async def reject_challenge(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f"Done, {interaction.user.name}.", view=None)