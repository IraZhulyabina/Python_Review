import random
import maze


class BacktrackingGenerator:
    def __init__(self, height, width):
        self._maze = maze.Maze(height, width)

    def generate(self):
        self._maze.clear_maze()
        current_cell = self._maze.get_cell(1, 1)
        processed_cells = list()
        self._maze.set_used(current_cell)
        while len(self._maze.get_unused()):
            neighbours = self._maze.get_neighbours(current_cell)
            if len(neighbours):
                processed_cells.append(current_cell)
                next_cell = random.choice(neighbours)
                self._maze.remove_wall(current_cell, next_cell)
                current_cell = next_cell
                self._maze.set_used(current_cell)
            elif len(processed_cells):
                current_cell = processed_cells.pop()
            else:
                current_cell = self._maze.get_random_unused()
        return self._maze
