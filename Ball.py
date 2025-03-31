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

    def paddle_hit(self, max_angle: int, paddle: Paddle) -> None:
        paddle_midpoint = paddle.x + paddle.width / 2
        paddle_position = (self.x - paddle_midpoint) / (paddle.width / 2)

        print(f'Ball position: {self.x}, Paddle midpoint: {paddle_midpoint}, Paddle position: {paddle_position}')

        angle = 90 - max_angle * paddle_position

        print(f'Paddle position: {paddle_position}, Angle: {angle}')

        angle_rad = math.radians(angle)

        if angle == 0:
            self.vx = 0
            self.vy = -self.speed
        else:
            self.vx = self.speed * math.cos(angle_rad)
            self.vy = self.speed * math.sin(angle_rad)

            if self.vy > 0:
                self.vy = -self.vy
            
            if self.vx > 0 and angle < 0:
                self.vx = -self.vx

        print(f'Angle: {angle} degrees, vx: {self.vx}, vy: {self.vy}')
        print('-----------')

    def begin(self):
        self.vx = 0
        self.vy = -self.speed