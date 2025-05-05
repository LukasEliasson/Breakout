import pygame
from GameManager import GameManager
from Brick import Brick
from Paddle import Paddle
from Ball import Ball
from Modifier import Modifier
from datetime import timedelta
from collections import defaultdict
import math
from pathlib import Path
import json

# Get highscores.json file path.
HIGHSCORES_PATH = Path(__file__).resolve().parent / "highscores.json"

class Main:
    
    def __init__(self):

        self.game_manager = None   # Initialises in setup method.
        self.window_size = 500
        self.canvas = None
        self.exit = False
        self.fps_list = []

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

        # Draw game elements (Bricks, paddle, balls, etc.)
        self.draw_game_elements()

        # Draw UI text at the top of the screen
        self.draw_ui()

        # Draw modifier information
        self.draw_modifier_info()

        # Draw big level text if new level is reached
        if self.game_manager.level_manager.time_spent == 0:
            self.draw_level_text()

        pygame.display.flip()

    def draw_ui(self):
        font = pygame.font.Font('freesansbold.ttf', 12)

        # Draw top right info
        level_text = font.render(f'Level: {self.game_manager.level_manager.current_level}', True, "white")
        level_rect = level_text.get_rect()
        level_rect.topleft = (5, 4)
        lives_text = font.render(f'Lives: {self.game_manager.lives}', True, "white")
        lives_rect = lives_text.get_rect()
        lives_rect.center = (self.window_size / 4, 10)
        self.canvas.blit(lives_text, lives_rect)
        self.canvas.blit(level_text, level_rect)

        # Calculate FPS using average from last 30 frames
        self.fps_list.append(1 / self.game_manager.dt)
        if len(self.fps_list) > 30:
            self.fps_list.pop(0)
        fps = round(sum(self.fps_list) / len(self.fps_list), 1)

        # Draw info
        formatted_time = str(timedelta(seconds=math.floor(self.game_manager.elapsed_time))).removeprefix('0:')
        fps_text = font.render(f'FPS: {fps}', True, "white")
        fps_rect = fps_text.get_rect()
        fps_rect.center = (self.window_size / 4 * 3, 10)
        timer = font.render(f'{formatted_time}', True, "white")
        timer_rect = timer.get_rect()
        timer_rect.topright = (self.window_size - 5, 4)
        self.canvas.blit(timer, timer_rect)
        self.canvas.blit(fps_text, fps_rect)

        # Draw score info
        score_text = font.render(str(self.game_manager.level_points + self.game_manager.total_points), True, "white")
        score_rect = score_text.get_rect()
        score_rect.center = (self.window_size / 2, 10)
        self.canvas.blit(score_text, score_rect)

    def draw_level_text(self):
        # Big level text
        font = pygame.font.Font('freesansbold.ttf', 50)
        level_text = font.render(f'Level {self.game_manager.level_manager.current_level}', True, "white")
        level_rect = level_text.get_rect()
        level_rect.center = (self.window_size / 2, self.window_size / 2)
        self.canvas.blit(level_text, level_rect)

        # Small text below
        small_font = pygame.font.Font('freesansbold.ttf', 15)
        small_text = small_font.render('Press up to start', True, "white")
        small_rect = small_text.get_rect()
        small_rect.center = (self.window_size / 2, self.window_size / 2 + 40)
        self.canvas.blit(small_text, small_rect)

    def draw_modifier_info(self):
        font = pygame.font.Font('freesansbold.ttf', 12)

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

    def draw_game_elements(self):

        # Draw bricks
        self.draw_bricks()

        # Draw paddle
        self.draw_paddle()

        # Draw balls
        self.draw_balls()

        # Draw dropped modifiers
        self.draw_dropped_modifiers()

    def draw_bricks(self):
        for brick in self.game_manager.bricks:
            # Create a brick with transparency based on durability
            surface = pygame.Surface((brick.width, brick.height))
            surface.fill(brick.color)
            surface.set_alpha(255 * ((brick.durability - brick.hits) / brick.durability))
            self.canvas.blit(surface, (brick.x, brick.y))

    def draw_paddle(self):
        pygame.draw.rect(self.canvas, "white", pygame.Rect(
            self.game_manager.paddle.x,
            self.game_manager.paddle.y,
            self.game_manager.paddle.width,
            self.game_manager.paddle.height
        ))

    def draw_balls(self):
        for ball in self.game_manager.balls:
            pygame.draw.circle(self.canvas, "white", ball.pos, ball.radius)

    def draw_dropped_modifiers(self):
        for modifier in self.game_manager.dropped_modifiers:
            pygame.draw.circle(self.canvas, modifier.color, (modifier.x, modifier.y), modifier.radius)

    def main(self):
 
        clock = pygame.time.Clock()
        pygame.init()
 
        # CREATE A self.canvas
        self.canvas = pygame.display.set_mode((self.window_size, self.window_size))

        # TITLE OF self.canvas
        pygame.display.set_caption("Breakout")
        pygame.display.set_icon(pygame.image.load('assets/apple_man.jpg'))
 
        # SETUP GAME OBJECTS
        self.setup()
 
        # GAME LOOP
        while not self.exit:
            if self.game_manager.lost_game:
                if not self.game_manager.name_entered:
                    self.handle_endgame()
                    continue
                self.display_endscreen()
                self.handle_events()
                continue
            
            self.game_manager.update()
            self.draw()
            self.handle_events()

            pygame.display.update()
            self.game_manager.dt = clock.tick(999) / 1000
            
            if self.game_manager.game_started:
                self.game_manager.tick += 1
                
    def get_highscores(self):
        with open(HIGHSCORES_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_highscores(self, highscores):
        with open(HIGHSCORES_PATH, 'w', encoding='utf-8') as f:
            json.dump(highscores, f, ensure_ascii=False, indent=4)

    # Runs every frame. What will happen each frame
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
 
        keys = pygame.key.get_pressed()
 
        self.react_to_user_input(keys)

    def handle_endgame(self):
        highscores = self.get_highscores()

        # Check if the score is a highscore.
        # If there are less than 5 highscores, or if the score is higher than the lowest highscore.
        is_highscore = len(highscores) < 5 or self.game_manager.total_points > min(highscores.values())

        # If the score is a highscore, ask for the player's name and add to highscores.
        if is_highscore:
            player_name = self.get_name()

            # If the player is not in the highscores, add them.
            # Otherwise, check if the score is higher than their previous score.
            if highscores.get(player_name) is None or self.game_manager.total_points > highscores[player_name]:
                highscores[player_name] = self.game_manager.total_points
                sorted_highscores = dict(sorted(highscores.items(), key=lambda i: i[1], reverse=True)[:5])
                self.save_highscores(sorted_highscores)
            
        self.game_manager.name_entered = True

    def display_endscreen(self):
        self.game_manager.sound_manager.stop_music()

        self.canvas.fill('black')
        font = pygame.font.Font('freesansbold.ttf', 30)
        small_font = pygame.font.Font('freesansbold.ttf', 15)

        text = font.render(f'Game Over. Score: {self.game_manager.total_points}', True, 'red')
        text_rect = text.get_rect()
        text_rect.center = (self.window_size / 2, self.window_size / 2)

        restart_text = small_font.render('Press Space to restart', True, 'white')
        restart_text_rect = restart_text.get_rect()
        restart_text_rect.center = (self.window_size / 2, self.window_size / 2 + 35)

        self.canvas.blit(text, text_rect)
        self.canvas.blit(restart_text, restart_text_rect)

        # Show highscores
        highscores = self.get_highscores()
        sorted_highscores = sorted(highscores.items(), key=lambda i: i[1], reverse=True)
        highscore_text = small_font.render('Highscores:', True, 'white')
        highscore_text_rect = highscore_text.get_rect()
        highscore_text_rect.center = (self.window_size / 2, self.window_size / 2 + 70)

        self.canvas.blit(highscore_text, highscore_text_rect)

        for i, (name, score) in enumerate(sorted_highscores):
            score_text = small_font.render(f'{i+1}. {name}: {score}', True, 'white')
            score_text_rect = score_text.get_rect()
            score_text_rect.center = (self.window_size / 2, self.window_size / 2 + 90 + i * 20)
            self.canvas.blit(score_text, score_text_rect)

        pygame.display.flip()
 
    def get_name(self):
        name = ''
        active = True
        font = pygame.font.Font('freesansbold.ttf', 20)

        while active:
            self.canvas.fill('black')
            prompt = font.render('New Highscore! Enter your name:', True, 'white')
            prompt_rect = prompt.get_rect()
            prompt_rect.center = (self.window_size / 2, self.window_size / 2 - 20)
            name_surface = font.render(name + '|', True, 'white')
            name_surface_rect = name_surface.get_rect()
            name_surface_rect.center = (self.window_size / 2, self.window_size / 2)
            self.canvas.blit(prompt, prompt_rect)
            self.canvas.blit(name_surface, name_surface_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(name) > 0:
                            active = False
                    else:
                        if len(name) < 10:
                            name += event.unicode
        return name

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