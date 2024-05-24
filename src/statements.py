from keywords import Keyword
import parser
from actions import *

def Statement(state: State, active: list):
    if parser.take_string(state, Keyword.ECHO): do_echo(state, active)
    elif parser.take_string(state, Keyword.IF): do_if_else(state, active)
    elif parser.take_string(state, Keyword.WHILE): do_while(state, active)
    elif parser.take_string(state, Keyword.ESC): do_break(active) 
    elif parser.take_string(state, Keyword.CALL): do_call(state, active)
    elif parser.take_string(state, Keyword.FUNC): do_func_def(state)
    else: do_assign(state, active)
