from random import randrange, shuffle
from utils.enums import Directions, Maze, TileType

movement_offsets = [Directions.TOP.value, Directions.LEFT.value,
                    Directions.BOTTOM.value, Directions.RIGHT.value]


def generate_maze(rows: int, cols: int) -> Maze:
    start = (randrange(1, rows - 1), randrange(1, cols - 1))
    visited = {start: True}
    steps = randrange(rows * cols // 2, (rows * cols * 3) // 4)
    stack = [start]

    maze = [
        [TileType.WALL for _ in range(cols)] for _ in range(rows)
    ]
    start_is_set = False
    free_cells = []

    while stack and steps > 0:
        steps -= 1
        cr, cc = stack.pop()

        if not start_is_set:
            maze[cr][cc] = TileType.START
            start_is_set = True
        else:
            maze[cr][cc] = TileType.EMPTY
            free_cells.append((cr, cc))

        shuffle(movement_offsets)
        neighbors = [
            (cr + row_offset, cc + col_offset) for row_offset, col_offset in movement_offsets
            if 1 <= cr + row_offset < rows - 1
            and 1 <= cc + col_offset < cols - 1
            and maze[cr + row_offset][cc + col_offset] not in (TileType.START, TileType.END)
        ]

        for neighbor in neighbors:
            if not visited.get(neighbor, False):
                visited[neighbor] = True
                stack.append(neighbor)

    maze[cr][cc] = TileType.END

    return maze, start
