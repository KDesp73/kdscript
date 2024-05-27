from linked_list import LinkedList, Node
from typing import Optional, Tuple
from logger import DEBU, WARN

from variable import Variable

class Scope:
    def __init__(self):
        self.scopes = LinkedList()
        self.scopes.insertAtBegin({})
        self.current_scope: Optional[Node] = self.scopes.head

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

    def call_function(self, func, *args, arguments: list):
        self.enter_scope()
        index = 1
        for index in range(1, 10):
            if arguments.__len__() < index:
                self.set_variable(f"_{index}", (Variable.INT, 0))
            else: 
                self.set_variable(f"_{index}", arguments[index-1])
            index += 1


        try:
            func(*args)
        finally:
            self.exit_scope()
