import sys
from keywords import KEYWORDS
from state import State, debug
import parser
from errors import Error
from logger import DEBU, INFO
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
        if state.scope.get_global_variable(id)[0] != Variable.NULL:
            state.scope.set_global_variable(id, e)
        else:
            state.scope.set_variable(id, e)
        # debug(state)


def run_func_def(state: State):
    from expressions import Block

    id = parser.take_next_alnum(state)
    
    if id == "": 
        Error(state, "missing function identifier").throw()

    if id in KEYWORDS:
        Error(state, f"{id} is a reserved keyword").throw()

    if state.scope.scopes.head != state.scope.current_scope:
        Error(state, "cannot define a function inside another function").throw()

    state.scope.set_variable(id, (Variable.METHOD, state.position))
    # debug(state)

    # Skip block inactively
    Block(state, [False])

def run_call(state: State, active: list):
    from expressions import Block, Expression

    id = parser.take_next_alnum(state)

    args = []
    parser.next(state)
    if parser.take_string(state, "<-"):
        while True:
            e = Expression(state, active)
            args.append(e)   
            if not parser.take_next(state, ','): break


    ret = state.position
    
    method = state.scope.get_global_variable(id) if state.scope.get_global_variable(id)[0] != Variable.NULL else state.scope.get_variable(id)
    if method[0] == Variable.NULL:
        Error(state, "unknown function").throw()

    state.position = method[1]
    
    if active[0]:
        state.scope.call_function(Block, state, active, arguments=args)
    
    state.position = ret

def run_if_else(state: State, active: list):
    def all_false(booleans: list):
        for bool in booleans:
            if bool:
                return False
        return True

    from expressions import BooleanExpression, Block

    b = BooleanExpression(state, active)
    booleans = []
    booleans.append(b)

    if active[0] and b: 
        Block(state, active)
    else:
        Block(state, [False])
    
    parser.next(state)
    
    while parser.take_string(state, "else"):
        if parser.take_string(state, "if"):
            b_elif = BooleanExpression(state, active)
            booleans.append(b_elif)
            if active[0] and b_elif:
                Block(state, active)
            else:
                Block(state, [False])

        if active[0] and all_false(booleans):
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


