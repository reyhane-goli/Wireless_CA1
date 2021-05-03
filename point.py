import math

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getReal(self):
        return self.x
    
    def getImaginary(self):
        return self.y
    
    def multiply(self, u, v):
        self.x = self.x * u - self.y * v
        self.y = self.x * v + self.y * u
    
    def add(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy

    def findNearest(self, others):
        min = float("inf")
        index = -1
        for i in range(0, len(others)):
            other = others[i]
            dx = self.x - other.x
            dy = self.y - other.y
            val = math.sqrt(dx**2 + dy**2)
            if(val < min):
                min = val
                index = i
        return index