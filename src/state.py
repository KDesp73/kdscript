from utils import read_file

class State:
    variable = {}

    def __init__(self, file, position):
        self.file = file
        self.position = position
        self.source = read_file(file)
