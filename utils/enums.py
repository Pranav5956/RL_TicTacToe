from enum import Enum
from typing import Dict, List, Tuple


class TileType(Enum):
    EMPTY = 0
    VISITED = 1
    CROSSED = 2
    START = 3
    END = 4
    WALL = 5
    COIN = 6


class Directions(Enum):
    TOP = (-1, 0)
    BOTTOM = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


Maze = List[List[TileType]]
Position = Tuple[int, int]
Observations = List[int]
Action = Directions
Actions = List[Directions]
QTable = Dict[str, List[float]]
Rewards = List[float]
State = Position
Response = [State, float, bool]
