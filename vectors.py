import math

def dcos(direction):
    return math.cos(math.radians(direction))

def dsin(direction):
    return math.sin(math.radians(direction))

def lerp(v0, v1, t):
    return v0 + t * (v1 - v0)

def dot(a, b):
    return a.x * b.x + a.y * b.y

def reflect(incident, normal):
    perp = 2.0 * dot(incident, normal)
    return incident - normal * perp

class tor2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def clone(self):
        return tor2(self.x, self.y)

    def __neg__(self):
        return tor2(-self.x, -self.y)

    def __add__(self, other):
        return tor2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return tor2(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):
        if other is tor2: return tor2(self.x / other.x, self.y / other.y)
        return tor2(self.x / other, self.y / other)

    def __mul__(self, other):
        if other is tor2: return tor2(self.x * other.x, self.y * other.y)
        return tor2(self.x * other, self.y * other)

    def nor(self):
        length = self.len()
        return tor2(self.x / length, self.y / length)

    def nor_with(self, other):
        return (self - other).nor()

    def len(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def len_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def lerp(self, other, alpha):
        return tor2(lerp(self.x, other.x, alpha), lerp(self.y, other.y, alpha))


class tor3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def clone(self):
        return tor3(self.x, self.y, self.z)

    def __neg__(self):
        return tor3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return tor3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return tor3(self.x - other.x, self.y - other.y, self.z + other.z)

    def __truediv__(self, other):
        if other is tor3:
            return tor3(self.x / other.x, self.y / other.y, self.z / other.z)
        return tor3(self.x / other, self.y / other, self.z / other)

    def __mul__(self, other):
        if other is tor3:
            return tor3(self.x * other.x, self.y * other.y, self.z * other.z)
        return tor3(self.x * other, self.y * other, self.y * other)

    def nor(self):
        length = self.len()
        return tor3(self.x / length, self.y / length, self.z / length)

    def nor_with(self, other):
        return (self - other).nor()

    def len(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def len_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def lerp(self, other, alpha):
        return tor3(lerp(self.x, other.x, alpha), lerp(self.y, other.y, alpha), lerp(self.z, other.z, alpha))
