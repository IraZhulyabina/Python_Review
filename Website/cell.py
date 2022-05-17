class Cell:
    def __init__(self, x, y):
        self._x_coord = x
        self._y_coord = y
        self._is_used = False
        self._is_way = False
        self._is_player_here = False

    def set_player_here(self):
        self._is_player_here = True

    def set_player_not_here(self):
        self._is_player_here = False

    def is_player_here(self):
        return self._is_player_here

    def set_used(self):
        self._is_used = True

    def make_way(self):
        self._is_way = True

    def unmake_way(self):
        self._is_way = False

    def set_unused(self):
        self._is_used = False

    def get_coordinates(self):
        return self._x_coord, self._y_coord

    def is_used(self):
        return self._is_used

    def is_way(self):
        return self._is_way
