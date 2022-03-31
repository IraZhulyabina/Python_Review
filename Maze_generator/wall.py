class Wall:
    def __init__(self):
        self._does_exist = True

    def does_exist(self):
        return self._does_exist

    def make_nonexistent(self):
        self._does_exist = False
