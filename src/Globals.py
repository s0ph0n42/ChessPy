from enum import Enum

class PieceColor(Enum):
    WHITE = 0
    BLACK = 1

class GameMode(Enum):
    CPUONLY = 0
    HUMANCPU = 1
    HUMANONLY = 2
