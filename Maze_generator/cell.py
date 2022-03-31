class Cell:
    def __init__(self, x, y):
        self._x_coord = x
        self._y_coord = y
        self._is_used = False

    def set_used(self):
        self._is_used = True

    def get_coordinates(self):
        return self._x_coord, self._y_coord

    def is_used(self):
        return self._is_used
