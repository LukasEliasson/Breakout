import pygame
from SoundManager import SoundManager
from Brick import Brick
from Paddle import Paddle
from Ball import Ball
import random
from copy import deepcopy

class GameManager:
    
    def __init__(self, modifiers, WINDOW_SIZE):
        
        self.MAX_POINTS = 100000
        self.MAX_TIME = 120
        self.MAX_BALL_SPEED = 2300
        self.WINDOW_SIZE = WINDOW_SIZE

        self.dt = 0   # Updated from the main loop
        self.paddle, self.balls = self.generate_objects()
        self.bricks = self.generate_bricks()
        self.modifiers = modifiers
        self.score = self.MAX_POINTS
        self.lives = 3
        self.game_started = False
        self.won_game = False
        self.lost_game = False
        self.tick = 0
        self.dropped_modifiers = []
        self.active_modifiers = []
        self.modifier_drop_rate = 1  # 100% chance to drop a modifier each time a brick is destroyed
        self.death_disabled = False
        self.elapsed_time = 0

        self.sound_manager = SoundManager()


    # Will update every frame
    def update(self):

        if not self.sound_manager.playing_music and self.game_started:
            self.sound_manager.start_music()

        if self.balls[0].vy != 0:
            self.elapsed_time += self.dt

        for ball in self.balls:
            ball.move(self.dt)

            if not ball.is_dead:
                ball.handle_edge_bounce(self.WINDOW_SIZE)
            else:
                self.balls.remove(ball)
                if len(self.balls) <= 0:
                    self.reset()

        # Handle dropped modifiers
        for modifier in self.dropped_modifiers[:]:

            modifier.fall()
            
            if modifier.is_out_of_bounds(self.WINDOW_SIZE):
                self.dropped_modifiers.remove(modifier)

            elif modifier.is_caught(self.paddle):
                modifier.activate(self)

        # Handle active modifiers
        for modifier in self.active_modifiers[:]:
            if modifier.time_remaining <= 0:
                modifier.deactivate(self)
            elif modifier.time_remaining > 0:
                modifier.time_remaining -= self.dt


        if self.paddle.width > self.paddle.base_width:
            self.paddle.width -= 1
            self.paddle.x += 0.5

            if self.paddle.width <= self.paddle.base_width:
                self.paddle.width = self.paddle.base_width
        
        elif self.paddle.width < self.paddle.base_width:
            self.paddle.width += 1
            self.paddle.x -= 0.5

            if self.paddle.width >= self.paddle.base_width:
                self.paddle.width = self.paddle.base_width

        for ball in self.balls:

            collision_object = ball.check_collision(self.paddle, self.bricks, self.balls)

            if collision_object:
                if isinstance(collision_object, Paddle):
                    if ball.vy > 0 or ball.vx > 0:
                        ball.paddle_hit(45, self.paddle)

                        self.sound_manager.play_paddle_hit_sound()

                elif isinstance(collision_object, Brick):
                    self.handle_brick_collision(ball, collision_object)

        # If there are no dropped modifiers, randomly drop a modifier from the top
        if len(self.dropped_modifiers) == 0 and self.game_started:
            random_num = random.randint(1, 500)
            if random_num == 1:
                modifier = deepcopy(random.choice(self.modifiers))
                modifier.x = random.randint(0 + modifier.radius * 2, self.WINDOW_SIZE - modifier.radius * 2)
                modifier.y = 0 + modifier.radius
                print(f'Dropped modifier: {modifier.name}')
                self.dropped_modifiers.append(modifier)

        # Cap ball speed
        for ball in self.balls:
            ball.speed = min(ball.speed, self.MAX_BALL_SPEED)

        self.score = self.calculate_score()
    
    def calculate_score(self):
        score = round(self.MAX_POINTS * (1 - (self.elapsed_time / self.MAX_TIME)))
        return max(0, score)
    
    def handle_brick_collision(self, ball: Ball, brick: Brick):
        brick.damage()

        self.sound_manager.play_brick_hit_sound()

        ball.bounce("y")

        if brick.is_destroyed():

            self.bricks.remove(brick)

            if len(self.bricks) == 0:
                self.win()

            random_num = random.randint(1, round(1 / self.modifier_drop_rate))

            if random_num == 1:
                modifier = deepcopy(random.choice(self.modifiers))

                if len(self.dropped_modifiers) < 5:
                    modifier.set_brick(brick)
                    modifier.move_to_brick()
                    print(f'Dropped modifier: {modifier.name}')
                    self.dropped_modifiers.append(modifier)
    
    def reset(self, restart_game=False):

        # Remove life and check for game win
        if restart_game:
            self.lost_game = False
            self.won_game = False
            self.game_started = False
            self.score = 0
            self.lives = 3
            self.tick = 0
            self.elapsed_time = 0

            self.sound_manager.start_music()

            self.bricks = self.generate_bricks()

        else:
            self.lives -= 1
            if self.lives <= 0:
                self.lose()

        # Deactivate and remove all modifiers
        for modifier in self.active_modifiers[:]:
            modifier.deactivate(self)

        self.dropped_modifiers = []

        # Regenerate objects
        self.paddle, self.balls = self.generate_objects()

        # Reset game state
        self.game_started = False

    def generate_objects(self) -> tuple[Paddle, list[Ball]]:
        paddle = Paddle(self.WINDOW_SIZE / 2 - 25, self.WINDOW_SIZE - 20)

        ball_radius = 5
        ball_starting_pos = {
            "x": self.WINDOW_SIZE / 2,
            "y": paddle.y - ball_radius,
        }

        balls = [Ball(ball_starting_pos["x"], ball_starting_pos["y"], 0, 0, 5, "white")]

        return paddle, balls
    
    def generate_bricks(self) -> list[Brick]:
        bricks = []
        colors = ["red", "red", "orange", "orange", "green", "green", "yellow", "yellow"]

        for x in range(0, self.WINDOW_SIZE, 22):
            for y in range(20, 90, 10):
                color_index = int(y / 10 - 1)
                color = colors[color_index]
                bricks.append(Brick(x, y, color))

        return bricks

    def win(self):
        self.game_started = False
        self.won_game = True
        self.sound_manager.stop_music()

    def lose(self):
        self.game_started = False
        self.lost_game = True
        self.sound_manager.stop_music()
