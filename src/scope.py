from variable import Variable


class Scope:
    GLOBAL_SCOPE = 0
    def __init__(self):
        self.scopes = [{}]
        self.current_scope = Scope.GLOBAL_SCOPE

    def enter_scope(self):
        self.scopes.append({})
        self.current_scope = len(self.scopes) - 1

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.current_scope = self.current_scope - 1 if self.current_scope > 0 else Scope.GLOBAL_SCOPE
        else:
            raise Exception("Cannot exit global scope")

    def set_variable(self, id, type_value: tuple):
        self.scopes[-1][id] = type_value

    def set_global_variable(self, id, type_value: tuple):
        self.scopes[Scope.GLOBAL_SCOPE][id] = type_value

    def get_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        
        return (Variable.NULL, 0)

    def call_function(self, func, *args):
        self.enter_scope()
        func(*args)
        self.exit_scope()
