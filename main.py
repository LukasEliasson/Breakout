import pygame
from Brick import Brick
from Paddle import Paddle
from Ball import Ball

def list_changed(list_1, list_2):
    if len(list_1) != len(list_2):
        return True

    for i in range(len(list_1)):
        if list_1[i] != list_2[i]:
            return True

    return False


class Main:
 
    def __init__(self):

        self.window_size = 500
        self.exit = False
        self.bricks = []
        self.paddle = Paddle(self.window_size / 2 - 25, self.window_size - 20)

        ball_radius = 5
        ball_starting_pos = {
            "x": self.window_size / 2,
            "y": self.paddle.y - ball_radius,
        }

        self.ball = Ball(ball_starting_pos["x"], ball_starting_pos["y"], 0, 0, 5, "white")
        self.player_pos = pygame.Vector2(ball_starting_pos["x"], ball_starting_pos["y"])
 
    # Will initialise the beginning of the game, create all essential objects etc.
    def setup(self, canvas: pygame.Surface, bricks: list[Brick]):
        for brick in bricks:
            pygame.draw.rect(canvas, "red", pygame.Rect(brick.x, brick.y, brick.width, brick.height))

        pygame.draw.rect(canvas, "white", pygame.Rect(self.paddle.x, self.paddle.y, self.paddle.width, self.paddle.height))
        pygame.draw.circle(canvas, "white", self.player_pos, self.ball.radius)


    def generate_bricks(self):
        for x in range(30, self.window_size - 30, 30):
            for y in range(30, 100, 10):
                self.bricks.append(Brick(x, y, "red"))


    def main(self):
 
        clock = pygame.time.Clock()
        pygame.init()
 
        # CREATE A CANVAS
        canvas = pygame.display.set_mode((self.window_size, self.window_size))
 
        # TITLE OF CANVAS
        pygame.display.set_caption("Breakout")
 
        # SETUP GAME OBJECTS
        self.generate_bricks()
        self.setup(canvas, self.bricks)
 
        # GAME LOOP
        while not self.exit:
            self.draw(canvas, self.bricks)
 
            self.handle_events()
 
            pygame.display.update()
            dt = clock.tick(30) / 1000
 
 
    # Runs every frame. What will happen each frame
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
 
        keys = pygame.key.get_pressed()
 
        self.react_to_user_input(keys)
 

    # Will redraw the screen each frame
    def draw(self, canvas: pygame.Surface, bricks: list[Brick]):
        canvas.fill((0, 0, 0))

        self.ball.move()
        self.player_pos.x = self.ball.x
        self.player_pos.y = self.ball.y
        collision = self.ball.check_collision(self.paddle, bricks)

        if collision:
            if isinstance(collision, Paddle):
                if self.ball.vy > 0 and self.ball.vx > 0:
                    self.ball.paddle_hit(45, (self.ball.x - self.paddle.x) / self.paddle.width)
                    self.ball.bounce("y")
                    
            elif isinstance(collision, Brick):
                self.ball.bounce("x")

        self.setup(canvas, bricks)

        pygame.display.flip()

 
    def react_to_user_input(self, keysPressed):
        if keysPressed[pygame.K_a] or keysPressed[pygame.K_LEFT]:
            pass

        if keysPressed[pygame.K_d] or keysPressed[pygame.K_RIGHT]:
            pass

        if keysPressed[pygame.K_w] or keysPressed[pygame.K_UP]:
            self.ball.begin()
 
 
 
main = Main()
 
main.main()