class Paddle:
    """
    Class representing the paddle in the game.

    Attributes
    ----------
    x : int
        The x-coordinate of the paddle's position.
    y : int
        The y-coordinate of the paddle's position.
    width : int
        The width of the paddle.
    base_width : int
        The width the paddle is supposed to be, and is transforming to.
    height : int
        The height of the paddle.
    color : str
        The color of the paddle.
    
    Methods
    -------
    move(direction: str, dt: int) -> None
        Moves the paddle in the specified direction.
        'left' and 'right' are the only valid directions.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.base_width = 50
        self.height = 10
        self.color = "white"

    def __str__(self):
        return "Paddle at x: " + str(self.x) + " y: " + str(self.y)
    
    def __repr__(self):
        return f'Paddle({self.x}, {self.y})'

    """
    Moves the paddle in the specified direction.

    Parameters
    ----------
    direction : str
        The direction to move the paddle in ('left' or 'right').
    dt : int
        The time delta to move the modifier in relation to.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the direction is not 'left' or 'right'.
    """
    def move(self, direction, dt: int) -> None:
        if direction == "left":
            self.x -= 300 * dt
        elif direction == "right":
            self.x += 300 * dt
        else:
            raise ValueError("Invalid direction. Expected 'left' or 'right'.")
