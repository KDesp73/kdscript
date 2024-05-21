from state import State

def error(state: State, msg):
    s = state.source[:state.position].rfind("\n") + 1
    e = state.source.find("\n", state.position)

    line = state.source[:state.position].count("\n") + 1

    print("\nERROR " + msg + " -> Line: " + str(line) + ": '" + state.source[s:state.position] + "_" + state.source[state.position:e] + "'\n")

    exit(1)
