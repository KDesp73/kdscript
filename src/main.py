import sys

def read_file(path):
    try:
        f = open(path, 'r')
    except: 
        print("ERROR: Can't find source file \'" + path + "\'.")
        exit(1)

    source = f.read() + '\0'
    f.close()
    
    return source

pc = 0
variable = {}
if len(sys.argv) < 2:
    print("USAGE: python3 main.py <file>")
    exit(1)
source = read_file(sys.argv[1])

WHITE = [' ', '\t', '\n', '\r']

def is_digit(c): return (c >= '0' and c <= '9')
def is_alpha(c): return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')
def is_alnum(c): return is_digit(c) or is_alpha(c)
def is_add_op(c): return (c == '+' or c == '-')
def is_mul_op(c): return (c == '*' or c == '/')

def BooleanFactor(active):
    inv = take_next('!')
    e = Expression(active)
    b = int(e[1])

    next()
    
    if (e[0] == 'i'):	
        if take_string("=="): b = (b == MathExpression(active))
        elif take_string("!="): b = (b != MathExpression(active))
        elif take_string("<="): b = (b <= MathExpression(active))
        elif take_string("<"): b = (b < MathExpression(active))
        elif take_string(">="): b = (b >= MathExpression(active))
        elif take_string(">"): b = (b > MathExpression(active))
    else:
        if take_string("=="): b = (b == StringExpression(active))
        elif take_string("!="): b = (b != StringExpression(active))
        else: b = (b != "")

    return active[0] and (b != inv)	

def BooleanTerm(active):
    b = BooleanFactor(active)
    while take_next('&'): b = b & BooleanFactor(active)
    return b

def BooleanExpression(active):
    b = BooleanTerm(active)
    while take_next('|'): b = b | BooleanTerm(active)
    return b

def MathFactor(active):
    m = 0
    if take_next('('):
        m = MathExpression(active)
        if not take_next(')'): error("missing ')'")
    elif is_digit(next()):
        while is_digit(inspect()): m = 10 * m + ord(take()) - ord('0') 
    elif take_string("val("):
        s = String(active)
        if active[0] and s.isdigit(): m = int(s)
        if not take_next(')'): error("missing ')'")
    else: 
        id = take_next_alnum()
        if id not in variable or variable[id][0] != 'i': error("unknown variable")
        elif active[0]: m = variable[id][1]
    
    return m

def MathTerm(active):
    m = MathFactor(active)
    while is_mul_op(next()):
        c = take()
        m2 = MathFactor(active)
        if c == '*': m = m * m2
        else: m = m / m2

    return m

def MathExpression(active):
    c = next()
    if is_add_op(c):
        c = take()
    m = MathTerm(active)
    if c == '-': m = -m
    while is_add_op(next()):
        c = take()
        m2 = MathTerm(active)
        if c == '+': m = m + m2
        else: m = m - m2
    return m

def String(active):
    s = ""
    if take_next('\"'):	
        while not take_string("\""):
            if inspect() == '\0': error("unexpected EOF")
            if take_string("\\n"): s += '\n'
            else: s += take()
    elif take_string("str("):
        s = str(MathExpression(active))
        if not take_next(')'): error("missing ')'")
    elif take_string("input()"):
        if active[0]: s = input()
    else: 
        id = take_next_alnum()
        if id in variable and variable[id][0] == 's':	s = variable[id][1]
        else: error("not a string")
    return s

def StringExpression(active):
    s = String(active)
    while take_next('+'): s += String(active)
    return s

def Expression(active):
    global pc
    copypc = pc
    id = take_next_alnum()
    pc = copypc

    if next() == '\"' or id == "str" or id == "input" or (id in variable and variable[id][0] == 's'):
        return ('s', StringExpression(active))
    else: return ('i', MathExpression(active))

def inspect():
    global pc
    
    if source[pc] == '#':
        while source[pc] != '\n' and source[pc] != '\0':
            pc += 1
    return source[pc]

def take():
    global pc
    c = inspect()
    pc += 1;
    return c

def take_string(word: str):
    global pc
    copypc = pc
    for c in word:
        if take() != c: 
            pc = copypc
            return False
    return True

def next():
    while WHITE.__contains__(inspect()):
        take()
    return inspect()

def take_next(c):
    if next() == c:
        take()
        return True
    return False

def take_next_alnum():
    alnum = ""
    if is_alpha(next()):
        while is_alnum(inspect()): alnum += take()

    return alnum

def block(active):
    if take_next('{'):
        while not take_next('}'):
            block(active)
    else: 
        statement(active)

def program():
    active = [True]
    while next() != '\0':
        block(active)

def do_assign(active):
    id = take_next_alnum()
    if not take_next('=') or id == "": error("unknown statement")
    e = Expression(active)
    if active[0] or id not in variable:
        variable[id] = e

def do_func_def():
    global pc
    id = take_next_alnum()
    if id == "": error("missing funcroutine identifier")
    variable[id] = ('p', pc)
    block([False])

def do_call(active):
    global pc
    id = take_next_alnum()
    if id not in variable or variable[id][0] != 'p': error("unknown funcroutine")
    ret = pc
    pc = variable[id][1]
    block(active)
    pc = ret

def do_if_else(active):
    b = BooleanExpression(active)
    if active[0] and b: block(active)
    else: block([False])
    next()
    if take_string("else"):
        if active[0] and not b:
            block(active)
        else: block([False])

def do_while(active):
    global pc
    local = [active[0]]
    pc_while = pc
    while BooleanExpression(local):
        block(local)
        pc = pc_while
    block([False])

def do_echo(active):
    while True:
        e = Expression(active)
        if active[0]: print(e[1], end="")
        if not take_next(','): return

def do_break(active):
    if active[0]: active[0] = False

def statement(active):
    if take_string("echo"): do_echo(active)
    elif take_string("if"): do_if_else(active)
    elif take_string("while"): do_while(active)
    elif take_string("break"): do_break(active) 
    elif take_string("call"): do_call(active)
    elif take_string("func"): do_func_def()
    else: do_assign(active)

def error(msg):
    s = source[:pc].rfind("\n") + 1; e = source.find("\n", pc)
    print("\nERROR " + msg + " in line " + str(source[:pc].count("\n") + 1) + ": '" + source[s:pc] + "_" + source[pc:e] + "'\n")
    exit(1)

if __name__ == "__main__":
    program()
