from SoundManager import SoundManager
from LevelManager import LevelManager
from Brick import Brick
from Paddle import Paddle
from Ball import Ball
import random
from copy import deepcopy

class GameManager:
    """
    GameManager class to manage the game state, including the paddle, balls, bricks, and modifiers.
    It handles updates the game state and manages the game objects.

    Attributes
    ----------
    MAX_POINTS : int
        Maximum points for each level.
    MAX_BALL_SPEED : int
        Speed cap for the ball.
    WINDOW_SIZE : int
        Size of the game window.
    MODIFIER_DROP_RATE : float
        Chance to drop a modifier each time a brick is destroyed.
    dt : float
        Time delta for the game loop.
    modifiers : list[Modifier]
        List of modifiers to be used in the game.
    level_points : int
        Points for the current level.
    total_points : int
        Total points accumulated in the game.
    lives : int
        Number of lives left in the game.
    game_started : bool
        Flag to check if the game has started.
    won_game : bool
        Flag to check if the game has been won.
    lost_game : bool
        Flag to check if the game has been lost.
    dropped_modifiers : list[Modifier]
        List of dropped modifiers in the game.
    active_modifiers : list[Modifier]
        List of active modifiers in the game.
    death_disabled : bool
        Flag to check if the ball death is disabled (ball will bounce on bottom edge of the screen).
    elapsed_time : float
        Time elapsed since the game started.
    name_entered : bool
        Flag to check if the player has entered their name.
    sound_manager : SoundManager
        Sound manager to handle sound effects and music.
    level_manager : LevelManager
        Level manager to handle level state and progression.
    paddle : Paddle
        Paddle object for the player.
    balls : list[Ball]
        List of ball objects in the game.
    bricks : list[Brick]
        List of brick objects in the game.
    
    Methods
    -------
    update() -> None
        Update the game state, including ball positions, dropped modifiers, and active modifiers.
    update_balls() -> None
        Update the position of the balls and check for collisions with edges.
    update_dropped_modifiers() -> None
        Update the position of dropped modifiers and check for collisions with the paddle.
    update_active_modifiers() -> None
        Update the time remaining for active modifiers and deactivate them if time is up.
    update_paddle_width() -> None
        Update the paddle width based on the current width and base width.
    handle_ball_collisions() -> None
        Handle ball collisions with the paddle, bricks, and other balls.
    drop_random_modifier() -> None
        Drop a random modifier from the top of the screen.
    calculate_score() -> int
        Calculate the score based on elapsed time and maximum points.
    handle_brick_collision(ball: Ball, brick: Brick) -> None
        Handle the collision between a ball and a brick, including damage and dropping modifiers.
    drop_modifier_from_brick(brick: Brick) -> None
        Drop a modifier from a brick when it is destroyed.
    reset(new_level: bool = False, restart_game: bool = False) -> None
        Reset the game state and regenerate objects.
    reset_game_state() -> None
        Reset the game state, including resetting the level manager and level state.
    reset_level_state() -> None
        Reset the level state, including game started and name entered flag.
    lose_life() -> None
        Decrease the number of lives by 1 and check for game over.
    reset_all_modifiers() -> None
        Deactivate all active modifiers and clear the dropped modifiers list.
    generate_objects() -> tuple[Paddle, list[Ball]]
        Generate the paddle and balls for the game.
    generate_bricks() -> list[Brick]
        Generate the bricks for the game in a grid pattern.
    win() -> None
        Handle the win condition, including resetting the game state and increasing the level.
    lose() -> None
        Handle the lose condition, including resetting the game state and stopping the music.
    """

    def __init__(self, modifiers, WINDOW_SIZE):
        
        self.MAX_POINTS = 100000   # Maximum points for each level
        self.MAX_BALL_SPEED = 1500   # Speed cap for the ball
        self.WINDOW_SIZE = WINDOW_SIZE   # Size of the game window
        self.MODIFIER_DROP_RATE = 0.2  # 20% chance to drop a modifier each time a brick is destroyed

        if self.MODIFIER_DROP_RATE > 1 or self.MODIFIER_DROP_RATE < 0:
            raise ValueError("Modifier drop rate must be between 0 and 1")

        self.dt = 0.02   # Updated from the main loop. Set to 0.02 to avoid division by zero error when calculating FPS.
        self.modifiers = modifiers   # List of modifiers to be used in the game
        self.level_points = self.MAX_POINTS   # Points for the current level
        self.total_points = 0   # Total points accumulated in the game. Level points are added to this when the level is completed.
        self.lives = 3   # Number of lives left in the game
        self.game_started = False   # Flag to check if the game has started
        self.won_game = False   # Flag to check if the game has been won
        self.lost_game = False   # Flag to check if the game has been lost
        self.dropped_modifiers = []   # List of dropped modifiers in the game
        self.active_modifiers = []   # List of active modifiers in the game
        self.death_disabled = False   # Flag to check if the ball death is disabled (ball will bounce on bottom edge of the screen)
        self.elapsed_time = 0   # Time elapsed since the game started. Updated using dt in the update method.
        self.name_entered = False   # Flag to check if the player has entered their name

        # Initialise sound manager and level manager
        self.sound_manager = SoundManager()
        self.level_manager = LevelManager()
        
        # Initialise game objects
        self.paddle, self.balls = self.generate_objects()
        self.bricks = self.generate_bricks()

    """
    Update the game state, including ball positions, dropped modifiers, and active modifiers.
    Runs every frame in the main loop.

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
    def update(self) -> None:
        
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

    """
    Update the position of the balls in the balls list.
    Check for collisions with edges and remove dead balls from the game.

    If all balls are dead, reset the game.

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
    def update_balls(self) -> None:

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
                ball.handle_edge_bounce(self, self.WINDOW_SIZE)     

    """
    Update the position of dropped modifiers, check for collisions with the paddle, and check for out of bounds.

    If a modifier is caught by the paddle, activate it.

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
    def update_dropped_modifiers(self) -> None:
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

    """
    Update the time remaining for active modifiers and deactivate them if time is up.

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
    def update_active_modifiers(self) -> None:
        # A copy of self.active_modifiers is used (by adding [:] at the end) to avoid modifying the list while iterating over it
        for modifier in self.active_modifiers[:]:

            # Update the time remaining for the modifier
            modifier.time_remaining -= self.dt

            # If the time remaining of the modifier is less than or equal to 0, deactivate it
            if modifier.time_remaining <= 0:
                modifier.deactivate(self)

    """
    Check if the paddle width is shrinking or growing and update its width accordingly.

    The paddle width is updated based on the current width and base width.

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
    def update_paddle_width(self) -> None:
        # Base width is the width the paddle should shrink or grow to
        # Width is the current width of the paddle

        # If the paddle is shrinking, decrease its width and correct its position
        if self.paddle.width > self.paddle.base_width:
            self.paddle.width -= 60 * self.dt
            self.paddle.x += 30 * self.dt

            # Check if the paddle width has reached the base width. If so, set it to the base width to avoid overshooting.
            if self.paddle.width <= self.paddle.base_width:
                self.paddle.width = self.paddle.base_width
        
        # If the paddle is growing, increase its width and correct its position
        elif self.paddle.width < self.paddle.base_width:
            self.paddle.width += 60 * self.dt
            self.paddle.x -= 30 * self.dt

            # Check if the paddle width has reached the base width. If so, set it to the base width to avoid overshooting.
            if self.paddle.width >= self.paddle.base_width:
                self.paddle.width = self.paddle.base_width

    """
    Handle ball collisions with the paddle, bricks, and other balls.
    Check for collisions and handle them accordingly.

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
    def handle_ball_collisions(self) -> None:
        for ball in self.balls:

            # Get collision object for the ball (or none if no collision)
            collision_object = ball.check_collision(self.paddle, self.bricks, self.balls)

            # If there is a collision object, handle the collision
            if collision_object:

                # If the collision object is the paddle, handle paddle collision
                if isinstance(collision_object, Paddle):

                    # Handle paddle collision only if the ball is moving
                    # This is to avoid the ball bouncing off the paddle before the game starts
                    if ball.vy > 0 or ball.vx > 0:
                        ball.paddle_hit(45, self.paddle)

                        self.sound_manager.play_paddle_hit_sound()

                # If the collision object is a brick, handle brick collision
                elif isinstance(collision_object, Brick):
                    self.handle_brick_collision(ball, collision_object)

    """
    Drop a random modifier from the top of the screen.
    The modifier is randomly selected from the list of modifiers and its position is set to the top of the screen.
    The modifier is then added to the dropped_modifiers list.

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
    def drop_random_modifier(self) -> None:
        
        # Make a copy of a random modifier and set its position to the top of the screen
        modifier = deepcopy(random.choice(self.modifiers))
        modifier.x = random.randint(0 + modifier.radius * 2, self.WINDOW_SIZE - modifier.radius * 2)
        modifier.y = 0 + modifier.radius
        print(f'Dropped modifier: {modifier.name}')
        self.dropped_modifiers.append(modifier)

    """
    Calculate the current level score based on time spent on the level and maximum points.

    Parameters
    ----------
    None

    Returns
    -------
    score : int
        The calculated score for the current level.

    Raises
    ------
    None
    """
    def calculate_score(self) -> int:
        # Calculate level points based on elapsed time, maximum time, and maximum points
        # The score decreases as time elapsed increases
        score = round(self.MAX_POINTS * (1 - (self.level_manager.time_spent / self.level_manager.max_time)))
        return max(0, score)
    
    """
    Handle the collision between a ball and a brick.
    Damage the brick, play sound effect, and bounce the ball off the brick.

    If the brick is destroyed, remove it from the game and check for win condition.
    Randomly drop a modifier from the brick using the modifier drop rate.

    Parameters
    ----------
    ball : Ball
        The ball object that collided with the brick.
    brick : Brick
        The brick object that was hit by the ball.
    
    Returns
    -------
    None

    Raises
    ------
    ValueError
        If ball is not an instance of Ball or brick is not an instance of Brick.
    """
    def handle_brick_collision(self, ball: Ball, brick: Brick) -> None:

        if not isinstance(ball, Ball):
            raise ValueError("ball must be an instance of Ball")
        
        if not isinstance(brick, Brick):
            raise ValueError("brick must be an instance of Brick")

        # Damage the brick
        brick.damage()

        # Play sound effect for brick hit
        self.sound_manager.play_brick_hit_sound()

        # Bounce the ball off the brick in the vertical direction
        ball.bounce("y")

        # If the brick is destroyed, remove it from the game and check for win condition
        if brick.is_destroyed():
            self.bricks.remove(brick)

            if len(self.bricks) == 0:
                self.win()

            # Randomly drop a modifier from the brick using the modifier drop rate
            random_num = random.randint(1, round(1 / self.MODIFIER_DROP_RATE))

            if random_num == 1:
                self.drop_modifier_from_brick(brick)
    
    """
    Drop a modifier from a brick.
    The modifier is randomly selected from the list of modifiers and its position is set to the brick's position.
    The modifier is then added to the dropped_modifiers list.

    Parameters
    ----------
    brick : Brick
        The brick object that was destroyed.
    
    Returns
    -------
    None

    Raises
    ------
    ValueError
        If brick is not an instance of Brick.
    """
    def drop_modifier_from_brick(self, brick: Brick) -> None:
        if not isinstance(brick, Brick):
            raise ValueError("brick must be an instance of Brick")

        # Create a copy of a randomly chosen modifier
        modifier = deepcopy(random.choice(self.modifiers))

        # Drop the modifier from the brick if there are less than 5 dropped modifiers.
        if len(self.dropped_modifiers) < 5:
            modifier.set_brick(brick)
            modifier.move_to_brick()

            print(f'Dropped modifier: {modifier.name}')

            self.dropped_modifiers.append(modifier)

    """
    Reset the game state and regenerate objects.
    Depending on the parameters, it can reset the game state, level state, or handle losing a life.

    It also deactivates and removes all modifiers, regenerates the paddle and balls, and resets the game started flag.

    Parameters
    ----------
    new_level : bool, optional
        If True, reset the game state for a new level (default is False).
    restart_game : bool, optional
        If True, reset the game state for a new game (default is False).
    
    Returns
    -------
    None

    Raises
    ------
    None
    """
    def reset(self, new_level: bool = False, restart_game: bool = False) -> None:

        # Reset game state depending on if the game is restarting or a new level is starting
        if restart_game:
            self.reset_game_state()
        elif new_level:
            self.reset_level_state()
        else:
            self.lose_life()

        # Deactivate and remove all modifiers
        self.reset_all_modifiers()

        # Regenerate game elements
        self.paddle, self.balls = self.generate_objects()

        # Reset game started flag
        self.game_started = False

    """
    Reset the game state, including resetting the level manager and level state.
    Reset the total points, lives, and elapsed time.

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
    def reset_game_state(self) -> None:
        self.lost_game = False
        self.won_game = False
        self.lives = 3
        self.elapsed_time = 0
        self.level_manager.reset()
        self.total_points = 0

        # Reset the level state
        self.reset_level_state()

    """
    Reset the level state, including game started and name entered flag.
    Starts the music again.

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
    def reset_level_state(self) -> None:
        self.game_started = False
        self.name_entered = False

        # Regenerate bricks
        self.bricks = self.generate_bricks()

        # Start the music again
        self.sound_manager.start_music()

    """
    Decrease the number of lives by 1.

    If the player has no lives left, handle game over.

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
    def lose_life(self) -> None:
        # Decrease the number of lives by 1
        self.lives -= 1

        # If the player has no lives left, end the game
        if self.lives <= 0:
            self.lose()

    """
    Deactivate all active modifiers and clear the dropped modifiers list.
    This is called when the game is reset or when a new level starts.

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
    def reset_all_modifiers(self) -> None:
        # Deactivate all active modifiers.
        # A copy of self.active_modifiers is used (by adding [:] at the end) to avoid modifying the list while iterating over it
        for modifier in self.active_modifiers[:]:
            modifier.deactivate(self)
            
        # Clear the dropped modifiers list
        self.dropped_modifiers = []

    """
    Generate the paddle and a starting ball for the game.
    The paddle is created at the bottom center of the screen and the starting ball is created at the paddle's position.

    Parameters
    ----------
    None

    Returns
    -------
    paddle, balls : tuple[Paddle, list[Ball]]
        A tuple containing the paddle object and a list containing the starting ball object.
    
    Raises
    ------
    None
    """
    def generate_objects(self) -> tuple[Paddle, list[Ball]]:

        # Create a paddle object and set its initial position
        paddle = Paddle(self.WINDOW_SIZE / 2 - 25, self.WINDOW_SIZE - 20)

        # Set the ball radius and starting position
        ball_radius = 5
        ball_starting_pos = {
            "x": self.WINDOW_SIZE / 2,
            "y": paddle.y - ball_radius,
        }

        # Create a balls list with a ball object
        balls = [Ball(ball_starting_pos["x"], ball_starting_pos["y"], 0, 0, 5, "white", speed=self.level_manager.ball_speed)]

        return paddle, balls
    
    """
    Create the bricks for the game in a grid pattern.
    The bricks are created in a grid pattern with alternating colors and durability based on the level manager's hit multiplier.

    Parameters
    ----------
    None

    Returns
    -------
    bricks : list[Brick]
        A list of brick objects created in a grid pattern.

    Raises
    ------
    None
    """
    def generate_bricks(self) -> list[Brick]:
        bricks = []
        colors = ["red", "red", "orange", "orange", "green", "green", "yellow", "yellow"]

        # Create bricks in a grid pattern
        for x in range(0, self.WINDOW_SIZE, 22):
            for y in range(20, 91, 10):
                # Create a brick object with color based on its row
                color_index = int(y / 10 - 2)
                color = colors[color_index]

                # Durability is based on the level manager's hit multiplier
                durability = 1 * self.level_manager.hit_multiplier

                # Add the brick to the bricks list
                bricks.append(Brick(x, y, color, durability=durability))

        return bricks

    """
    Handle the win condition, including resetting the game state and increasing the level.
    The game state is reset, the level is increased, and the music is stopped. Level points are added to the total points.

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
    def win(self) -> None:
        # If the game is won, reset the game state and increase the level
        self.game_started = False
        self.won_game = True
        self.total_points += self.level_points
        self.level_manager.increase_level()

        # Stop the music
        self.sound_manager.stop_music()
        
        self.reset(new_level=True)

    """
    Handle the lose condition.
    The game started and lost game flags are set to False and True respectively.
    The music is stopped.

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
    def lose(self) -> None:
        # If the game is lost, set the game state to lost
        self.game_started = False
        self.lost_game = True

        # Stop the music
        self.sound_manager.stop_music()
