from enum import Enum, auto

class QuestType(Enum):
    UNSET = 0
    MURDER = auto()

    BUILD = auto()
    COLLECT = auto()

class QuestState(Enum):
    UNASSIGNED = auto()
    IN_PROGRESS = auto()
    REJECTED = auto()
    COMPLETED = auto()
    FAILED = auto()



class Quest:
    def __init__(self, goal = "", type = QuestType.UNSET, points = 0, reward = "", penalty = ""):
        self.goal = goal
        self.type = type
        self.points = points
        self.reward = reward
        self.penalty = penalty

        self.status = QuestState.UNASSIGNED

    def complete(self):
        self.status = QuestState.COMPLETED

    
        
