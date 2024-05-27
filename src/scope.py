class Scope:
    def __init__(self):
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise Exception("Cannot exit global scope")

    def set_variable(self, name, value):
        self.scopes[-1][name] = value

    def get_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable '{name}' not found")

    def set_global_variable(self, name, value):
        self.scopes[0][name] = value

    def call_function(self, func, *args):
        self.enter_scope()
        func(*args)
        self.exit_scope()
