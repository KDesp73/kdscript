class Variable:
    """
    Referring to variables and methods
    """

    INT = 'i'
    FLOAT = 'f'
    CHAR = 'c'
    STRING = 's'
    METHOD = 'm'
    ARRAY = 'a'
    NULL = 'n'

    def __init__(self, type: str, id: str, value) -> None:
        self.type = type
        self.id = id
        self.value = value

def get_type(item):
    if isinstance(item, int): return Variable.INT
    elif isinstance(item, float): return Variable.FLOAT
    elif isinstance(item, str): return Variable.STRING
    elif isinstance(item, list): return Variable.ARRAY
    else: return Variable.NULL
