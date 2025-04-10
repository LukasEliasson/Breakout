import pygame
from Brick import Brick
from Paddle import Paddle
from Ball import Ball
from Modifier import Modifier
import random
from copy import deepcopy

class Main:
    
    def __init__(self):

        self.window_size = 500
        self.canvas = None
        self.exit = False
        self.bricks = []
        self.paddle = None
        self.balls = []
        self.lives = 3
        self.score = 0
        self.game_started = False
        self.won_game = False
        self.lost_game = False
        self.tick = 0
        self.modifiers = []
        self.dropped_modifiers = []
        self.active_modifiers = []
        self.modifier_drop_rate = 1  # 100% chance to drop a modifier each time a brick is destroyed
 
    def start_music(self):
        pygame.mixer.music.load('sfx/atari_st_beat.mp3')
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.play(-1, 0.0)

    # Will initialise the beginning of the game, create all essential objects etc.
    def setup(self):

        self.generate_bricks()
        self.generate_objects()
        
        # Initialise modifiers
        self.modifiers.append(Modifier("Fast Ball", "negative", duration=5))
        self.modifiers.append(Modifier("Wide Paddle", "positive", duration=8))
        self.modifiers.append(Modifier("Extra Ball", "positive", duration=None))

        pygame.mixer.init()
        self.start_music()

        self.update()

    # Will redraw the screen each frame
    def update(self):
        if self.lost_game or self.won_game:
            self.display_endscreen()
            return

        self.canvas.fill((0, 0, 0))

        for ball in self.balls:
            ball.move()

            if not ball.is_dead:
                ball.handle_edge_bounce(self.window_size)
            else:
                self.balls.remove(ball)
                if len(self.balls) <= 0:
                    self.reset()

        # Handle dropped modifiers
        for modifier in self.dropped_modifiers[:]:

            modifier.fall()
            
            if modifier.is_out_of_bounds(self.window_size):
                self.dropped_modifiers.remove(modifier)

            elif modifier.is_caught(self.paddle):
                self.activate_modifier(modifier)

        for modifier in self.active_modifiers[:]:
            if modifier.duration and self.tick >= (modifier.activated_at + modifier.duration):
                self.deactivate_modifier(modifier)

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

                        paddle_hit_sound = pygame.mixer.Sound('sfx/paddle_hit.wav')
                        paddle_hit_sound.play()

                elif isinstance(collision_object, Brick):
                    self.handle_brick_collision(ball, collision_object)

                elif isinstance(collision_object, Ball):
                    pass
                    #if self.tick - 60 >= ball.spawned_at:
                    #    print(f'Ball collision: {self.tick - 60} > {ball.spawned_at}')
                    #    # Bounce off the other ball, the other ball will also bounce off this ball when it gets to it in the loop.
                    #    ball.bounce('xy')


        # If there are no dropped modifiers, randomly drop a modifier from the top
        if len(self.dropped_modifiers) == 0 and self.game_started:
            random_num = random.randint(1, 500)
            if random_num == 1:
                modifier = deepcopy(random.choice(self.modifiers))
                modifier.x = random.randint(0 + modifier.radius * 2, self.window_size - modifier.radius * 2)
                modifier.y = 0 + modifier.radius
                print(f'Dropped modifier: {modifier.name}')
                self.dropped_modifiers.append(modifier)

        self.draw()

    def handle_brick_collision(self, ball: Ball, brick: Brick):
        brick.damage()

        brick_hit_sound = pygame.mixer.Sound('sfx/brick_hit.wav')
        brick_hit_sound.play()

        ball.bounce("y")

        if brick.is_destroyed():

            self.score += 1
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

    def draw(self):
        for brick in self.bricks:
            pygame.draw.rect(self.canvas, brick.color, pygame.Rect(brick.x, brick.y, brick.width, brick.height))

        # Info text
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(f'Lives: {self.lives}. Score: {self.score}', True, "white")
        text_rect = text.get_rect()
        text_rect.center = (55, 10)
        self.canvas.blit(text, text_rect)

        pygame.draw.rect(self.canvas, "white", pygame.Rect(self.paddle.x, self.paddle.y, self.paddle.width, self.paddle.height))

        for ball in self.balls:
            pygame.draw.circle(self.canvas, "white", ball.pos, ball.radius)
        
        for modifier in self.dropped_modifiers:
            pygame.draw.circle(self.canvas, modifier.color, (modifier.x, modifier.y), modifier.radius)

        pygame.display.flip()

    def generate_bricks(self):
        self.bricks = []
        colors = ["red", "red", "orange", "orange", "green", "green", "yellow", "yellow"]

        for x in range(0, self.window_size, 22):
            for y in range(10, 90, 10):
                color_index = int(y / 10 - 1)
                print(color_index)
                color = colors[color_index]
                print(color)
                self.bricks.append(Brick(x, y, color))

    def main(self):
 
        clock = pygame.time.Clock()
        pygame.init()
 
        # CREATE A self.canvas
        self.canvas = pygame.display.set_mode((self.window_size, self.window_size))
 
        # TITLE OF self.canvas
        pygame.display.set_caption("Breakout")
 
        # SETUP GAME OBJECTS
        self.setup()
 
        # GAME LOOP
        while not self.exit:
            self.update()
 
            self.handle_events()
 
            pygame.display.update()
            dt = clock.tick(60) / 1000
            
            if self.game_started:
                self.tick += 1
                for ball in self.balls:
                    ball.speed += self.tick / 6000000

    # Runs every frame. What will happen each frame
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
 
        keys = pygame.key.get_pressed()
 
        self.react_to_user_input(keys)

    def generate_objects(self):
        self.paddle = Paddle(self.window_size / 2 - 25, self.window_size - 20)

        ball_radius = 5
        ball_starting_pos = {
            "x": self.window_size / 2,
            "y": self.paddle.y - ball_radius,
        }

        self.balls.append(Ball(ball_starting_pos["x"], ball_starting_pos["y"], 0, 0, 5, "white", self.tick))

    def activate_modifier(self, modifier: Modifier):

        if modifier.duration:
            self.active_modifiers.append(modifier)
        self.dropped_modifiers.remove(modifier)

        modifier.set_activated_time(self.tick)

        match modifier.name:
            case "Fast Ball":
                for ball in self.balls:
                    ball.speed += 3
            case "Wide Paddle":
                self.paddle.base_width += 50
            case "Extra Ball":
                self.balls.append(Ball(modifier.x, modifier.y, 0, -1, 5, "white", self.tick))
                self.balls.append(Ball(modifier.x, modifier.y, 0.5, -0.5, 5, "white", self.tick))
                self.balls.append(Ball(modifier.x, modifier.y, -0.5, -0.5, 5, "white", self.tick))

        print(f'Activated modifier: {modifier.name}')

    def deactivate_modifier(self, modifier: Modifier):
        match modifier.name:
            case "Fast Ball":
                print('Deactivated modifier: Fast Ball')
                for ball in self.balls:
                    if ball.speed >= 8:
                        ball.speed -= 3
            case "Wide Paddle":
                print('Deactivated modifier: Wide Paddle')
                self.paddle.base_width -= 50

        self.active_modifiers.remove(modifier)

    def reset(self, restart_game=False):

        # Remove life and check for game win
        if restart_game:
            self.lost_game = False
            self.won_game = False
            self.game_started = False
            self.score = 0
            self.lives = 3
            self.tick = 0

            self.start_music()

            self.generate_bricks()

        else:
            self.lives -= 1
            if self.lives <= 0:
                self.lose()

        # Deactivate and remove all modifiers
        for modifier in self.active_modifiers[:]:
            self.deactivate_modifier(modifier)

        self.dropped_modifiers = []
        self.balls = []

        # Regenerate objects
        self.generate_objects()

        # Reset game state
        self.game_started = False
        
    def display_endscreen(self):
        pygame.mixer.music.stop()

        self.canvas.fill('black')
        font = pygame.font.Font('freesansbold.ttf', 30)
        small_font = pygame.font.Font('freesansbold.ttf', 15)

        text = None
        text_rect = None

        if self.lost_game:
            text = font.render(f'Game Over. Score: {self.score}', True, 'red')
        else:
            text = font.render(f'You win! Score: {self.score}', True, 'green')

        text_rect = text.get_rect()
        text_rect.center = (self.window_size / 2, self.window_size / 2)

        restart_text = small_font.render('Press Space to restart', True, 'white')
        restart_text_rect = restart_text.get_rect()
        restart_text_rect.center = (self.window_size / 2, self.window_size / 2 + 35)

        self.canvas.blit(text, text_rect)
        self.canvas.blit(restart_text, restart_text_rect)
        pygame.display.flip()

    def win(self):
        self.game_started = False
        self.won_game = True
        self.display_endscreen()

    def lose(self):
        self.game_started = False
        self.lost_game = True
        self.display_endscreen()
 
    def react_to_user_input(self, keysPressed):
        paddle_left_edge = self.paddle.x
        paddle_right_edge = self.paddle.x + self.paddle.width

        if keysPressed[pygame.K_a] or keysPressed[pygame.K_LEFT]:
            if self.game_started:
                if paddle_left_edge > 0:
                    self.paddle.move('left')

        if keysPressed[pygame.K_d] or keysPressed[pygame.K_RIGHT]:
            if self.game_started:
                if paddle_right_edge < self.window_size:
                    self.paddle.move('right')

        if keysPressed[pygame.K_w] or keysPressed[pygame.K_UP]:
            if not self.game_started:
                self.balls[0].begin()
                self.game_started = True

        if keysPressed[pygame.K_SPACE]:
            self.reset(restart_game=True)
 
 
 
main = Main()
 
main.main()