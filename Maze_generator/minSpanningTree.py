import maze
import random


class MinSpanningTreeGenerator:
    def __init__(self, height, width):
        self._maze = maze.Maze(height, width)

    def generate(self):
        self._maze.clear_maze()
        cells_to_use = [self._maze.get_cell(1, 1)]
        while len(cells_to_use):
            cur_cell = random.choice(cells_to_use)
            if not cur_cell.is_used():
                cells_to_use.remove(cur_cell)
                self._maze.set_used(cur_cell)
                neighbours = self._maze.get_visited_neighbours(cur_cell)
                if len(neighbours):
                    neighbour = random.choice(neighbours)
                    self._maze.remove_wall(cur_cell, neighbour)
                for el in self._maze.get_neighbours(cur_cell):
                    cells_to_use.append(el)
            else:
                cells_to_use.remove(cur_cell)
        self._maze.set_all_unused()
        return self._maze
