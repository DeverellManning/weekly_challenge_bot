import json
from enum import Enum, auto
from textwrap import wrap

from challenge_bot.challenge_bot_encoder import ChallengeBotEncoder

class QuestType(Enum):
    UNSET = 0
    MURDER = auto()
    PROTECT = auto()

    SABOTAGE = auto()
    BUILD = auto()

    STEAL = auto()
    COLLECT = auto()

class QuestState(Enum):
    UNASSIGNED = auto()
    PENDING_OFFER = auto()
    ACCEPTED = auto()
    REJECTED = auto()
    COMPLETED = auto()
    FAILED = auto()

class QuestDifficulty(Enum):
    EASY = 1,
    MODERATE = 2,
    HARD = 3



class Quest:
    def __init__(self, goal = "", type = QuestType.UNSET, points = 0, difficulty = QuestDifficulty.EASY, reward = "", penalty = ""):
        self.goal = goal
        self.type = type
        self.points = points
        self.reward = reward
        self.penalty = penalty

        self.status = QuestState.UNASSIGNED
        self.difficulty = difficulty

        self.evidence = []
    
    def to_json(self):
        return json.dumps(self, cls=ChallengeBotEncoder)

    def complete(self):
        if self.status == QuestState.ACCEPTED:
            self.status = QuestState.COMPLETED

    def fail(self):
        if self.status == QuestState.ACCEPTED:
            self.status = QuestState.FAILED

    def assign(self):
        if self.status == QuestState.UNASSIGNED:
            self.status = QuestState.PENDING_OFFER

    def accept(self):
        if self.status == QuestState.PENDING_OFFER:
            self.status = QuestState.ACCEPTED

    def reject(self):
        if self.status == QuestState.PENDING_OFFER:
            self.status = QuestState.REJECTED

    def display(self) -> str:
        return f"""## Quest Name
{"".join(wrap(self.goal, 32, initial_indent="  ", subsequent_indent="  "))}
> Points: {self.points} | Difficulty: {self.difficulty.name}
"""

    
        
