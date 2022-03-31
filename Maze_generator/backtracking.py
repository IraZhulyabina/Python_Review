import numpy as np
import cell
import wall


class BacktrackingGenerator:
    def __init__(self, height_, width_):
        self._height = height_ * 2 + 1
        self._width = width_ * 2 + 1
        self._maze = np.ndarray((self._height, self._width))

    def __generate_maze__(self):
        for i in range(self._height):
            for j in range(self._width):
                if i % 2 and j % 2:
                    self._maze[i][j] = cell.Cell(i, j)
                else:
                    self._maze[i][j] = wall.Wall

    def __get_neighbours__(self, current_cell):
        neighbours = list()
        cur_x_coord, cur_y_coord = current_cell.get_coordinates()
        distances = [(0, -2), (0, 2), (2, 0), (-2, 0)]
        for dist in distances:
            x_coord = cur_x_coord + dist[0]
            y_coord = cur_y_coord + dist[1]
            if 0 < x_coord < self._width and 0 < y_coord < self._height:
                if not self._maze[x_coord][y_coord].is_used():
                    neighbours.append(self._maze[x_coord][y_coord])
        return neighbours

    def generate(self):
        self.__generate_maze__()
        current_cell = self._maze[1][1]
        current_cell.set_used()
        processed_cells = list()
        number_of_unused = self._height // 2 * self._width // 2 - 1
        while number_of_unused:
            neighbours = self.__get_neighbours__(current_cell)
            if len(neighbours):
                processed_cells.append(current_cell)
                next_cell = np.random.choice(neighbours, 1)
                self.__remove_wall__(current_cell, next_cell)
                current_cell = next_cell
                current_cell.set_used()
                number_of_unused -= 1
            elif len(processed_cells):
                current_cell = processed_cells.pop()
            else:
                current_cell = self.__get_random_unused__()

    def __get_random_unused__(self):
        while True:
            x_coord = np.random.choice(range(1, self._width, 2), 1)
            y_coord = np.random.choice(range(1, self._length, 2), 1)
            if self._maze[x_coord][y_coord].is_unused:
                yield self._maze[x_coord][y_coord]

    def __remove_wall__(self, current_cell, next_cell):
        cur_x_coord, cur_y_coord = current_cell.get_coordinates()
        next_x_coord, next_y_coord = next_cell.get_coordinates()
        x_coord = np.mean(cur_x_coord, next_x_coord)
        y_coord = np.mean(cur_y_coord, next_y_coord)
        self._maze[x_coord][y_coord].make_nonexistent()
