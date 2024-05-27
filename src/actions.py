import sys
from keywords import KEYWORDS
from state import State
import parser
from errors import Error
from variable import Variable

def run_exit(state: State, active: list):
    from expressions import Expression

    value = Expression(state, active)[1]
    
    if active[0] and not isinstance(value, int):
        Error(state, "expression is not an integer").throw()

    if active[0]:
        sys.exit(int(value))


def run_assign(state: State, active: list):
    from expressions import Expression

    id = parser.take_next_alnum(state)
    
    if not parser.take_next(state, '=') or id == "": 
        Error(state, "unknown statement").throw()

    if id in KEYWORDS:
        Error(state, f"{id} is a reserved keyword").throw()

    e = Expression(state, active)

    if active[0]:
        state.scope.set_variable(id, e)

def run_func_def(state: State):
    from expressions import Block

    id = parser.take_next_alnum(state)
    
    if id == "": 
        Error(state, "missing funcroutine identifier").throw()

    state.scope.set_variable(id, (Variable.METHOD, state.position))

    # Skip block inactively
    Block(state, [False])

def run_call(state: State, active: list):
    from expressions import Block

    id = parser.take_next_alnum(state)

    ret = state.position
    
    method = state.scope.get_variable(id)
    if method[0] == Variable.NULL:
        Error(state, "unknown function").throw()

    state.position = method[1]
    
    if active[0]:
        state.scope.call_function(Block, state, active)
    
    state.position = ret

def run_if_else(state: State, active: list):
    from expressions import BooleanExpression, Block

    b = BooleanExpression(state, active)
    if active[0] and b: 
        Block(state, active)
    else:
        Block(state, [False])
    
    parser.next(state)
    
    if parser.take_string(state, "else"):
        if active[0] and not b:
            Block(state, active)
        else:
            Block(state, [False])

def run_while(state: State, active: list):
    from expressions import BooleanExpression, Block

    local = [active[0]]
    position_while = state.position

    while BooleanExpression(state, local):
        Block(state, local)
        state.position = position_while
    
    Block(state, [False])

def run_echo(state: State, active: list):
    from expressions import Expression

    while True:
        e = Expression(state, active)
        if active[0]: print(e[1], end="")
        if not parser.take_next(state, ','): return

def run_break(active: list):
    if active[0]: active[0] = False


