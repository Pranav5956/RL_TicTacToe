from typing import List
from objects.agent import Agent
from objects.tile import Tile
from utils.constants import *
from utils.enums import *
from utils.maze import generate_maze


class Environment:
    def __init__(self, maze_tiles: List[List[Tile]], agent: Agent) -> None:
        self._actions = [direction for direction in Directions]
        self._current_action = None
        self._maze = None
        self._maze_tiles = maze_tiles
        self._agent = agent
        self._observations = []

        self._state = None

    @property
    def maze(self) -> Maze:
        return self._maze

    @property
    def state(self) -> State:
        return self._state

    @property
    def actions(self) -> Actions:
        return self._actions

    @property
    def observations(self) -> Observations:
        return self.__encoded_observations()

    @property
    def current_action(self) -> Action:
        return self._current_action

    def __apply_action(self) -> State:
        return self._state[0] + self._current_action.value[0], self._state[1] + self._current_action.value[1]

    def __encoded_observations(self) -> str:
        row, col = self._state
        self._observations = [
            str(self._maze[row + row_offset][col + col_offset].value)
            for row_offset in (-1, 0, 1)
            for col_offset in (-1, 0, 1)
            if not row_offset == 0 or not col_offset == 0
        ]

        return ''.join(self._observations)

    def __update_maze_tile(self, position: Position, tile_type: TileType) -> None:
        self._maze_tiles[position[0]][position[1]
                                      ].tile_type = tile_type

    def reset(self) -> State:
        self._maze, self._state = generate_maze(TILE_ROW_COUNT, TILE_COL_COUNT)

        for row in range(TILE_ROW_COUNT):
            for col in range(TILE_COL_COUNT):
                self.__update_maze_tile((row, col), self._maze[row][col])

        return self.__encoded_observations()

    def step(self, action: Action) -> Response:
        self._current_action = action
        next_state = self.__apply_action()
        next_tile = self._maze[next_state[0]][next_state[1]]

        if next_tile is TileType.WALL:
            return self.__encoded_observations(), -0.75, False

        if next_tile is TileType.COIN:
            self._state = next_state
            self._agent.update_position(self._state)
            self.__update_maze_tile(self._state, TileType.EMPTY)
            return self.__encoded_observations(), 0.75, False

        if next_tile is TileType.END:
            self._state = next_state
            self._agent.update_position(self._state)
            return self.__encoded_observations(), 1, True

        if next_tile is TileType.VISITED:
            self._state = next_state
            self._agent.update_position(self._state)
            self.__update_maze_tile(self._state, TileType.CROSSED)
            return self.__encoded_observations(), -0.1, False

        if next_tile is TileType.CROSSED:
            self._state = next_state
            self._agent.update_position(self._state)
            return self.__encoded_observations(), -0.3, False

        self._state = next_state
        self._agent.update_position(self._state)
        if next_tile is TileType.EMPTY:
            self.__update_maze_tile(self._state, TileType.VISITED)

        return self.__encoded_observations(), -0.001, False
