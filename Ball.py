import math
from pygame import Vector2
from Paddle import Paddle
from Brick import Brick

class Ball:
    """
    Class representing a ball in the game.
    
    Attributes
    ----------
    x : int
        The x-coordinate of the ball's position.
    y : int
        The y-coordinate of the ball's position.
    pos : Vector2
        The position of the ball as a pygame.Vector2 object.
    vx : int
        The x-component of the ball's velocity.
    vy : int
        The y-component of the ball's velocity.
    radius : int
        The radius of the ball.
    color : str
        The color of the ball.
    speed : int
        The speed of the ball.
    is_dead : bool
        Indicates if the ball is dead (i.e., has fallen off the screen).
    death_disabled : bool
        Indicates if the ball's death is disabled (will bounce off the bottom of the screen).
    
    Methods
    -------
    move(dt: float) -> None
        Moves the ball based on its velocity and speed.
    check_collision(paddle: Paddle, bricks: list[Brick], balls: list) -> Paddle | Brick | None
        Checks for collisions with the paddle, bricks, and other balls. Returns the object that was hit.
    bounce(direction: str) -> None
        Bounces the ball in the specified direction.
    handle_edge_bounce(game_manager: GameManager, window_size: int) -> None
        Handles the ball's bounce when it hits the edges of the window.
    paddle_hit(max_angle: int, paddle: Paddle) -> None
        Calculates and bounces the ball off the paddle based on the position of impact.
    begin() -> None
        Begins the ball's movement in the straight upward direction.
    """

    def __init__(self, x: int, y: int, vx: int, vy: int, radius: int, color: str, speed=300):
        self.x = x
        self.y = y
        self.pos = Vector2(self.x, self.y)
        self.vx = vx   # X-component of the ball's velocity
        self.vy = vy   # Y-component of the ball's velocity
        self.radius = radius
        self.color = color
        self.speed = speed
        self.is_dead = False   # Indicates if the ball is dead, which happens when it is out of bounds.
        self.death_disabled = False   # Indicates if the ball has death disabled (will bounce off the bottom of the screen)

    """
    Moves the ball based on its velocity and speed.

    Parameters
    ----------
    dt : float
        The time delta to move the ball in relation to.
    
    Returns
    -------
    None

    Raises
    ------
    ValueError
        If dt is less than 0.
    """
    def move(self, dt: float) -> None:
        if dt < 0:
            raise ValueError("dt must be greater than 0")

        self.x += self.speed * self.vx * dt
        self.y += self.speed * self.vy * dt
        self.pos = Vector2(self.x, self.y)

    """
    Checks for collisions with the paddle, bricks, and other balls. Returns the object that was hit.

    Parameters
    ----------
    paddle : Paddle
        The paddle object to check for collision with.
    bricks : list[Brick]
        The list of brick objects to check for collision with.
    balls : list[Ball]
        The list of ball objects to check for collision with.
    
    Returns
    -------
    Paddle | Brick | Ball | None
        Returns the paddle if a collision with it is detected, the brick if a collision with it is detected,
        the ball if a collision with it is detected, or None if no collision is detected.
        In other words, the object that was hit is returned.

    Raises
    ------
    None
    """
    def check_collision(self, paddle: Paddle, bricks: list[Brick], balls: list) -> Paddle | Brick | None:
        # If the ball collides with the paddle, return the paddle object
        if (self.x + self.radius >= paddle.x and self.x - self.radius <= paddle.x + paddle.width and
                self.y + self.radius >= paddle.y and self.y - self.radius <= paddle.y + paddle.height):
            return paddle
        
        # If the ball collides with a brick, return the brick object
        for brick in bricks:
            if (self.x + self.radius >= brick.x and self.x - self.radius <= brick.x + brick.width and
                    self.y + self.radius >= brick.y and self.y - self.radius <= brick.y + brick.height):
                return brick
        
        # If the ball collides with another ball, return the ball object
        # NOTE: Currently not being used. Ball to ball collisions are not implemented.
        for ball in balls:
            if ball != self and (self.x + self.radius >= ball.x - ball.radius and self.x - self.radius <= ball.x + ball.radius and
                    self.y + self.radius >= ball.y - ball.radius and self.y - self.radius <= ball.y + ball.radius):
                return ball
        
        # If no collision is found, return None.
        return None
    
    """
    Bounces the ball in the specified direction.

    Parameters
    ----------
    direction : str
        The direction to bounce the ball in. Can be "x", "y", or "xy".
    
    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the direction is not "x", "y", or "xy".
    """
    def bounce(self, direction: str) -> None:
        if direction == "y":
            # Invert vy
            self.vy = -self.vy
        elif direction == "x":
            # Invert vx
            self.vx = -self.vx
        elif direction == "xy":
            # Invert vx and vy
            self.vx = -self.vx
            self.vy = -self.vy
        else:
            raise ValueError("Invalid bounce direction. Use 'x', 'y', or 'xy'.")

    """
    Handles the ball's bounce when it hits the edges of the window.

    Parameters
    ----------
    game_manager : GameManager
        The GameManager object that manages the game state and objects.
    window_size : int
        The size of the window to check for edge collisions.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If window_size is less than or equal to 0.
    TypeError
        If window_size is not an integer.
    """
    def handle_edge_bounce(self, game_manager, window_size: int) -> None:
        if window_size <= 0:
            raise ValueError("window_size must be greater than 0")
        if not type(window_size) == int:
            raise TypeError("window_size must be an integer")

        # Define ball edge coordinates
        ball_left_edge = self.x - self.radius
        ball_right_edge = self.x + self.radius
        ball_top_edge = self.y - self.radius
        ball_bottom_edge = self.y + self.radius

        # Handle collisions with each edge of the screen.
        # Bounce the ball in the appropriate direction,
        # set the ball position to the edge (to avoid overshooting and getting stuck inside the edge), 
        # then play the wall hit sound.
        if (ball_left_edge <= 0) and (ball_top_edge <= 0):
            self.bounce('xy')
            self.x = self.radius
            self.y = self.radius
            game_manager.sound_manager.play_wall_hit_sound()
        elif (ball_right_edge >= window_size) and (ball_top_edge <= 0):
            self.bounce('xy')
            self.x = window_size - self.radius
            self.y = self.radius
            game_manager.sound_manager.play_wall_hit_sound()
        elif ball_left_edge <= 0:
            self.bounce('x')
            self.x = self.radius
            game_manager.sound_manager.play_wall_hit_sound()
        elif ball_right_edge >= window_size:
            self.bounce('x')
            self.x = window_size - self.radius
            game_manager.sound_manager.play_wall_hit_sound()
        elif ball_top_edge <= 0:
            self.bounce('y')
            self.y = self.radius
            game_manager.sound_manager.play_wall_hit_sound()
        elif ball_bottom_edge >= window_size and self.death_disabled:
            # Handle ball bouncing on the bottom edge if death is disabled.
            self.bounce('y')
            self.y = window_size - self.radius
            game_manager.sound_manager.play_wall_hit_sound()
        elif ball_top_edge >= window_size and not self.death_disabled:
            # If the ball escapes on the bottom of the screen and death is not disabled, set ball as dead.
            self.is_dead = True

        # Check if the ball has escaped the screen (should not happen anymore, bug got fixed)
        if ball_bottom_edge < 0 or ball_right_edge < 0 or ball_left_edge > window_size:
            # If so, move it to the center of the screen.
            self.x = window_size / 2
            self.y = window_size / 2

    """
    Calculates and bounces the ball off the paddle based on the position of impact.

    Parameters
    ----------
    max_angle : int
        The maximum angle of deflection from the paddle.
    paddle : Paddle
        The paddle object to check for collision with.
    
    Returns
    -------
    None

    Raises
    ------
    ValueError
        If max_angle is less than or equal to 0.
    TypeError
        If max_angle is not an integer.
    """
    def paddle_hit(self, max_angle: int, paddle: Paddle) -> None:
        if max_angle <= 0:
            raise ValueError("max_angle must be greater than 0")
        if not type(max_angle) == int:
            raise TypeError("max_angle must be an integer")

        # Find paddle midpoint x-coordinate
        paddle_midpoint = paddle.x + paddle.width / 2
        
        # Find collision point on the paddle.
        # -1 is far left edge. +1 is far right edge. 0 is middle.
        paddle_position = (self.x - paddle_midpoint) / (paddle.width / 2)

        # Calculate the bounce angle (in degrees)
        angle = 90 - max_angle * paddle_position

        # Convert to radians
        angle_rad = math.radians(angle)

        if angle == 0:
            # Set velocity straight upwards
            self.vx = 0
            self.vy = -self.speed
        else:
            # Calculate vx using cos and vy using sin
            self.vx = math.cos(angle_rad)
            self.vy = -math.sin(angle_rad)

    """
    Begins the ball's movement in the straight upward direction. This is typically called when the game starts.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    None
    """
    def begin(self) -> None:
        self.vx = 0
        self.vy = -1