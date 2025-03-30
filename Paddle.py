class Paddle:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 10
        self.color = "white"

    def __str__(self):
        return "Paddle at x: " + str(self.x) + " y: " + str(self.y)
    
    def __repr__(self):
        return f'Paddle({self.x}, {self.y})'

    def move(self, direction):
        if direction == "left":
            self.x -= 5
        if direction == "right":
            self.x += 5