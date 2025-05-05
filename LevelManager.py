class LevelManager:
    """
    Manages the game levels, including level progression, ball speed, and time limits, etc.

    Attributes
    ----------
    current_level : int
        The current level number.
    hit_multiplier : int
        The multiplier applied to the durability of the bricks.
        Same as the current level number.
    ball_speed : int
        The initial speed of the balls.
        Starts at 300, increases by 50 for each level.
    max_time : int
        The maximum time allowed for the current level in seconds.
        Starts at 120, increases by 120 for each level.
    time_spent : int
        The time elapsed since the level started.

    Methods
    -------
    increase_level() -> None
        Increases the current level number and applies the hit multiplier.
    reset() -> None
        Reset the level manager to its initial state, i.e. level 1.
    """

    def __init__(self):
        self.current_level = 1
        self.hit_multiplier = self.current_level
        self.ball_speed = 300 + self.current_level * 50
        self.max_time = 120 * self.current_level
        self.time_spent = 0

    def increase_level(self) -> None:
        self.current_level += 1
        self.hit_multiplier += 1
        self.ball_speed += 50
        self.max_time += 120
        self.time_spent = 0

    def reset(self) -> None:
        self.current_level = 1
        self.hit_multiplier = self.current_level
        self.ball_speed = 300 + self.current_level * 50
        self.max_time = 120 * self.current_level
        self.time_spent = 0
