import pygame
from GameManager import GameManager
from Brick import Brick
from Paddle import Paddle
from Ball import Ball
from Modifier import Modifier
from datetime import timedelta
from collections import defaultdict
import math

class Main:
    
    def __init__(self):

        self.game_manager = None   # Initialises in setup method.
        self.window_size = 500
        self.canvas = None
        self.exit = False

    # Will initialise the beginning of the game, create all essential objects etc.
    def setup(self):

        # Initialise modifiers
        modifiers = []
        modifiers.append(Modifier("Fast Ball", "negative", time_remaining=5))
        modifiers.append(Modifier("Wide Paddle", "positive", time_remaining=10))
        modifiers.append(Modifier("Extra Ball", "positive"))
        modifiers.append(Modifier("Extravaganza", "special", time_remaining=5))
        modifiers.append(Modifier("Extra Brick Row", "negative"))

        self.game_manager = GameManager(modifiers, self.window_size)
        self.game_manager.generate_bricks()
        self.game_manager.generate_objects()

        self.game_manager.update()
        self.draw()

    def draw(self):
        self.canvas.fill((0, 0, 0))

        for brick in self.game_manager.bricks:
            pygame.draw.rect(self.canvas, brick.color, pygame.Rect(brick.x, brick.y, brick.width, brick.height))

        # Info text
        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(f'Lives: {self.game_manager.lives}', True, "white")
        text_rect = text.get_rect()
        text_rect.center = (30, 10)
        self.canvas.blit(text, text_rect)

        formatted_time = str(timedelta(seconds=math.floor(self.game_manager.elapsed_time))).removeprefix('0:')
        timer = font.render(f'{formatted_time}', True, "white")
        timer_rect = timer.get_rect()
        timer_rect.center = (self.window_size - 25, 10)
        self.canvas.blit(timer, timer_rect)

        score_text = font.render(str(self.game_manager.score), True, "white")
        score_rect = score_text.get_rect()
        score_rect.center = (self.window_size / 2, 10)
        self.canvas.blit(score_text, score_rect)

        # Modifier info
        modifier_counts = defaultdict(list)
        for modifier in self.game_manager.active_modifiers:
            modifier_counts[modifier.name].append(modifier)

        for i, (name, modifiers) in enumerate(modifier_counts.items()):
            count = len(modifiers)
            time_remaining = min(mod.time_remaining for mod in modifiers)

            display_name = f'{name} (x{count})' if count > 1 else name
            modifier_text = font.render(f'{display_name}: {time_remaining:.1f}s', True, "white")
            modifier_rect = modifier_text.get_rect()
            modifier_rect.bottomleft = (10, 150 + i * 15)
            self.canvas.blit(modifier_text, modifier_rect)

        pygame.draw.rect(self.canvas, "white", pygame.Rect(self.game_manager.paddle.x, self.game_manager.paddle.y, self.game_manager.paddle.width, self.game_manager.paddle.height))

        for ball in self.game_manager.balls:
            pygame.draw.circle(self.canvas, "white", ball.pos, ball.radius)
        
        for modifier in self.game_manager.dropped_modifiers:
            pygame.draw.circle(self.canvas, modifier.color, (modifier.x, modifier.y), modifier.radius)

        pygame.display.flip()

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
            if self.game_manager.lost_game or self.game_manager.won_game:
                self.display_endscreen()
                self.handle_events()
                continue
            
            self.game_manager.update()
            self.draw()
            self.handle_events()

            pygame.display.update()
            self.game_manager.dt = clock.tick(60) / 1000
            
            if self.game_manager.game_started:
                self.game_manager.tick += 1

    # Runs every frame. What will happen each frame
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
 
        keys = pygame.key.get_pressed()
 
        self.react_to_user_input(keys)
        
    def display_endscreen(self):
        pygame.mixer.music.stop()

        self.canvas.fill('black')
        font = pygame.font.Font('freesansbold.ttf', 30)
        small_font = pygame.font.Font('freesansbold.ttf', 15)

        text = None
        text_rect = None

        if self.game_manager.lost_game:
            text = font.render(f'Game Over.', True, 'red')
        else:
            text = font.render(f'You win! Score: {self.game_manager.score}', True, 'green')

        text_rect = text.get_rect()
        text_rect.center = (self.window_size / 2, self.window_size / 2)

        restart_text = small_font.render('Press Space to restart', True, 'white')
        restart_text_rect = restart_text.get_rect()
        restart_text_rect.center = (self.window_size / 2, self.window_size / 2 + 35)

        self.canvas.blit(text, text_rect)
        self.canvas.blit(restart_text, restart_text_rect)
        pygame.display.flip()
 
    def react_to_user_input(self, keysPressed):
        paddle_left_edge = self.game_manager.paddle.x
        paddle_right_edge = self.game_manager.paddle.x + self.game_manager.paddle.width

        if keysPressed[pygame.K_a] or keysPressed[pygame.K_LEFT]:
            if self.game_manager.game_started:
                if paddle_left_edge > 0:
                    self.game_manager.paddle.move('left', self.game_manager.dt)

        if keysPressed[pygame.K_d] or keysPressed[pygame.K_RIGHT]:
            if self.game_manager.game_started:
                if paddle_right_edge < self.window_size:
                    self.game_manager.paddle.move('right', self.game_manager.dt)

        if keysPressed[pygame.K_w] or keysPressed[pygame.K_UP]:
            if not self.game_manager.game_started:
                self.game_manager.balls[0].begin()
                self.game_manager.game_started = True

        if keysPressed[pygame.K_SPACE]:
            self.game_manager.reset(restart_game=True)
 
 
 
main = Main()
 
main.main()