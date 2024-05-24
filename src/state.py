from utils import read_file

class State:
    variables = {}
    # TODO: updated these accordingly
    # line = 1
    # column = 1

    def __init__(self, file, position):
        self.file = file
        self.position = position
        self.source = read_file(file)
