from state import State
from logger import ERRO
from utils import line_from_position

def print_error(state: State, message, tag: str):
        s = state.source[:state.position].rfind("\n") + 1
        e = state.source.find("\n", state.position)
        line = line_from_position(state.source, state.position)
        print(f"\n{tag}: {message} -> Line: {str(line)}: '{state.source[s:state.position]}_{state.source[state.position:e]}'\n")

class Error:
    def __init__(self, state: State, message):
        self.TAG = "Error"
        self.state = state
        self.message = message

    def throw(self, severe: bool = True):
        print_error(self.state, self.message, self.TAG)
        if severe: exit(1)

class RuntimeError(Error):
    def __init__(self, state: State, message):
         super().__init__(state, message)
         self.TAG = "RuntimeError"

def TODO():
    ERRO("Not implemented yet")
    exit(1)
