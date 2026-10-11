import json
import challenge_bot.quest as quest
from challenge_bot.player_data import PlayerData
from challenge_bot.guild_data import GuildData

class ChallengeBotEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, quest.Quest):
            return {"__Quest__": True, "goal": o.goal, "points": o.points, "status": o.status, "difficulty": o.difficulty}

        if isinstance(o, quest.QuestState):
            return o.value

        if isinstance(o, quest.QuestDifficulty):
            return o.value

        if isinstance(o, quest.QuestType):
            return o.value

        if isinstance(o, PlayerData):
            return {"member_id": o.id, "quest": o.active_quest}

        if isinstance(o, GuildData):
            return {
                "guild_id": o.guild_id,
                "players": o.players,
                "quest_pool": o.quest_pool
            }
        

        # Let the base class default method raise the TypeError
        return super().default(o)