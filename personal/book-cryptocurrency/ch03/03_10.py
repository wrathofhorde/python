class Parent:
    def sing(self):
        print("sing a song")

class LuckyChild(Parent):
    def dance(self):
        print("shuffle dance")

luckyboy = LuckyChild()
luckyboy.sing()
luckyboy.dance()