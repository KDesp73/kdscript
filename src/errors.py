from state import State

def error(state: State, msg):
    s = state.source[:state.position].rfind("\n") + 1; e = state.source.find("\n", state.position)
    print("\nERROR " + msg + " in line " + str(state.source[:state.position].count("\n") + 1) + ": '" + state.source[s:state.position] + "_" + state.source[state.position:e] + "'\n")
    exit(1)
