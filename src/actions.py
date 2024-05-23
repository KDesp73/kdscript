from state import State
import parser
from errors import Error

def do_assign(state: State, active):
    from expressions import Expression

    id = parser.take_next_alnum(state)
    if not parser.take_next(state, '=') or id == "": Error(state, "unknown statement").throw()
    e = Expression(state, active)
    if active[0] or id not in state.variable:
        state.variable[id] = e

def do_func_def(state: State):
    from expressions import Block

    id = parser.take_next_alnum(state)
    if id == "": Error(state, "missing funcroutine identifier").throw()
    state.variable[id] = ('p', state.position)

    # Skip block inactively
    Block(state, [False])

def do_call(state: State, active):
    from expressions import Block

    id = parser.take_next_alnum(state)
    if id not in state.variable or state.variable[id][0] != 'p': 
        Error(state, "unknown funcroutine").throw()
    ret = state.position
    state.position = state.variable[id][1]
    Block(state, active)
    state.position = ret

def do_if_else(state: State, active):
    from expressions import BooleanExpression, Block

    b = BooleanExpression(state, active)
    if active[0] and b: Block(state, active)
    else: Block(state, [False])
    parser.next(state)
    if parser.take_string(state, "else"):
        if active[0] and not b:
            Block(state, active)
        else: Block(state, [False])

def do_while(state: State, active):
    from expressions import BooleanExpression, Block

    local = [active[0]]
    position_while = state.position
    while BooleanExpression(state, local):
        Block(state, local)
        state.position = position_while
    Block(state, [False])

def do_echo(state: State, active):
    from expressions import Expression

    while True:
        e = Expression(state, active)
        if active[0]: print(e[1], end="")
        if not parser.take_next(state, ','): return

def do_break(active):
    if active[0]: active[0] = False
