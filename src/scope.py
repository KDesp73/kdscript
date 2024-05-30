from linked_list import LinkedList, Node
from typing import Optional, Tuple
from logger import DEBU, WARN

from variable import Variable

class Scope:
    def __init__(self):
        self.scopes = LinkedList()
        self.scopes.insertAtBegin({})
        self.current_scope: Optional[Node] = self.scopes.head
        self.return_value = None

    def enter_scope(self):
        self.scopes.insertAtEnd({})
        self.current_scope = self.scopes.head
        while self.current_scope and self.current_scope.next:
            self.current_scope = self.current_scope.next

    def exit_scope(self):
        if self.scopes.sizeOfLL() > 1:
            self.scopes.remove_last_node()
            self.current_scope = self.scopes.head
            while self.current_scope and self.current_scope.next:
                self.current_scope = self.current_scope.next
        else:
            raise Exception("Cannot exit global scope")

    def set_variable(self, id, type_value: Tuple):
        if self.current_scope:
            self.current_scope.data[id] = type_value
        else:
            raise Exception("No current scope available")

    def set_global_variable(self, id, type_value: Tuple):
        if self.scopes.head is not None:
            self.scopes.head.data[id] = type_value
        else:
            raise Exception("No global scope available")

    def get_variable(self, name: str):
        current = self.scopes.head
        while current is not None:
            if name in reversed(current.data):
                return current.data[name]
            current = current.next
    
        return (Variable.NULL, 0)

    def get_global_variable(self, name: str):
        current = self.scopes.head
        if current is not None:
            if name in reversed(current.data):
                return current.data[name]
    
        return (Variable.NULL, 0)

    def set_return_value(self, value):
        self.return_value = value

    def get_return_value(self):
        return self.return_value

    def clear_return_value(self):
        self.return_value = None

    def call_function(self, func, *args, arguments: list):
        self.enter_scope()
        index = 1
        for arg in arguments:
            self.set_variable(f"_{index}", arg)
            index += 1

        try:
            func(*args)
        finally:
            self.exit_scope()
