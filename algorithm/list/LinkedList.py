class LData:
    def __init__(self, data = None):
        self.data = data

class Node:
    def __init__(self, lData = None):
        self.size = 0
        self.next = None
        self.lData = lData

class SimpleList:
    def __init__(self):
        self.size = 0
        self.curr = None
        self.prev = None
        self.comp = None
        self.head = Node()

    def insert(self, ldata):
        newNode = Node(ldata)
        newNode.next = self.head.next
        self.head.next = newNode
        self.count += 1

    def first(self):
        self.prev = self.head
        self.curr = self.prev.next

    def next(self):
        if self.curr.next == None:
            return False
        self.prev = self.curr
        self.curr = self.prev.next
        return True

    def remove(self):
        if self.curr == None:
            return False
        self.prev.next = self.curr.next
        self.curr = self.prev.next
        self.count -= 1
        return True

    def count(self):
        return self.count

    def setSortRule(self, comp):
        self.comp = comp

def compare(lhs, rhs):
    if lhs.data < rhs.data:
        return True
    else:
        return False
