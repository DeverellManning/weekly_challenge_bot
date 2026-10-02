import discord

from challenge_bot.quest import *
from challenge_bot.dialogs import QuestDecisionDialog


class PlayerData:
    def __init__(self, member : discord.Member) -> None:
        self.guild_id = member.guild.id
        self.id = member.id
        self.name = member.nick or member.name
        self.active_quest : Quest|None = None

    async def display_quest(self, interaction : discord.Interaction):
        text = f"This is your weekly quest, {self.name}:\n{self.get_quest_info()}"
        await interaction.response.send_message(text, ephemeral=True)
        
    async def offer_quest(self, interaction : discord.Interaction):
        assert(self.active_quest is not None)
        orig_text = f"""Hey {self.name}, here is your quest for this week:\n{self.get_quest_info()}"""
        view = QuestDecisionDialog(self.on_accept, self.on_decline)

        i2 = await interaction.respond(orig_text, view=view, ephemeral=True)
        await view.wait()
        match(self.active_quest.status):
            case QuestState.ACCEPTED:
                orig_text += "\n *Quest Accepted*"
            case QuestState.REJECTED:
                orig_text += "\n *Quest Declined*"

        await i2.edit(content=orig_text, view=None)

    def assign_quest(self, quest : Quest):
        self.active_quest = quest
        self.active_quest.assign()
        

    # Handlers
    async def on_accept(self, interaction : discord.Interaction):
        assert(self.has_quest())
        self.active_quest.accept()

    async def on_decline(self, interaction : discord.Interaction):
        assert(self.has_quest())
        self.active_quest.reject()


    def has_quest(self):
        if isinstance(self.active_quest, Quest):
            return True
        return False

    def has_accepted_quest(self):
        if not self.has_quest():
            return False
        if self.active_quest.status == QuestState.ACCEPTED:
            return True
        else:
            return False


    def public_status(self):
        if self.has_quest():
            return f"{self.name}: Quest is `{self.active_quest.status.name.lower()}`."
        else:
            return f"{self.name}: No Quest"

    def get_quest_info(self):
        if self.has_quest() is not None:
            return self.active_quest.display()
        else:
            return "*Right now, you don't have a quest.*"