from array import array

class LData:
    def __init__(self, data = 0):
        self.data = data

class ArrayList:
    def __init__(self, size = 100):
        self.size = size
        self.numOfData = 0
        self.curPosition = -1
        self.arr = [LData(0) for _ in range(self.size)]

    def LInsert(self, lData):
        if self.numOfData >= self.size: 
            print("리스트가 가득 찼습니다.")
            return
        
        self.arr[self.numOfData].data = lData.data
        self.numOfData += 1

    def LFirst(self, lData):
        if self.numOfData == 0:
            print("리스트가 비어 있습니다.")
            return False
        
        self.curPosition = 0
        lData.data = self.arr[self.curPosition].data
        return True
    
    def LNext(self, lData):
        if self.curPosition >= self.numOfData - 1:
            return False
        
        self.curPosition += 1
        lData.data = self.arr[self.curPosition].data
        return True
    
    def LRemove(self):
        num = self.numOfData
        pos = self.curPosition
        lData = LData(self.arr[pos].data)

        for i in range(pos, num - 1):
            self.arr[i] = self.arr[i + 1]

        self.numOfData -= 1
        self.curPosition -= 1

        return lData
    
    def LCount(self):
        return self.numOfData

if __name__ == "__main__":
    arr = ArrayList(5)
    arr.LInsert(LData(7))
    arr.LInsert(LData(1))
    arr.LInsert(LData(2))
    arr.LInsert(LData(3))
    arr.LInsert(LData(4))
    arr.LInsert(LData(5))

    lData = LData()

    if arr.LFirst(lData):
        print(f"첫 번째 데이터 {lData.data}")
    else:
        print("데이터가 없습니다.")

    while arr.LNext(lData):
        if lData.data == 3:
            arr.LRemove()
            continue

        print(lData.data)
