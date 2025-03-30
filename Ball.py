import math
from Paddle import Paddle
from Brick import Brick

class Ball:

    def __init__(self, x: int, y: int, vx: int, vy: int, radius: int, color: str):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.speed = 5

    def move(self) -> None:
        self.x += self.vx
        self.y += self.vy

    def check_collision(self, paddle: Paddle, bricks: list[Brick]) -> str | None:
        if (self.x + self.radius >= paddle.x and self.x - self.radius <= paddle.x + paddle.width and
                self.y + self.radius >= paddle.y and self.y - self.radius <= paddle.y + paddle.height):
            return paddle
        
        for brick in bricks:
            if (self.x + self.radius >= brick.x and self.x - self.radius <= brick.x + brick.width and
                    self.y + self.radius >= brick.y and self.y - self.radius <= brick.y + brick.height):
                return brick
            
        return None
    
    def bounce(self, direction: str) -> None:
        if direction == "y":
            self.vy = -self.vy
        elif direction == "x":
            self.vx = -self.vx
        elif direction == "xy":
            self.vx = -self.vx
            self.vy = -self.vy

    def paddle_hit(self, max_angle: int, paddle_position: float) -> None:
        angle = max_angle * paddle_position

        angle_rad = math.radians(angle)

        self.vx = self.speed * math.cos(angle_rad)
        self.vy = self.speed * math.sin(angle_rad)

    def begin(self):
        self.vx = 0
        self.vy = -self.speed