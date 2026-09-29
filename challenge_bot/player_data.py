import discord

from challenge_bot.quest import *

class AcceptView(discord.ui.View):
    """The personalized, ephemeral part."""
    def __init__(self, user: discord.abc.User):
        super().__init__(timeout=180)
        self.user = user

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.primary)
    async def accept_challenge(self, button, interaction: discord.Interaction):
        orig_text = interaction.message.content
        orig_text += "\n *Quest Accepted*"
        await interaction.response.edit_message(content=orig_text, view=None)
        await interaction.channel.send(f"{self.user.name} has accepted their quest.")

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.danger)
    async def reject_challenge(self, button, interaction: discord.Interaction):
        orig_text = interaction.message.content
        orig_text += "\n *Quest Rejected*"
        await interaction.response.edit_message(content=orig_text, view=None)
        await interaction.channel.send(f"{self.user.name} has rejected their quest.")


class PlayerData:
    def __init__(self, member : discord.Member) -> None:
        self.guild_id = member.guild.id
        self.id = member.id
        self.name = member.nick or member.name

        self.registered = True

        self.active_quest : Quest|None = None

    def get_active_quest_info(self):
        if self.active_quest is not None:
            return f"{self.active_quest.goal}"
        else:
            return ""

    async def display_quest(self, interaction : discord.Interaction):
        text = f"""
        {self.name}, this is your quest:
        > {self.get_active_quest_info()}
        """
        await interaction.response.send_message(text, view=AcceptView(interaction.user), ephemeral=True)

    def has_quest(self):
        return True
