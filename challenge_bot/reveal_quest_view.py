import discord

from challenge_bot.player_data import PlayerData
from challenge_bot.quest import QuestState


class RevealQuestView(discord.ui.View):
    """The public, persistent message."""
    def __init__(self, players : dict[int, PlayerData]):
        super().__init__(timeout=None)

        self.players = players
        self.orig_mesg = ""

    @discord.ui.button(label="Reveal your Quest", style=discord.ButtonStyle.green, custom_id="entry:open")
    async def open_panel(self, button, interaction: discord.Interaction):
        if not interaction.user: return
        try:
            player = self.players[interaction.user.id]
        except IndexError:
            print(f"{interaction.user.id} is not a valid player!")
            return
        
        if not player.has_accepted_quest():
            await player.offer_quest(interaction)

            n_accept = 0
            total = len(self.players)
            for p in self.players.values():
                if p.has_accepted_quest() == QuestState.ACCEPTED:
                    n_accept += 1
            
            text = self.orig_mesg + f"\n*{n_accept} out of {total} players have accepted.*"
            await self.message.edit(content=text, view=self)
        else:
            await interaction.respond("-# *You have already accepted a quest!*", ephemeral=True)