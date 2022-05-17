import cell
import numpy as np
import sys
import wall


class Maze:
    def __init__(self, height, width):
        self._height = height * 2 + 1
        self._width = width * 2 + 1
        self._maze = list()
        for i in range(self._height):
            self._maze.append(list())
            for j in range(self._width):
                if i % 2 and j % 2:
                    self._maze[i].append(cell.Cell(i, j))
                else:
                    self._maze[i].append(wall.Wall())
        self._maze[self._height - 2][self._width - 1].make_nonexistent()
        self._maze[1][1].set_player_here()
        self._player_cell = self._maze[1][1]

    def __get_all_neighbours__(self, current_cell):
        neighbours = list()
        cur_x_coord, cur_y_coord = current_cell.get_coordinates()
        distances = [(0, -2), (0, 2), (2, 0), (-2, 0)]
        for dist in distances:
            x_coord = cur_x_coord + dist[0]
            y_coord = cur_y_coord + dist[1]
            if 0 < x_coord < self._height and 0 < y_coord < self._width:
                neighbours.append(self._maze[x_coord][y_coord])
        return neighbours

    def __is_there_wall__(self, first_cell, second_cell):
        cur_x_coord, cur_y_coord = first_cell.get_coordinates()
        next_x_coord, next_y_coord = second_cell.get_coordinates()
        x_coord = (cur_x_coord + next_x_coord) // 2
        y_coord = (cur_y_coord + next_y_coord) // 2
        return self._maze[x_coord][y_coord].does_exist()

    @property
    def end(self):
        return self._maze[self._height - 2][self._width - 2]

    def make_way(self, cur_cell):
        x_coord, y_coord = cur_cell.get_coordinates()
        self._maze[x_coord][y_coord].make_way()

    def unmake_way(self, cur_cell):
        x_coord, y_coord = cur_cell.get_coordinates()
        self._maze[x_coord][y_coord].unmake_way()

    def set_used(self, cur_cell):
        x_coord, y_coord = cur_cell.get_coordinates()
        self._maze[x_coord][y_coord].set_used()

    def set_unused(self, cur_cell):
        x_coord, y_coord = cur_cell.get_coordinates()
        self._maze[x_coord][y_coord].set_unused()

    def get_reachable_neighbours(self, cur_cell):
        all_neighbours = list()
        neighbours = self.__get_all_neighbours__(cur_cell)
        for neighbour in neighbours:
            if not self.__is_there_wall__(cur_cell, neighbour) and (not neighbour.is_used() or neighbour.is_way()):
                all_neighbours.append(neighbour)
        return all_neighbours

    def get_visited_neighbours(self, current_cell):
        all_neighbours = list()
        neighbours = self.__get_all_neighbours__(current_cell)
        for neighbour in neighbours:
            if neighbour.is_used():
                all_neighbours.append(neighbour)
        return all_neighbours

    def clear_maze(self):
        for i in range(self._height):
            self._maze.append(list())
            for j in range(self._width):
                if i % 2 and j % 2:
                    self._maze[i][j].set_unused()
                else:
                    self._maze[i][j].declare_existence()
        self._maze[1][0].make_nonexistent()
        self._maze[self._height - 2][self._width - 1].make_nonexistent()

    def get_neighbours(self, current_cell):
        all_neighbours = list()
        neighbours = self.__get_all_neighbours__(current_cell)
        for neighbour in neighbours:
            if not neighbour.is_used():
                all_neighbours.append(neighbour)
        return all_neighbours

    def remove_wall(self, current_cell, next_cell):
        cur_x_coord, cur_y_coord = current_cell.get_coordinates()
        next_x_coord, next_y_coord = next_cell.get_coordinates()
        x_coord = (cur_x_coord + next_x_coord) // 2
        y_coord = (cur_y_coord + next_y_coord) // 2
        self._maze[x_coord][y_coord].make_nonexistent()

    def get_random_unused(self):
        while True:
            x_coord = np.random.choice(range(1, self._width, 2), 1)
            y_coord = np.random.choice(range(1, self._height, 2), 1)
            if self._maze[y_coord[0]][x_coord[0]].is_unused:
                yield self._maze[y_coord[0]][x_coord[0]]

    def set_all_unused(self):
        for i in range(1, self._height, 2):
            for j in range(1, self._width, 2):
                self._maze[i][j].set_unused()

    def get_unused(self):
        unused = list()
        for i in range(1, self._height, 2):
            for j in range(1, self._width, 2):
                if not self._maze[i][j].is_used():
                    unused.append(self._maze[i][j])
        return unused

    def get_cell(self, x_coord, y_coord):
        return self._maze[x_coord * 2 - 1][y_coord * 2 - 1]

    def get_height(self):
        return self._height // 2

    def get_width(self):
        return self._width // 2

    def draw_solution(self, file=sys.stdout):
        print("<!DOCTYPE html>", '<html lang="en">', "<head>", '    <meta charset="UTF-8">',
              '    <title>Labyrinth</title>', '    <link rel="stylesheet" href="../static/lab_game.css">',
              '</head>', '<body>', '<div class="vertical-center">', '<pre>', sep='\n', file=file)
        print('<h1>', end='', file=file)
        for j in range(1, self._width, 2):
            if self._maze[0][j].does_exist():
                print('___ ', end='', file=file)
            else:
                print(' ', end='', file=file)
        print('</h1>', file=file)
        for i in range(1, self._height, 2):
            print('<h1>', end='', file=file)
            for j in range(self._width):
                if j % 2:
                    if self._maze[i + 1][j].does_exist() and self._maze[i][j].is_way():
                        print("_", "\u2022", "_", sep="", end='', file=file)
                    elif self._maze[i + 1][j].does_exist():
                        print('___', end='', file=file)
                    elif self._maze[i][j].is_way():
                        print(' \u2022 ', end='', file=file)
                    else:
                        print('   ', end='', file=file)
                else:
                    if self._maze[i][j].does_exist():
                        print('|', end='', file=file)
                    else:
                        print(' ', end='', file=file)
            print('</h1>', file=file)
        print('</pre>', '</div>', file=file)
        print('''<form method="get" action="/Labyrinth">
            <button class="button button1" type="submit">Back</button>
        </form>''', file=file)
        print('</body>', '</html>', sep='\n', file=file)

    def draw(self, file=sys.stdout):
        print("<!DOCTYPE html>", '<html lang="en">', "<head>", '    <meta charset="UTF-8">',
              '    <title>Labyrinth</title>', '    <link rel="stylesheet" href="../static/lab_game.css">',
              '<meta http-equiv="refresh" content="0.5; URL=/Labyrinth/game">', '</head>', '<body>',
              '<div class="vertical-center">', '<pre>', sep='\n', file=file)
        print('<h1>', end='', file=file)
        for j in range(1, self._width, 2):
            if self._maze[0][j].does_exist():
                print('___ ', end='', file=file)
            else:
                print(' ', end='', file=file)
        print('</h1>', file=file)
        for i in range(1, self._height, 2):
            print('<h1>', end='', file=file)
            for j in range(self._width):
                if j % 2:
                    if self._maze[i][j].is_player_here() and self._maze[i + 1][j].does_exist():
                        print("_@_", end='', file=file)
                    elif self._maze[i][j].is_player_here():
                        print(" @ ", end='', file=file)
                    elif self._maze[i + 1][j].does_exist():
                        print('___', end='', file=file)
                    else:
                        print('   ', end='', file=file)
                else:
                    if self._maze[i][j].does_exist():
                        print('|', end='', file=file)
                    else:
                        print(' ', end='', file=file)
            print('</h1>', file=file)
        print('</pre>', '</div>', file=file)
        print('''<script>
  document.addEventListener('keydown', (event) => {
    var name = event.key;
    if (name == "ArrowRight" || name == "ArrowDown" || name == "ArrowUp" || name == "ArrowLeft") {
      var xhr = new XMLHttpRequest();
      xhr.open("POST", '/Labyrinth/game');
      xhr.setRequestHeader('Content-Type', 'application/json');
      xhr.send(JSON.stringify({name: name}));
    }
  }, false);
</script>''', file=file)
        print('''<form method="get" action="/Labyrinth/solution">
    <button class="button button1" type="submit">Solution</button>
</form>''', file=file)
        print('</body>', '</html>', sep='\n', file=file)

    def move(self, letter):
        x, y = self._player_cell.get_coordinates()
        print(x, y)
        if letter == 'a' and not self._maze[x][y - 1].does_exist() and y != 1:
            self._maze[x][y].set_player_not_here()
            self._maze[x][y - 2].set_player_here()
            self._player_cell = self._maze[x][y - 2]
        if letter == 'd' and not self._maze[x][y + 1].does_exist():
            self._maze[x][y].set_player_not_here()
            self._maze[x][y + 2].set_player_here()
            self._player_cell = self._maze[x][y + 2]
        if letter == 'w' and not self._maze[x - 1][y].does_exist() and x != 1:
            self._maze[x][y].set_player_not_here()
            self._maze[x - 2][y].set_player_here()
            self._player_cell = self._maze[x - 2][y]
        if letter == 's' and not self._maze[x + 1][y].does_exist():
            self._maze[x][y].set_player_not_here()
            self._maze[x + 2][y].set_player_here()
            self._player_cell = self._maze[x + 2][y]
        x, y = self._player_cell.get_coordinates()
        print(x, y)
        if x == self._height - 2 and y == self._width - 2:
            return True
        return False
