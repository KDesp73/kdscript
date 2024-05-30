from typing import Optional, Dict

class Node:
    def __init__(self, data):
        self.data: Dict = data if data is not None else {}
        self.next: Optional['Node'] = None

class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None

    def insertAtBegin(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insertAtEnd(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current_node = self.head
            while current_node.next:
                current_node = current_node.next
            current_node.next = new_node

    def remove_last_node(self):
        if self.head is None:
            return
        if self.head.next is None:
            self.head = None
        else:
            current_node = self.head
            while current_node.next and current_node.next.next:
                current_node = current_node.next
            current_node.next = None

    def sizeOfLL(self):
        size = 0
        current_node = self.head
        while current_node:
            size += 1
            current_node = current_node.next
        return size

    def printLL(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next

