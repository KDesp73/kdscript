from keywords import Keyword
import parser
from actions import *

def Statement(state: State, active: list):
    if parser.take_string(state, Keyword.ECHO): run_echo(state, active)
    elif parser.take_string(state, Keyword.IF): run_if_else(state, active)
    elif parser.take_string(state, Keyword.WHILE): run_while(state, active)
    elif parser.take_string(state, Keyword.ESC): run_break(active) 
    elif parser.take_string(state, Keyword.CALL): run_call(state, active)
    elif parser.take_string(state, Keyword.FUNC): run_func_def(state)
    elif parser.take_string(state, Keyword.EXIT): run_exit(state, active)
    else: run_assign(state, active)
