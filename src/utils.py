import re
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

def write_to_file(filename, text):
    with open(filename, 'w') as file:
        file.write(text)

def is_digit(c): return (c >= '0' and c <= '9')
def is_float(c): return (re.match(r"^[0-9]*\.[0-9]*$", str(c)) != None)
def is_alpha(c): return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z')
def is_alnum(c): return is_digit(c) or is_alpha(c) or c == '_'
def is_add_op(c): return (c == '+' or c == '-')
def is_mul_op(c): return (c == '*' or c == '/' or c == '%')
def is_int(s: str):
    try:
        int(s)
        return True
    except ValueError:
        return False

def line_from_position(code: str, position: int):
    return code[:position].count("\n") + 1


def count_digits(number):
    return len(str(number).replace('-', '').replace('.', '').replace('e', '').replace('+', ''))

def print_enumarated(source: str):
    i = 1
    for line in source.split('\n'):
        print(i, end="")
        print(" " * (5-count_digits(i)) , end="")
        print(line)
        i += 1
    print()

def enable_ansi_escape_codes():
    import os
    import platform
    if platform.system() == 'Windows':
        os.system('')

    elif platform.system() == 'Linux':
        pass  # Usually, no action is needed for Linux
