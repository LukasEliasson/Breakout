class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.hit_multiplier = self.current_level
        self.ball_speed = 300 + self.current_level * 50
        self.max_time = 120 * self.current_level

    def increase_level(self):
        self.current_level += 1
        self.hit_multiplier += 1
        self.ball_speed += 50
        self.max_time += 120
