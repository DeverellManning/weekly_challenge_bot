import json
import challenge_bot.quest as quest
from challenge_bot.player_data import PlayerData

class ChallengeBotEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, quest.Quest):
            return {"goal": o.goal, "status": o.status, "difficulty": o.difficulty}

        if isinstance(o, quest.QuestState):
            return o.value

        if isinstance(o, quest.QuestDifficulty):
            return o.value

        if isinstance(o, quest.QuestType):
            return o.value

        if isinstance(o, PlayerData):
            return {"member_id": o.id, "quest": o.active_quest}
        

        # Let the base class default method raise the TypeError
        return super().default(o)