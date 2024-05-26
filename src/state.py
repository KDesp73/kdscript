from utils import read_file

class State:
    variables = {}
    # TODO: updated these accordingly
    # line = 1
    # column = 1

    def __init__(self, file, source = "", position = 0):
        self.file = file
        self.position = position
        if source == "":
            self.source = read_file(file)
        else:
            self.source = source

