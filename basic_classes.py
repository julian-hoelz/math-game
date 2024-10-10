from dataclasses import dataclass
from enum import Enum
from typing import Callable


class Color:

    WHITE = (240, 240, 240)
    DARK_GRAY = (18, 18, 18)
    GRAY = (101, 101, 101)
    LIGHT_GRAY = (158, 158, 158)
    RED = (169, 50, 38)
    GREEN = (55, 106, 69)
    BLUE = (46, 58, 140)
    YELLOW = (184, 134, 11)
    ORANGE = (195, 84, 18)
    PURPLE = (91, 44, 111)
    TURQUOISE = (40, 125, 125)
    SPRING_GREEN = (0, 255, 127)
    BRIGHT_RED = (255, 76, 76)


class TextAlign(Enum):
    
    LEFT = 0
    RIGHT = 1
    CENTER = 2
        
        
@dataclass
class Score:
    
    score: float
    n_correct: int
    time: float
    timestamp: int
    player_name: str
    
    
    def to_dict(self) -> None:
        return {
            'score': self.score,
            'nCorrect': self.n_correct,
            'time': self.time,
            'timestamp': self.timestamp,
            'playerName': self.player_name
        }


@dataclass
class ButtonData:
    
    text: str
    bg_color: tuple[int, int, int]
    on_action: Callable[[], None]