from node import Node
from DLinkedList import LinkedList


class BaseStack(LinkedList):
    def __init__(self) -> None:
        super().__init__()

    def isEmpty(self):
        return self.count() == 0

    def push(self, data):
        self.insert(data=data)

    def pop(self):
        node = Node()
        if self.first(node=node) is False:
            print("pop(): stack empty")
            return None

        data = self.remove()
        assert node.data == data
        return data

    def peek(self):
        node = Node()
        if self.first(node=node) is False:
            print("peek(): stack empty")
            return None

        return node.data


if __name__ == "__main__":
    stack = BaseStack()
    print(stack.isEmpty())
    stack.push(1)
    stack.push(2)
    stack.print()
    print(stack.peek())
    print(stack.isEmpty())
    print(stack.pop())
    print(stack.pop())
