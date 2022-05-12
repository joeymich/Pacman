from constants import TILE_SIZE

class Vec2():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.threshold = 0.00001

    def __add__(self, v2):
        return Vec2(self.x + v2.x, self.y + v2.y)

    def __iadd__(self, v2):
        return self.__add__(v2)

    def __sub__(self, v2):
        return Vec2(self.x - v2.x, self.y - v2.y)

    def __isub__(self, v2):
        return self.__sub__(v2)

    def __mul__(self, s):
        return Vec2(self.x * s, self.y * s)
        
    def __imul__(self, s):
        return self.__mul__(s)

    def __truediv__(self, s):
        return Vec2(self.x / s, self.y / 2)

    def __itruediv__(self, s):
        return self.__truediv__(s)

    def __eq__(self, v2):
        if abs(self.x - v2.x) < self.threshold and abs(self.y - v2.y) < self.threshold:
            return True
        return False

    def equals(self, v2, threshold):
        if abs(self.x - v2.x) < threshold and abs(self.y - v2.y) < threshold:
            return True
        return False

    def __ne__(self, v2):
        return not self.__eq__(v2)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

    def magnitude_squared(self):
        return self.x ** 2 + self.y ** 2

    def as_tuple(self):
        return self.x, self.y

    def as_ints(self):
        return int(self.x), int(self.y)

    def tile_to_pixels(self):
        return Vec2(self.x * TILE_SIZE - TILE_SIZE / 2, self.y * TILE_SIZE - TILE_SIZE / 2)

    def tile_to_pixels_tuple(self):
        return self.x * TILE_SIZE - TILE_SIZE / 2, self.y * TILE_SIZE - TILE_SIZE / 2