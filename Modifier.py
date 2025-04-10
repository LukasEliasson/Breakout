from Brick import Brick
from Paddle import Paddle

class Modifier:

    def __init__(self, name: str, type: str, ball_speed: int=5, paddle_size: int=50, duration: int=None):
        self.x = 0
        self.y = 0
        self.name = name
        self.type = type
        self.powerup = None
        self.radius = 5
        self.color = "green" if type == "positive" else "red" if type == "negative" else "yellow" if type == "special" else "grey"
        self.fall_speed = 2
        self.duration = None if duration is None else duration * 60
        self.activated_at = None
        self.deactivated_at = None
        self.is_active = False
        self.brick = None

    def set_brick(self, brick: Brick) -> None:
        self.x = brick.x
        self.y = brick.y
        self.brick = brick

    def move_to_brick(self) -> None:
        self.x = self.brick.x + self.brick.width / 2
        self.y = self.brick.y + self.brick.height

    def fall(self) -> None:
        self.y += self.fall_speed

    def is_caught(self, paddle: Paddle) -> bool:
        if (self.x + self.radius >= paddle.x and self.x - self.radius <= paddle.x + paddle.width and
                self.y + self.radius >= paddle.y and self.y - self.radius <= paddle.y + paddle.height):
            return True
        return False
    
    def is_out_of_bounds(self, window_size: int) -> bool:
        return (self.y - self.radius) > window_size
    
    def set_activated_time(self, time: int) -> None:
        self.activated_at = time

    def set_deactivated_time(self, time: int) -> None:
        self.deactivated_at = time 

    def set_duration(self, duration: int) -> None:
        # Convert duration to ms
        duration *= 1000

        self.duration = duration