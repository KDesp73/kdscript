from logger import INFO
from utils import *
from state import State


def inspect(state: State):
    """
    Skips comments and returns current character without advancing
    """

    if state.source[state.position] == '#':
        while state.source[state.position] != '\n' and state.source[state.position] != '\0':
            state.position += 1

    return state.source[state.position]

def take(state: State):
    """
    Returns the current character and advances by one
    """

    c = inspect(state)
    state.position += 1;
    return c

def take_string(state: State, word: str):
    """
    Checks whether the word is available
    """

    copypc = state.position
    for c in word:
        if take(state) != c: 
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

