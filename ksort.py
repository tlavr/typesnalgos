class ksort:
    def __init__(self):
        self.__len__ = 800
        self.__abc__ = "abcdefgh"
        self.items = [None] * self.__len__

    def checkline(self, line):
        if line.__len__() != 3:
            return False
        if not(line[0] in self.__abc__) or not line[1].isdigit() or not line[2].isdigit():
            return False
        return True

    def index(self, line):
        if not self.checkline(line):
            return -1
        idx = (ord(line[0]) - 97)*100 + int(line[1]) * 10 + int(line[2])
        return idx

    def add(self, line):
        if not self.checkline(line):
            return False
        self.items[self.index(line)] = line
        return True

