from scope import Scope
from utils import read_file


class State:
    def __init__(self, file, source = "", position = 0):
        self.file = file
        self.position = position
        if source == "":
            self.source = read_file(file)
        else:
            self.source = source

        self.variables = {}
        self.scope = Scope()

        # TODO: updated these accordingly
        # self.line = 1
        # self.column = 1


def debug(state: State):
    print("---")
    state.scope.scopes.printLL()
    input()
