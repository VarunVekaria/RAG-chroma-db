# rat_knowledge_base.py

import math

class RatKnowledgeBase:
    def __init__(self, env, bot_position, alpha=0.5):
        self.env = env
        self.bot_position = bot_position
        self.alpha = alpha
        self.rat_detection_probabilities = self.calculate_detection_probabilities()

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def calculate_detection_probabilities(self):
        detection_probs = {}
        for r in range(1, self.env.size - 1):
            for c in range(1, self.env.size - 1):
                if self.env.matrix[r][c] == 0:
                    distance = self.manhattan_distance(self.bot_position, (r, c))
                    probability = math.exp(-(self.alpha * (distance - 1)))
                    detection_probs[(r, c)] = probability
        return detection_probs

    def filter_to_target_cells(self, target_cells):
        self.rat_detection_probabilities = {cell: prob for cell, prob in self.rat_detection_probabilities.items() if cell in target_cells}

    def update_target_cells(self, new_bot_position):
        updated_probs = {}
        for cell in self.rat_detection_probabilities:
            distance = self.manhattan_distance(new_bot_position, cell)
            probability = math.exp(-(self.alpha * (distance - 1)))
            updated_probs[cell] = probability
        self.rat_detection_probabilities = updated_probs
