from logger import INFO
from utils import *
from state import State

def advance(state: State):
    """
    Increases the current position by 1
    """

    state.position += 1
    state.line = line_from_position(state.source, state.position)

def inspect(state: State):
    """
    Returns current character without advancing
    """

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
    nxt = next(state)
    if is_alpha(nxt) or nxt == '_':
        while is_alnum(inspect(state)): 
            alnum += take(state)
        
    return alnum

def make_escape_character(state: State, c) -> str:
    match c:
        case 'n':
            return '\n'
        case 't':
            return '\t'
        case "'":
            return '\''
        case '"':
            return '\"'
        case 'r':
            return '\r'
        case 'b':
            return '\b'
        case 'f':
            return '\f'
        case 'a':
            return '\a'
        case 'v':
            return '\v'
        case '0':
            return '\0'
        case _:
            Error(state, "unrecognized escape character").throw()
            return ""
