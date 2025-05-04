from GameManager import GameManager
from Ball import Ball
from Brick import Brick
from Paddle import Paddle
import random

class Modifier:
    """
    Class representing a modifier that can be dropped by bricks when they are destroyed. These can have various effects on the game, such as changing the speed of the ball, changing the size of the paddle, or adding extra balls.

    Attributes:
        x (int): The x-coordinate of the modifier's position.
        y (int): The y-coordinate of the modifier's position.
        name (str): The name of the modifier.
        type (str): The type of the modifier (positive, negative, special).
        radius (int): The radius of the visible dropped modifier.
        color (str): The color of the visible dropped modifier. Randomly chosen from a list of colors.
        fall_speed (int): The speed at which the modifier falls.
        time_remaining (float): The time remaining for the modifier to be active.
        activated_at (int): The tick at which the modifier was activated.
        deactivated_at (int): The tick at which the modifier was deactivated.
        is_active (bool): Indicates if the modifier is currently active.
        brick (Brick): The brick that the modifier is associated with.
    """

    def __init__(self, name: str, type: str, ball_speed: int=5, paddle_size: int=50, time_remaining: float=None):
        self.x = 0
        self.y = 0
        self.name = name
        self.type = type
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

    """
    Sets the brick that the modifier is associated with.

    Parameters
    ----------
    brick : Brick
        The brick object that the modifier is associated with, i.e. the brick it will be dropped from.
    
    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the brick is not an instance of the Brick class.
    """
    def set_brick(self, brick: Brick) -> None:
        if not isinstance(brick, Brick):
            raise ValueError("Brick must be an instance of the Brick class")
    
        self.brick = brick

    """
    Moves the modifier to the position of the brick it is associated with.
    
    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the associated brick is not an instance of the Brick class.
    """
    def move_to_brick(self) -> None:
        if not isinstance(self.brick, Brick):
            raise ValueError("Associated brick must be an instance of the Brick class")

        self.x = self.brick.x + self.brick.width / 2
        self.y = self.brick.y + self.brick.height

    """
    Moves the modifier downwards by its fall speed.

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
    def fall(self) -> None:
        self.y += self.fall_speed

    """
    Checks if the modifier is caught by the paddle.

    Parameters
    ----------
    paddle : Paddle
        The paddle object to check for collision with.
    
    Returns
    -------
    bool
        Returns True if the modifier is caught by the paddle, False otherwise.
    
    Raises
    ------
    ValueError
        If the paddle is not an instance of the Paddle class.
    """
    def is_caught(self, paddle: Paddle) -> bool:
        if not isinstance(paddle, Paddle):
            raise ValueError("Paddle must be an instance of the Paddle class")

        # Check if the modifier is within the bounds of the paddle
        if (self.x + self.radius >= paddle.x and self.x - self.radius <= paddle.x + paddle.width and
                self.y + self.radius >= paddle.y and self.y - self.radius <= paddle.y + paddle.height):
            return True
        return False
    
    """
    Checks if the modifier is out of bounds.

    Parameters
    ----------
    window_size : int
        The size of the window to check against.

    Returns
    -------
    bool
        Returns True if the modifier is out of bounds, False otherwise.
    
    Raises
    ------
    ValueError
        If the window size is not greater than 0.
    """
    def is_out_of_bounds(self, window_size: int) -> bool:
        if not window_size > 0:
            raise ValueError("Window size must be greater than 0")

        # The modifier can only move downwards, so it is out of bounds if its lowest point is greater than the window size
        return (self.y - self.radius) > window_size
    
    """
    Sets the tick at which the modifier was activated.

    Parameters
    ----------
    time : int
        The tick at which the modifier was activated.
    
    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the time is not greater than 0.
    """
    def set_activated_time(self, time: int) -> None:
        if not time > 0:
            raise ValueError("Time must be greater than 0")
        
        self.activated_at = time

    """
    Sets the tick at which the modifier was deactivated.

    Parameters
    ----------
    time : int
        The tick at which the modifier was deactivated.
    
    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the time is not greater than 0.
    """
    def set_deactivated_time(self, time: int) -> None:
        if not time > 0:
            raise ValueError("Time must be greater than 0")

        self.deactivated_at = time 

    """
    Sets the duration attribute of the modifier. This is the time in seconds that the modifier will be active for. The duration is converted to milliseconds.

    Parameters
    ----------
    duration : int
        The duration of the modifier in seconds.
    
    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the duration is not greater than 0.
    """
    def set_duration(self, duration: int) -> None:
        if not duration > 0:
            raise ValueError("Duration must be greater than 0")

        # Convert duration to ms
        duration *= 1000

        self.duration = duration

    """
    Activates the modifier. This method is called when the modifier is caught by the paddle.
    Depending on the type of modifier, it will have different effects on the game.
    If the modifier has a time limit, it will be added to the game_manager's active modifiers list.

    Parameters
    ----------
    game_manager : GameManager
        The GameManager object that manages the game state and objects.
    
    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the game_manager is not an instance of the GameManager class.
    """
    def activate(self, game_manager: GameManager) -> None:

        # If game_manager is not an instance of GameManager, raise a ValueError
        if not isinstance(game_manager, GameManager):
            raise ValueError("game_manager must be an instance of the GameManager class")

        # If the modifier has a time limit, add it to the active modifiers list
        if self.time_remaining:
            game_manager.active_modifiers.append(self)
        
        # Remove the modifier from the dropped modifiers list
        game_manager.dropped_modifiers.remove(self)

        # Sets the time at which the modifier was activated
        self.set_activated_time(game_manager.tick)

        # Activate the modifier based on its name
        match self.name:
            case "Fast Ball":
                # Increase the speed of all balls by 150
                for ball in game_manager.balls:
                    ball.speed += 150
            case "Wide Paddle":
                # Increase the width of the paddle by 50
                # The base width is the width the paddle is supposed to be, and the actual width will be increased gradually until it reaches the base width
                game_manager.paddle.base_width += 50
            case "Extra Ball":
                # New balls will have the same speed as the first ball in the balls list.
                ball_speed = game_manager.balls[0].speed

                # Create new balls with different velocities
                game_manager.balls.append(Ball(self.x, self.y, 0, -1, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, 0.5, -0.5, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, -0.5, -0.5, 5, "white", speed=ball_speed))
            case "Extravaganza":
                # New balls will have the same speed as the first ball in the balls list.
                ball_speed = game_manager.balls[0].speed

                # Create new balls with different velocities
                game_manager.balls.append(Ball(self.x, self.y, 0, -1, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, 0.5, -0.5, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, -0.5, -0.5, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, -0.25, -0.75, 5, "white", speed=ball_speed))
                game_manager.balls.append(Ball(self.x, self.y, 0.25, -0.75, 5, "white", speed=ball_speed))

                # Increase the speed of all balls by 1000 and disable their death
                for ball in game_manager.balls:
                    ball.speed += 1000
                    ball.death_disabled = True
                
                # Set the time at which the modifier was activated
                self.set_activated_time(game_manager.tick)

                if not game_manager.sound_manager.extravaganza:
                    # Play the extravaganza music
                    game_manager.sound_manager.start_extravaganza()

            case "Extra Brick Row":
                # Move all bricks down 1 row (10 pixels)
                for brick in game_manager.bricks:
                    brick.y += 10

                # Create a new row of bricks at the top of the screen
                for i in range(0, game_manager.WINDOW_SIZE, 22):
                    game_manager.bricks.append(Brick(i, 20, "grey"))
                
                # Play the sound for a new row of bricks
                game_manager.sound_manager.play_new_row_sound()

        print(f'Activated modifier: {self.name}')

    """
    Deactivates the modifier. This method is called when the modifier's time limit is reached or when the game ends.
    Depending on the type of modifier, it will have different effects on the game.

    Parameters
    ----------
    game_manager : GameManager
        The GameManager object that manages the game state and objects.
    
    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the game_manager is not an instance of the GameManager class.
    """
    def deactivate(self, game_manager: GameManager) -> None:

        # If game_manager is not an instance of GameManager, raise a ValueError
        if not isinstance(game_manager, GameManager):
            raise ValueError("game_manager must be an instance of the GameManager class")

        # Decrease the modifier based on its name
        match self.name:
            case "Fast Ball":
                # Decrease the speed of all balls by 150, but not below 300 (the minimum speed)
                for ball in game_manager.balls:
                    if ball.speed >= 450:
                        ball.speed -= 150
            case "Wide Paddle":
                # Decrease the width of the paddle by 50
                # The base width is the width the paddle is supposed to be, and the actual width will be decreased gradually until it reaches the base width
                game_manager.paddle.base_width -= 50
            case "Extravaganza":
                # Count the number of active extravaganza modifiers
                extravaganza_count = 0
                for mod in game_manager.active_modifiers:
                    if mod.name == "Extravaganza":
                        extravaganza_count += 1

                # If there are no more active extravaganza modifiers, remove the death disabled from all balls and stop extravaganza music
                # Decrease the speed of all balls by 1000, but not below the lowest speed for the current amount of extravaganza modifiers (300 + 1000 * extravaganza_count)
                for ball in game_manager.balls:
                    if extravaganza_count <= 1:
                        ball.death_disabled = False
                        game_manager.sound_manager.stop_extravaganza()
                    
                    if ball.speed >= 300 + 1000 * extravaganza_count:
                        ball.speed -= 1000

        # If the modifier is in the active modifiers list, remove it
        if self in game_manager.active_modifiers:
            game_manager.active_modifiers.remove(self)

        print(f'Deactivated modifier: {self.name}')
