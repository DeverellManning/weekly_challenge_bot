import discord

class RevealQuestDialog(discord.ui.View):
    """The persistent, public dialog through which a player can reveal their quest."""
    def __init__(self, on_respond_callback):
        super().__init__(timeout=None)
        self.on_respond = on_respond_callback

    @discord.ui.button(label="Reveal your Quest", style=discord.ButtonStyle.green, custom_id="entry:open")
    async def open_panel(self, button, interaction: discord.Interaction):
        if not interaction.user: return

        await self.on_respond(interaction)


class QuestDecisionDialog(discord.ui.View):
    """The personalized, ephemeral part."""
    def __init__(self, accept_callback, decline_callback):
        super().__init__(timeout=180)
        self.on_accept = accept_callback
        self.on_decline = decline_callback

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.primary)
    async def accept_challenge(self, button, interaction: discord.Interaction):
        await self.on_accept(interaction)
        self.stop()
        

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline_challenge(self, button, interaction: discord.Interaction):
        await self.on_decline()
        self.stop()