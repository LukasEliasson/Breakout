import pygame
from SoundManager import SoundManager
from LevelManager import LevelManager
from Brick import Brick
from Paddle import Paddle
from Ball import Ball
import random
from copy import deepcopy

class GameManager:
    
    def __init__(self, modifiers, WINDOW_SIZE):
        
        self.MAX_POINTS = 100000
        self.MAX_BALL_SPEED = 1500
        self.WINDOW_SIZE = WINDOW_SIZE

        self.dt = 0.02   # Updated from the main loop
        self.modifiers = modifiers
        self.level_points = self.MAX_POINTS
        self.total_points = 0
        self.lives = 3
        self.game_started = False
        self.won_game = False
        self.lost_game = False
        self.tick = 0
        self.dropped_modifiers = []
        self.active_modifiers = []
        self.modifier_drop_rate = 0.2  # 20% chance to drop a modifier each time a brick is destroyed
        self.death_disabled = False
        self.elapsed_time = 0
        self.name_entered = False

        self.sound_manager = SoundManager()
        self.level_manager = LevelManager()
        
        self.paddle, self.balls = self.generate_objects()
        self.bricks = self.generate_bricks()

    # Will update every frame
    def update(self):

        # Start music if not already playing and game has started.
        if not self.sound_manager.playing_music and self.game_started:
            self.sound_manager.start_music()

        # Increase elapsed time. The first ball is used to check if the game has started.
        if self.game_started:
            self.elapsed_time += self.dt
            self.level_manager.time_spent += self.dt

        # Update position of balls
        self.update_balls()

        # Handle dropped modifiers
        self.update_dropped_modifiers()

        # Handle active modifiers
        self.update_active_modifiers()

        # Update paddle width if it is shrinking or growing
        self.update_paddle_width()

        # Handle ball collisions
        self.handle_ball_collisions()

        # If there are no dropped modifiers, randomly drop a modifier from the top
        if len(self.dropped_modifiers) == 0 and self.game_started:
            random_num = random.randint(1, 500)
            if random_num == 1:
                self.drop_random_modifier()

        # Cap ball speed
        for ball in self.balls:
            ball.speed = min(ball.speed, self.MAX_BALL_SPEED)

        self.level_points = self.calculate_score()

    def update_balls(self):

        # A copy of self.balls is used (by adding [:] at the end) to avoid modifying the list while iterating over it
        for ball in self.balls[:]:

            # Update ball position
            ball.move(self.dt)

            if ball.is_dead:
                # If the ball is dead, remove it from the game
                self.balls.remove(ball)

                # If all balls are dead, reset the game
                if len(self.balls) <= 0:
                    self.reset()

            else:
                # Handle collisions with edges
                ball.handle_edge_bounce(self.WINDOW_SIZE)     

    def update_dropped_modifiers(self):
        # A copy of self.dropped_modifiers is used (by adding [:] at the end) to avoid modifying the list while iterating over it
        for modifier in self.dropped_modifiers[:]:

            # Update modifier position
            modifier.fall(self.dt)
            
            # If the modifier is out of bounds, remove it from the game
            if modifier.is_out_of_bounds(self.WINDOW_SIZE):
                self.dropped_modifiers.remove(modifier)

            # If the modifier is caught by the paddle, activate it
            elif modifier.is_caught(self.paddle):
                modifier.activate(self)

    def update_active_modifiers(self):
        # A copy of self.active_modifiers is used (by adding [:] at the end) to avoid modifying the list while iterating over it
        for modifier in self.active_modifiers[:]:

            # If the time remaining of the modifier is less than or equal to 0, deactivate it
            if modifier.time_remaining <= 0:
                modifier.deactivate(self)

            # If the modifier is still active, update its time remaining
            else:
                modifier.time_remaining -= self.dt

    def update_paddle_width(self):
        if self.paddle.width > self.paddle.base_width:
            self.paddle.width -= 60 * self.dt
            self.paddle.x += 30 * self.dt

            if self.paddle.width <= self.paddle.base_width:
                self.paddle.width = self.paddle.base_width
        
        elif self.paddle.width < self.paddle.base_width:
            self.paddle.width += 60 * self.dt
            self.paddle.x -= 30 * self.dt

            if self.paddle.width >= self.paddle.base_width:
                self.paddle.width = self.paddle.base_width

    def handle_ball_collisions(self):
        for ball in self.balls:

            collision_object = ball.check_collision(self.paddle, self.bricks, self.balls)

            if collision_object:
                if isinstance(collision_object, Paddle):
                    if ball.vy > 0 or ball.vx > 0:
                        ball.paddle_hit(45, self.paddle)

                        self.sound_manager.play_paddle_hit_sound()

                elif isinstance(collision_object, Brick):
                    self.handle_brick_collision(ball, collision_object)

    def drop_random_modifier(self):
        modifier = deepcopy(random.choice(self.modifiers))
        modifier.x = random.randint(0 + modifier.radius * 2, self.WINDOW_SIZE - modifier.radius * 2)
        modifier.y = 0 + modifier.radius
        print(f'Dropped modifier: {modifier.name}')
        self.dropped_modifiers.append(modifier)

    def calculate_score(self):
        # Calculate score based on elapsed time, maximum time, and maximum points
        # The score decreases as time elapsed increases
        score = round(self.MAX_POINTS * (1 - (self.level_manager.time_spent / self.level_manager.max_time)))
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
    
    def reset(self, new_level: bool = False, restart_game: bool = False) -> None:

        # Reset game state depending on if the game is restarting or a new level is starting
        if restart_game or new_level:

            # Reset game state
            if restart_game:
                self.lost_game = False
                self.won_game = False
                self.lives = 3
                self.tick = 0
                self.elapsed_time = 0
                self.level_manager.reset()
                self.total_points = 0

            # Reset level state
            self.game_started = False
            self.name_entered = False

            # Start music again
            self.sound_manager.start_music()

        else:
            # Remove one life and check for game over
            self.lives -= 1
            if self.lives <= 0:
                self.lose()
                return

        # Deactivate and remove all modifiers
        for modifier in self.active_modifiers[:]:
            modifier.deactivate(self)
            
        self.dropped_modifiers = []
        
        # Regenerate objects
        self.paddle, self.balls = self.generate_objects()

        # If the game is restarting or there is a new level, regenerate bricks
        if restart_game or new_level:
            self.bricks = self.generate_bricks()

        # Reset game state
        self.game_started = False

    def generate_objects(self) -> tuple[Paddle, list[Ball]]:
        paddle = Paddle(self.WINDOW_SIZE / 2 - 25, self.WINDOW_SIZE - 20)

        ball_radius = 5
        ball_starting_pos = {
            "x": self.WINDOW_SIZE / 2,
            "y": paddle.y - ball_radius,
        }

        balls = [Ball(ball_starting_pos["x"], ball_starting_pos["y"], 0, 0, 5, "white", speed=self.level_manager.ball_speed)]

        return paddle, balls
    
    def generate_bricks(self) -> list[Brick]:
        bricks = []
        colors = ["red", "red", "orange", "orange", "green", "green", "yellow", "yellow"]

        for x in range(0, self.WINDOW_SIZE, 22):
            for y in range(20, 90, 10):
                color_index = int(y / 10 - 1)
                color = colors[color_index]
                bricks.append(Brick(x, y, color, durability=1*self.level_manager.hit_multiplier))

        return bricks

    def win(self):
        self.game_started = False
        self.won_game = True
        self.total_points += self.level_points
        self.level_manager.increase_level()
        self.sound_manager.stop_music()
        self.reset(new_level=True)

    def lose(self):
        self.game_started = False
        self.lost_game = True
        self.sound_manager.stop_music()
