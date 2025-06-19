from node import Node
from icecream import ic
from graph import Graph
from vertics import Vertics
from BaseStack import BaseStack

# ic.enable()


class Dfs(Graph):
    def __init__(self, numOfVertics) -> None:
        super().__init__(numOfVertics)
        self.visitInfo = dict()

        for v in Vertics:
            if v.value < self.numOfVertics:
                self.visitInfo[v] = False
            else:
                break

    def print(self):
        super().print()
        print(self.visitInfo)

    def visitVertex(self, visitV):
        if self.visitInfo[visitV] is False:
            self.visitInfo[visitV] = True
            print(visitV, end=" ")
            return True

        return False

    def showGraphVertex(self, startV):
        visitV = startV
        stack = BaseStack()
        for k in self.visitInfo.keys():
            self.visitInfo[k] = False

        self.visitVertex(visitV)
        stack.push(visitV)
        nextV = Node()

        while self.dict[visitV].first(nextV) is True:
            visitflag = False

            if self.visitVertex(nextV.data) is True:
                if stack.exist(visitV) is False:
                    stack.push(visitV)
                stack.push(nextV.data)
                visitV = nextV.data
                visitflag = True
            else:
                while self.dict[visitV].next(nextV) is True:
                    if self.visitVertex(nextV.data) is True:
                        if stack.exist(visitV) is False:
                            stack.push(visitV)
                        stack.push(nextV.data)
                        visitV = nextV.data
                        visitflag = True
                        break

            if visitflag == False:
                if stack.isEmpty() == True:
                    break
                else:
                    visitV = stack.pop()

        print()


if __name__ == "__main__":
    dfs = Dfs(8)
    dfs.addEdge(Vertics.A, Vertics.B)
    dfs.addEdge(Vertics.A, Vertics.D)
    dfs.addEdge(Vertics.B, Vertics.C)
    dfs.addEdge(Vertics.D, Vertics.C)
    dfs.addEdge(Vertics.D, Vertics.E)
    dfs.addEdge(Vertics.E, Vertics.F)
    dfs.addEdge(Vertics.E, Vertics.G)
    dfs.addEdge(Vertics.D, Vertics.H)
    dfs.showGraphEdgeInfo()
    dfs.showGraphVertex(Vertics.A)
    dfs.showGraphVertex(Vertics.B)
    dfs.showGraphVertex(Vertics.C)
    dfs.showGraphVertex(Vertics.D)
    dfs.showGraphVertex(Vertics.E)
    dfs.showGraphVertex(Vertics.F)
    dfs.showGraphVertex(Vertics.G)
    dfs.showGraphVertex(Vertics.H)
