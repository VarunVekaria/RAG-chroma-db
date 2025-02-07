# rat.py

class Rat:
    def __init__(self, env, bot_position):
        self.env = env
        self.position = self.env.place_random_open_cell(avoid_cells=[bot_position])
