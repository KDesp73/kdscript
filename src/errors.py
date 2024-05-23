from state import State

class Error:
    def __init__(self, state: State, message):
        self.state = state
        self.message = message

    def throw(self, severe: bool = True):
        s = self.state.source[:self.state.position].rfind("\n") + 1
        e = self.state.source.find("\n", self.state.position)
        line = self.state.source[:self.state.position].count("\n") + 1

        print("\nERROR " + self.message + " -> Line: " + str(line) + ": '" + self.state.source[s:self.state.position] + "_" + self.state.source[self.state.position:e] + "'\n")

        if severe: exit(1)
