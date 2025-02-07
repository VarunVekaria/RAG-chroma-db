# bot.py

import random

class Bot:
    def __init__(self, env, knowledge_base):
        self.env = env
        self.kb = knowledge_base
        self.position = random.choice(list(self.kb.possible_positions))
        self.history = []
        self.recent_positions = []
        self.target_path = []
        self.rat_kb = None

    def set_target_path(self, path, rat_kb):
        self.target_path = path
        self.rat_kb = rat_kb

    def move_to_target(self):
        if self.target_path and self.target_path[0] == self.position:
            self.target_path.pop(0)

        if self.target_path:
            next_position = self.target_path.pop(0)
            self.position = next_position
            self.history.append(self.position)
            if self.rat_kb:
                self.rat_kb.update_target_cells(self.position)

    def sense_directions(self):
        r, c = self.position
        return self.kb.get_open_neighbors(r, c)

    def move(self):
        probabilities = self.kb.calculate_direction_probabilities()
        if probabilities is None:
            return False

        directions_map = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        chosen_direction_index = random.choices(range(4), weights=probabilities, k=1)[0]
        dr, dc = directions_map[chosen_direction_index]
        new_position = (self.position[0] + dr, self.position[1] + dc)

        if (0 <= new_position[0] < self.env.size and
            0 <= new_position[1] < self.env.size and
            self.env.matrix[new_position[0]][new_position[1]] == 0):
            self.position = new_position
            self.history.append(self.position)
            self.update_recent_positions(new_position)
            self.kb.update_possible_positions(dr, dc)
            return True

        return False

    def update_recent_positions(self, new_position):
        self.recent_positions.append(new_position)
        if len(self.recent_positions) > 2:
            self.recent_positions.pop(0)
        if len(self.recent_positions) == 2 and self.recent_positions[0] == self.recent_positions[1]:
            self.kb.enforce_stricter_filtering(self.recent_positions[0])
