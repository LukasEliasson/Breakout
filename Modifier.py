from GameManager import GameManager
from Ball import Ball
from Brick import Brick
from Paddle import Paddle
import random

class Modifier:

    def __init__(self, name: str, type: str, ball_speed: int=5, paddle_size: int=50, time_remaining: int=None):
        self.x = 0
        self.y = 0
        self.name = name
        self.type = type
        self.powerup = None
        self.radius = 5
        
        #self.color = "green" if type == "positive" else "red" if type == "negative" else "yellow" if type == "special" else "grey"
        colors = ["green", "red", "yellow", "blue", "purple"]
        self.color = random.choice(colors)

        self.fall_speed = 2
        self.time_remaining = time_remaining
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

    def activate(self, game_manager: GameManager) -> None:
        if self.time_remaining:
            game_manager.active_modifiers.append(self)
        game_manager.dropped_modifiers.remove(self)

        self.set_activated_time(game_manager.tick)

        match self.name:
            case "Fast Ball":
                for ball in game_manager.balls:
                    ball.speed += 150
            case "Wide Paddle":
                game_manager.paddle.base_width += 50
            case "Extra Ball":
                # New balls will have the same speed as the first ball
                ball_speed = game_manager.balls[0].speed
                game_manager.balls.append(Ball(self.x, self.y, 0, -1, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, 0.5, -0.5, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, -0.5, -0.5, 5, "white", speed=ball_speed))
            case "Extravaganza":
                # New balls will have the same speed as the first ball
                ball_speed = game_manager.balls[0].speed
                game_manager.balls.append(Ball(self.x, self.y, 0, -1, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, 0.5, -0.5, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, -0.5, -0.5, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, -0.25, -0.75, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, 0.25, -0.75, 5, "white", speed=ball_speed))

                for ball in game_manager.balls:
                    ball.speed += 1000
                    ball.death_disabled = True
                
                self.set_activated_time(game_manager.tick)

            case "Extra Brick Row":
                # Move all bricks down 1 row (10 pixels)
                for brick in game_manager.bricks:
                    brick.y += 10

                # Create a new row of bricks at the top of the screen
                for i in range(0, game_manager.WINDOW_SIZE, 22):
                    game_manager.bricks.append(Brick(i, 20, "grey"))

        print(f'Activated self: {self.name}')

    def deactivate(self, game_manager: GameManager) -> None:
        match self.name:
            case "Fast Ball":
                for ball in game_manager.balls:
                    if ball.speed >= 450:
                        ball.speed -= 150
            case "Wide Paddle":
                game_manager.paddle.base_width -= 50
            case "Extravaganza":
                extravaganza_count = 0
                
                for mod in game_manager.active_modifiers:
                    if mod.name == "Extravaganza":
                        extravaganza_count += 1

                for ball in game_manager.balls:
                    if extravaganza_count <= 1:
                        ball.death_disabled = False
                    
                    if ball.speed >= 300 + 1000 * extravaganza_count:
                        ball.speed -= 1000

        if self in game_manager.active_modifiers:
            game_manager.active_modifiers.remove(self)

        print(f'Deactivated modifier: {self.name}')
