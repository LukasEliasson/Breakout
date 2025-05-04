class Brick:

    def __init__(self, x, y, color, width=437/22, height=7, durability=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.durability = durability
        self.hits = 0

    def __str__(self):
        return "Brick at x: " + str(self.x) + " y: " + str(self.y)
    
    def __repr__(self):
        return f'Brick({self.x}, {self.y}, {self.color}, {self.width}, {self.height})'
    
    def damage(self):
        self.hits += 1

    def is_destroyed(self):
        return self.hits >= self.durability