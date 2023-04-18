class CircleList(list):
    def __iter__(self):
        self.num = 0
        return self

    def __next__(self):
        if(self.num >= len(self)):
            self.num = 0
        self.num += 1
        return self[self.num-1]