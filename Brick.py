class Brick:

    def __init__(self, x, y, color, width=20, height=5, durability=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.durability = durability

    def __str__(self):
        return "Brick at x: " + str(self.x) + " y: " + str(self.y)
    
    def __repr__(self):
        return f'Brick({self.x}, {self.y}, {self.color}, {self.width}, {self.height})'
    
    def damage(self):
        self.durability -= 1

    def is_destroyed(self):
        return self.durability <= 0