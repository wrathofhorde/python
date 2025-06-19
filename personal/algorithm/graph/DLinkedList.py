from node import Node
from icecream import ic

ic.disable()


class LinkedList:
    def __init__(self) -> None:
        self.head = Node()
        self.curr = None
        self.prev = None
        self.comp = None
        self.num_of_data = 0

    def finsert(self, data) -> None:
        node = Node(data=data)
        curr = self.head
        node.next = curr.next
        curr.next = node
        self.num_of_data += 1
        ic(f"{node.data} is inserted at 1st pos, size:{self.num_of_data}")

    def sinsert(self, data) -> None:
        node = Node(data=data)
        curr = self.head

        while curr.next != None and self.comp(node.data, curr.next.data) != 0:
            curr = curr.next

        node.next = curr.next
        curr.next = node

        self.num_of_data += 1
        ic(f"{node.data} added")

    def insert(self, data) -> None:
        if self.comp is None:
            self.finsert(data=data)
        else:
            self.sinsert(data=data)

    def first(self, node) -> bool:
        self.prev = self.head
        self.curr = self.prev.next

        if self.curr is None:
            return False

        node.data = self.curr.data

        return True

    def next(self, node) -> bool:
        if self.curr.next is None:
            return False

        self.prev = self.curr
        self.curr = self.curr.next
        node.data = self.curr.data

        return True

    def remove(self) -> any:
        if self.curr is None:
            ic("list empty, remove nothing")
            pass

        remove_pos = self.curr
        self.prev.next = remove_pos.next
        self.curr = self.prev
        self.num_of_data -= 1

        ic(f"remove {remove_pos.data}")

        return remove_pos.data

    def count(self) -> int:
        return self.num_of_data

    def setSortRule(self, comp) -> Node:
        self.comp = comp

    def removeAll(self) -> None:
        node = Node()

        if self.first(node) is True:
            self.remove()
            while self.next(node) is True:
                self.remove()
        else:
            ic("list empty, removeAll nothing to do")
            pass

    def exist(self, data) -> bool:
        curr: Node = self.head.next

        while curr is not None:
            if curr.data == data:
                return True
            else:
                curr = curr.next

        return False

    def print(self) -> None:
        list = []
        node = Node()

        if self.first(node) is True:
            list.append(node.data)
            while self.next(node) is True:
                list.append(node.data)

        print(list)


if __name__ == "__main__":
    l1 = LinkedList()
    l1.print()
    l1.insert(3)
    l1.insert(2)
    l1.insert(1)
    l1.insert(8)
    l1.print()
    l1.removeAll()
    l1.removeAll()
    l1.print()

    def comp(lhs, rhs):
        if lhs < rhs:
            return 0
        else:
            return 1

    l2 = LinkedList()
    l2.setSortRule(comp=comp)
    l2.insert(2)
    l2.insert(1)
    l2.insert(3)
    l2.insert(8)
    l2.print()
