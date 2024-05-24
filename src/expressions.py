import parser
from state import State
from statements import Statement
from utils import *
from errors import Error, RuntimeError
from variable import Variable

def BooleanFactor(state: State, active: list):
    inv = parser.take_next(state, '!')
    e = Expression(state, active)
    b = int(e[1])

    parser.next(state)
    
    if (e[0] == Variable.INT):	
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

def BooleanTerm(state: State, active: list):
    b = BooleanFactor(state, active)
    while parser.take_next(state, '&'): b = b & BooleanFactor(state, active)
    return b

def BooleanExpression(state: State, active: list):
    b = BooleanTerm(state, active)
    while parser.take_next(state, '|'): b = b | BooleanTerm(state, active)
    return b

def MathFactor(state, active: list):
    m = 0
    m_dec = 0
    is_dec = False
    if parser.take_next(state, '('): # complex expression
        m = MathExpression(state, active)
        if not parser.take_next(state, ')'): Error(state, "missing ')'").throw()
    elif is_digit(parser.next(state)): # number
        while is_digit(parser.inspect(state)) or parser.inspect(state) == '.': 
            c = parser.take(state)
            
            if c == '.': 
                is_dec = True
                continue
            if not is_dec:
                m = 10 * m + ord(c) - ord('0') 
            else:
                m_dec = 10 * m_dec + ord(c) - ord('0') 
        if is_dec:
            m = m + ( m_dec/(len(str(m_dec)*10)) )
    elif parser.take_string(state, "val("): # string to num
        s = String(state, active)
        if active[0]:
            if s.isdigit(): m = int(s)
            elif is_float(s): 
                m = float(s)
            else: RuntimeError(state, "input not a number").throw()
        if not parser.take_next(state, ')'): Error(state, "missing ')'").throw()
    else: # Variables
        id = parser.take_next_alnum(state)
        if (
                id not in state.variable or 
                (state.variable[id][0] != Variable.INT and state.variable[id][0] != Variable.FLOAT)
            ): 
            Error(state, "unknown state.variable").throw()
        elif active[0]: m = state.variable[id][1]
    
    return m

def MathTerm(state: State, active: list):
    m = MathFactor(state, active)
    while is_mul_op(parser.next(state)):
        c = parser.take(state)
        m2 = MathFactor(state, active)
        if c == '*': 
            m = m * m2
        else: 
            if m2 == 0:
                RuntimeError(state, "Division by zero").throw()
            m = m / m2

    return m

def MathExpression(state: State, active: list):
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

def String(state: State, active: list):
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
        if id in state.variables and state.variables[id][0] == Variable.STRING:
            s = state.variables[id][1]
        else: 
            Error(state, "not a string").throw()
    return s

def StringExpression(state: State, active: list):
    s = String(state, active)
    while parser.take_next(state, '+'): 
        s += String(state, active)
    return s

def Expression(state: State, active: list):
    store_pos = state.position
    id = parser.take_next_alnum(state)
    state.position = store_pos

    if parser.next(state) == '\"' or id == "str" or id == "input" or (id in state.variable and state.variable[id][0] == 's'):
        return ('s', StringExpression(state, active))
    else:
        var = MathExpression(state, active)
        if is_float(var): return ('f', var)
        else: return ('i', var)


    if parser.next(state) == '\"' or id == "str" or id == "input" or (id in state.variables and state.variables[id][0] == Variable.STRING):
        return (Variable.STRING, StringExpression(state, active))
    else: 
        var = MathExpression(state, active)
        if is_float(var): return (Variable.FLOAT, var)
        else: return (Variable.INT, var)

def Block(state: State, active: list):
    if parser.take_next(state, '{'):
        while not parser.take_next(state, '}'):
            Block(state, active)
    else: 
        Statement(state, active)

def Program(state: State):
    active = [True]
    while parser.next(state) != '\0':
        Block(state, active)

