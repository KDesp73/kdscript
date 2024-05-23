import parser
from actions import *

def Statement(state: State, active: list):
    if parser.take_string(state, "echo"): do_echo(state, active)
    elif parser.take_string(state, "if"): do_if_else(state, active)
    elif parser.take_string(state, "while"): do_while(state, active)
    elif parser.take_string(state, "break"): do_break(active) 
    elif parser.take_string(state, "call"): do_call(state, active)
    elif parser.take_string(state, "func"): do_func_def(state)
    else: do_assign(state, active)
