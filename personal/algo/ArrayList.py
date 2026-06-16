class ArrayList:
    def __init__(self):
        self.LIST_LEN = 100
        self.arr = [0]  * 100
        self.numOfData = 0
        self.curPosition = -1

    def insert(self, data):
        if self.numOfData >= self.LIST_LEN:
            print("더 이상 저장이 불가능합니다.")
            return
        
        self.arr[self.numOfData] = data
        self.numOfData += 1
    
    def first(self, data):
        if self.numOfData == 0:
            return False
        
        self.curPosition = 0
        data[0] = self.arr[self.curPosition]
        return True
    
    def next(self, data):
        if self.curPosition >= self.numOfData - 1:
            return False
        
        self.curPosition += 1
        data[0] = self.arr[self.curPosition]
        return True
    
    def remove(self):
        rpos = self.curPosition
        num = self.numOfData
        rdata = self.arr[self.curPosition]

        for i in range(rpos, num - 1):
            self.arr[i] = self.arr[i + 1]

        self.curPosition -= 1
        self.numOfData -= 1
        return rdata
    
    def count(self):
        return self.numOfData

from icecream import ic

if __name__ == "__main__":
    list = ArrayList()
    list.insert(1)
    list.insert(2)
    list.insert(3)
    ic(list.count())

    