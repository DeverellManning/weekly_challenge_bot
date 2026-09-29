from enum import Enum, auto

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
    IN_PROGRESS = auto()
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

    def complete(self):
        self.status = QuestState.COMPLETED

    
        
