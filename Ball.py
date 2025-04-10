import math
from pygame import Vector2
from Paddle import Paddle
from Brick import Brick

class Ball:

    def __init__(self, x: int, y: int, vx: int, vy: int, radius: int, color: str):
        self.x = x
        self.y = y
        self.pos = Vector2(self.x, self.y)
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.speed = 5
        self.is_dead = False

    def move(self) -> None:
        self.x += self.speed * self.vx
        self.y += self.speed * self.vy
        self.pos = Vector2(self.x, self.y)

    def check_collision(self, paddle: Paddle, bricks: list[Brick]) -> Paddle | Brick | None:
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

    def handle_edge_bounce(self, window_size: int) -> None:
        ball_left_edge = self.x - self.radius
        ball_right_edge = self.x + self.radius
        ball_top_edge = self.y - self.radius
        ball_bottom_edge = self.y + self.radius

        if (ball_left_edge <= 0 or ball_right_edge >= window_size) and (self.y > window_size):
            self.bounce('xy')
        elif ball_left_edge <= 0 or ball_right_edge >= window_size:
            self.bounce('x')
        elif ball_top_edge <= 0:
            self.bounce('y')
        elif ball_top_edge >= window_size:
            self.is_dead = True

        # Check if the ball has escaped the screen
        if ball_bottom_edge < 0 or ball_right_edge < 0 or ball_left_edge > window_size:
            self.x = window_size / 2
            self.y = window_size / 2

    def paddle_hit(self, max_angle: int, paddle: Paddle) -> None:
        paddle_midpoint = paddle.x + paddle.width / 2
        paddle_position = (self.x - paddle_midpoint) / (paddle.width / 2)

        angle = 90 - max_angle * paddle_position

        angle_rad = math.radians(angle)

        if angle == 0:
            self.vx = 0
            self.vy = -self.speed
        else:
            self.vx = math.cos(angle_rad)
            self.vy = math.sin(angle_rad)

            if self.vy > 0:
                self.vy = -self.vy
            
            if self.vx > 0 and angle < 0:
                self.vx = -self.vx

    def begin(self):
        self.vx = 0
        self.vy = -1