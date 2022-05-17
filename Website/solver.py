import random


class MazeSolver:
    @staticmethod
    def solve(maze_):
        maze_.set_all_unused()
        current_cell = maze_.get_cell(1, 1)
        processed_cells = list()
        maze_.set_used(current_cell)
        maze_.make_way(current_cell)
        while current_cell != maze_.end:
            neighbours = maze_.get_reachable_neighbours(current_cell)
            last_visited = list()
            if len(neighbours):
                processed_cells.append(current_cell)
                last_visited.append(current_cell)
                next_cell = random.choice(neighbours)
                if next_cell.is_used():
                    while len(last_visited) and last_visited[-1] != next_cell:
                        maze_.unmake_way(last_visited[-1])
                        maze_.set_unused(last_visited[-1])
                        last_visited.pop()
                current_cell = next_cell
                maze_.set_used(current_cell)
                maze_.make_way(current_cell)
            elif len(processed_cells):
                current_cell = processed_cells.pop()
        return maze_
