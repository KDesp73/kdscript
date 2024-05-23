WHITE = [' ', '\t', '\n', '\r']

def read_file(path):
    try:
        f = open(path, 'r')
    except: 
        print("ERROR: Can't find source file \'" + path + "\'.")
        exit(1)

    source = f.read() + '\0'
    f.close()
    
    return source

def is_digit(c): return (c >= '0' and c <= '9')
def is_alpha(c): return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')
def is_alnum(c): return is_digit(c) or is_alpha(c) or c == '_'
def is_add_op(c): return (c == '+' or c == '-')
def is_mul_op(c): return (c == '*' or c == '/')
