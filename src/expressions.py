from logger import DEBU, INFO
import parser
from state import State, debug
from statements import Statement
from utils import *
from errors import Error, RuntimeError
from variable import Variable
from keywords import KEYWORDS


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

def MathFactor(state: State, active: list):
    m = 0
    m_dec = 0
    is_floating = False
    if parser.take_next(state, '('): # complex expression
        m = MathExpression(state, active)
        if not parser.take_next(state, ')'): Error(state, "missing ')'").throw()
    elif is_digit(parser.next(state)): # number
        while is_digit(parser.inspect(state)) or parser.inspect(state) == '.': 
            c = parser.take(state)
            
            if c == '.': 
                is_floating = True
                continue

            if not is_floating:
                m = 10 * m + ord(c) - ord('0') 
            else:
                m_dec = 10 * m_dec + ord(c) - ord('0') 
        if is_floating:
            divisor = 10 ** len(str(m_dec))
            m = m + m_dec / divisor
    elif parser.take_string(state, "val("): # string to num
        s = String(state, active)
        if active[0]:
            if is_int(s): 
                m = int(s)
            elif is_float(s): 
                m = float(s)
            else: RuntimeError(state, "input is not a number").throw()
        if not parser.take_next(state, ')'): Error(state, "missing ')'").throw()
    else: # Variables
        id = parser.take_next_alnum(state)

        if id in KEYWORDS:
            Error(state, f"{id} is a reserved keyword").throw()

        variable = state.scope.get_global_variable(id) if state.scope.get_global_variable(id)[0] != Variable.NULL else state.scope.get_variable(id)
        if  active[0] and variable[0] == Variable.NULL:
            Error(state, f"{id} is not defined").throw()

        if active[0] and variable[0] != Variable.INT and variable[0] != Variable.FLOAT:
            Error(state, f"Variable {id} is not a number").throw()

        if active[0]:
            m = variable[1]
    
    return m

def MathTerm(state: State, active: list):
    m = MathFactor(state, active)
    while is_mul_op(parser.next(state)):
        c = parser.take(state)
        m2 = MathFactor(state, active)
        if c == '*': 
            m = m * m2
        elif c == '/': 
            if active[0]: 
                if m2 == 0:
                    RuntimeError(state, "Division by zero").throw()
                m = m / m2
        elif c == '%':
            m = m % m2

    return m

def MathExpression(state: State, active: list):
    c = parser.next(state)

    if is_add_op(c):
        c = parser.take(state)

    m = MathTerm(state, active)

    if c == '-':
        m = -m

    while is_add_op(parser.next(state)):
        c = parser.take(state)
        m2 = MathTerm(state, active)

        if c == '+':
            m = m + m2
        else:
            m = m - m2
    return m

def String(state: State, active: list):
    s = ""
    if parser.take_next(state, '\"'):	
        while not parser.take_string(state, "\""):
            if parser.inspect(state) == '\0': 
                Error(state, "unexpected EOF").throw()
            if parser.take_string(state, "\\"): 
                s += parser.make_escape_character(state, parser.take(state))
            else: 
                s += parser.take(state)
    elif parser.take_string(state, "str("):
        s = str(MathExpression(state, active))
        if not parser.take_next(state, ')'): 
            Error(state, "missing ')'").throw()
    elif parser.take_string(state, "input()"):
        if active[0]:
            s = input()
    else: 
        id = parser.take_next_alnum(state)
        variable = state.scope.get_global_variable(id) if state.scope.get_global_variable(id)[0] != Variable.NULL else state.scope.get_variable(id)
        if variable[0] == Variable.STRING:
            s = str(variable[1])
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

    variable = state.scope.get_global_variable(id) if state.scope.get_global_variable(id)[0] != Variable.NULL else state.scope.get_variable(id)
    if parser.next(state) == '\"' or id == "str" or id == "input" or (variable[0] == Variable.STRING):
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

