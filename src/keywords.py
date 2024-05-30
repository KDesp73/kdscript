class Keyword:
    FUNC = "func"
    CALL = "call"
    IF = "if"
    ELSE = "else"
    WHILE = "while"
    ESC = "esc"
    INPUT = "input"
    VAL = "val"
    STR = "str"
    ECHO = "echo"
    EXIT = "exit"
    AS = "as"
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    ARRAY = "array"
    RETURN = "return"


KEYWORDS = [getattr(Keyword, attr) for attr in dir(Keyword) if not callable(getattr(Keyword, attr)) and not attr.startswith("__")]
