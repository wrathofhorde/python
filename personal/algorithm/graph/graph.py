from icecream import ic
from vertics import Vertics, comp_vertics
from DLinkedList import LinkedList

# ic.disable()


class Graph:
    def __init__(self, numOfVertics) -> None:
        self.dict = dict()
        self.numOfEdges = 0
        self.numOfVertics = numOfVertics

        for v in Vertics:
            if v.value >= self.numOfVertics:
                break

            self.dict[v] = LinkedList()
            self.dict[v].setSortRule(comp_vertics)

        ic(self.dict)

    def addEdge(self, fromV, toV):
        if fromV.value >= self.numOfVertics or toV.value >= self.numOfVertics:
            raise ValueError

        self.dict[fromV].insert(toV)
        self.dict[toV].insert(fromV)
        self.numOfEdges += 1

    def showGraphEdgeInfo(self):
        for k, v in self.dict.items():
            print(k, end=": ")
            v.print()

    def print(self):
        print(f"number of vertics:{self.numOfVertics}")
        print(f"number of edges:{self.numOfEdges}")

        self.showGraphEdgeInfo()


if __name__ == "__main__":
    graph = Graph(5)
    graph.addEdge(Vertics.A, Vertics.B)
    graph.addEdge(Vertics.A, Vertics.D)
    graph.addEdge(Vertics.B, Vertics.C)
    graph.addEdge(Vertics.C, Vertics.D)
    graph.addEdge(Vertics.D, Vertics.E)
    graph.addEdge(Vertics.E, Vertics.A)
    graph.print()
