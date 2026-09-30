import json
import challenge_bot.quest as quest

class ChallengeBotEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, quest.Quest):
            return {"goal": o.goal, "status": o.status, "difficulty": o.difficulty}

        if isinstance(o,quest.QuestState):
            return o.value

        if isinstance(o,quest.QuestDifficulty):
            return o.value

        if isinstance(o,quest.QuestType):
            return o.value
        

        # Let the base class default method raise the TypeError
        return super().default(o)