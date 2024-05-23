import parser
from state import State
from statements import Statement
from utils import *
from errors import Error

def BooleanFactor(state: State, active):
    inv = parser.take_next(state, '!')
    e = Expression(state, active)
    b = int(e[1])

    parser.next(state)
    
    if (e[0] == 'i'):	
        if parser.take_string(state, "=="): b = (b == MathExpression(state, active))
        elif parser.take_string(state, "!="): b = (b != MathExpression(state, active))
        elif parser.take_string(state, "<="): b = (b <= MathExpression(state, active))
        elif parser.take_string(state, "<"): b = (b < MathExpression(state, active))
        elif parser.take_string(state, ">="): b = (b >= MathExpression(state, active))
        elif parser.take_string(state, ">"): b = (b > MathExpression(state, active))
    else:
        if parser.take_string(state, "=="): b = (b == StringExpression(state, active))
        elif parser.take_string(state, "!="): b = (b != StringExpression(state, active))
        else: b = (b != "")

    return active[0] and (b != inv)	

def BooleanTerm(state: State, active):
    b = BooleanFactor(state, active)
    while parser.take_next(state, '&'): b = b & BooleanFactor(state, active)
    return b

def BooleanExpression(state: State, active):
    b = BooleanTerm(state, active)
    while parser.take_next(state, '|'): b = b | BooleanTerm(state, active)
    return b

def MathFactor(state, active):
    m = 0
    if parser.take_next(state, '('):
        m = MathExpression(state, active)
        if not parser.take_next(state, ')'): Error(state, "missing ')'").throw()
    elif is_digit(parser.next(state)):
        while is_digit(parser.inspect(state)): m = 10 * m + ord(parser.take(state)) - ord('0') 
    elif parser.take_string(state, "val("):
        s = String(state, active)
        if active[0] and s.isdigit(): m = int(s)
        if not parser.take_next(state, ')'): Error(state, "missing ')'").throw()
    else: 
        id = parser.take_next_alnum(state)
        if id not in state.variable or state.variable[id][0] != 'i': Error(state, "unknown state.variable").throw()
        elif active[0]: m = state.variable[id][1]
    
    return m

def MathTerm(state: State, active):
    m = MathFactor(state, active)
    while is_mul_op(parser.next(state)):
        c = parser.take(state)
        m2 = MathFactor(state, active)
        if c == '*': m = m * m2
        else: m = m / m2

    return m

def MathExpression(state: State, active):
    c = parser.next(state)
    if is_add_op(c):
        c = parser.take(state)
    m = MathTerm(state, active)
    if c == '-': m = -m
    while is_add_op(parser.next(state)):
        c = parser.take(state)
        m2 = MathTerm(state, active)
        if c == '+': m = m + m2
        else: m = m - m2
    return m

def String(state: State, active):
    s = ""
    if parser.take_next(state, '\"'):	
        while not parser.take_string(state, "\""):
            if parser.inspect(state) == '\0': 
                Error(state, "unexpected EOF").throw()
            if parser.take_string(state, "\\n"): 
                s += '\n'
            else: 
                s += parser.take(state)
    elif parser.take_string(state, "str("):
        s = str(MathExpression(state, active))
        if not parser.take_next(state, ')'): 
            Error(state, "missing ')'").throw()
    elif parser.take_string(state, "input()"):
        if active[0]: s = input()
    else: 
        id = parser.take_next_alnum(state)
        if id in state.variable and state.variable[id][0] == 's':
            s = state.variable[id][1]
        else: 
            Error(state, "not a string").throw()
    return s

def StringExpression(state: State, active):
    s = String(state, active)
    while parser.take_next(state, '+'): s += String(state, active)
    return s

def Expression(state: State, active):
    copypc = state.position
    id = parser.take_next_alnum(state)
    state.position = copypc

    if parser.next(state) == '\"' or id == "str" or id == "input" or (id in state.variable and state.variable[id][0] == 's'):
        return ('s', StringExpression(state, active))
    else: return ('i', MathExpression(state, active))

def Block(state: State, active):
    if parser.take_next(state, '{'):
        while not parser.take_next(state, '}'):
            Block(state, active)
    else: 
        Statement(state, active)

def Program(state: State):
    active = [True]
    while parser.next(state) != '\0':
        Block(state, active)

