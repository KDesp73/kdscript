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

    def __init__(self, type: str, id: str, value) -> None:
        self.type = type
        self.id = id
        self.value = value

