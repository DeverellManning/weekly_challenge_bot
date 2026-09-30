import discord

from challenge_bot.quest import *


class PlayerData:
    def __init__(self, member : discord.Member) -> None:
        self.guild_id = member.guild.id
        self.id = member.id
        self.name = member.nick or member.name

        self.registered = True

        self.active_quest : Quest|None = None

    def get_quest_info(self):
        if self.active_quest is not None:
            return self.active_quest.display()
        else:
            return "*Right now, you don't have a quest.*"

    async def display_quest(self, interaction : discord.Interaction):
        text = f"This is your weekly quest, {self.name}:\n{self.get_quest_info()}"

        await interaction.response.send_message(text, ephemeral=True)

    def assign_quest(self, quest : Quest):
        self.active_quest = quest
        self.active_quest.assign()
        
    async def offer_quest(self, interaction : discord.Interaction):
        text = f"""Hey {self.name}, here is your quest for this week:\n{self.get_quest_info()}"""
        view = QuestDecisionView(self)
        await interaction.response.send_message(text, view=view, ephemeral=True)
        await view.wait()

    def has_quest(self):
        return False

    def has_accepted_quest(self):
        if not self.active_quest:
            return False
        if self.active_quest.status == QuestState.ACCEPTED:
            return True
        else:
            return False
    




class QuestDecisionView(discord.ui.View):
    """The personalized, ephemeral part."""
    def __init__(self, player: PlayerData):
        super().__init__(timeout=180)
        if not player:
            raise(ValueError("Player information was not provided to the Quest Decision View."))
        else:
            self.player = player

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.primary)
    async def accept_challenge(self, button, interaction: discord.Interaction):
        orig_text = interaction.message.content
        orig_text += "\n *Quest Accepted*"
        await interaction.response.edit_message(content=orig_text, view=None)
        await interaction.channel.send(f"{self.player.name} has accepted their quest.")
        self.player.active_quest.accept()
        self.stop()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def reject_challenge(self, button, interaction: discord.Interaction):
        orig_text = interaction.message.content
        orig_text += "\n *Quest Declined*"
        await interaction.response.edit_message(content=orig_text, view=None)
        await interaction.channel.send(f"{self.player.name} has declined their quest.")
        self.player.active_quest.reject()
        self.stop()