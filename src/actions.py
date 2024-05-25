import sys
from keywords import KEYWORDS
from state import State
import parser
from errors import TODO, Error
from utils import is_int
from variable import Variable

def do_exit(state: State, active: list):
    from expressions import MathExpression

    id = parser.take_next_alnum(state)

    if active[0] and id != '':
        if id not in state.variables: 
            Error(state, "unknown variable").throw()

        if state.variables[id][0] != Variable.INT:
            Error(state, "variable type not an int").throw()


    if id != '':
        value = state.variables[id][1]
    else:
        value = MathExpression(state, active)
    
    if active[0] and not isinstance(value, int):
        Error(state, "expression is not an integer").throw()

    if active[0]:
        sys.exit(int(value))


def do_assign(state: State, active: list):
    from expressions import Expression

    id = parser.take_next_alnum(state)
    
    if not parser.take_next(state, '=') or id == "": 
        Error(state, "unknown statement").throw()

    if id in KEYWORDS:
        Error(state, f"{id} is a reserved keyword").throw()

    e = Expression(state, active)
    if active[0] or id not in state.variables:
        state.variables[id] = e

def do_func_def(state: State):
    from expressions import Block

    id = parser.take_next_alnum(state)
    if id == "": Error(state, "missing funcroutine identifier").throw()
    state.variables[id] = (Variable.METHOD, state.position)

    # Skip block inactively
    Block(state, [False])

def do_call(state: State, active: list):
    from expressions import Block

    id = parser.take_next_alnum(state)
    if id not in state.variables or state.variables[id][0] != Variable.METHOD: 
        Error(state, "unknown function").throw()
    ret = state.position
    state.position = state.variables[id][1]
    if active[0]:
        Block(state, active)
    state.position = ret

def do_if_else(state: State, active: list):
    from expressions import BooleanExpression, Block

    b = BooleanExpression(state, active)
    if active[0] and b: Block(state, active)
    else: Block(state, [False])
    parser.next(state)
    if parser.take_string(state, "else"):
        if active[0] and not b:
            Block(state, active)
        else: Block(state, [False])

def do_while(state: State, active: list):
    from expressions import BooleanExpression, Block

    local = [active[0]]
    position_while = state.position
    while BooleanExpression(state, local):
        Block(state, local)
        state.position = position_while
    Block(state, [False])

def do_echo(state: State, active: list):
    from expressions import Expression

    while True:
        e = Expression(state, active)
        if active[0]: print(e[1], end="")
        if not parser.take_next(state, ','): return

def do_break(active: list):
    if active[0]: active[0] = False
