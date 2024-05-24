from logger import INFO
from utils import *
from state import State

def advance(state: State):
    """
    Increases the current position by 1
    """

    state.position += 1

def inspect(state: State):
    """
    Skips comments and returns current character without advancing
    """

    # TODO: handle removing comments with preproccessor
    if state.source[state.position] == '#':
        while state.source[state.position] != '\n' and state.source[state.position] != '\0':
            advance(state)

    return state.source[state.position]

def take(state: State):
    """
    Returns the current character and advances by one
    """

    c = inspect(state)
    advance(state);
    return c

def take_string(state: State, word: str):
    """
    Checks whether the word is available
    """

    copypc = state.position
    for c in word:
        next_char = inspect(state)
        advance(state)
        if next_char != c: 
            state.position = copypc
            return False
    return True

def next(state: State):
    """
    Returns next non whitespace character
    """

    while WHITE.__contains__(inspect(state)):
        take(state)
    return inspect(state)

def take_next(state: State, c):
    """
    Consumes next character if available
    """

    if next(state) == c:
        take(state)
        return True
    return False

def take_next_alnum(state: State):
    """
    Returns next alphanumeric string
    """

    alnum = ""
    if is_alpha(next(state)):
        while is_alnum(inspect(state)): 
            alnum += take(state)
        
    return alnum

