# simulation.py

from collections import deque
import math
import random
from ship_environment import ShipEnvironment
from knowledge_base import KnowledgeBase
from bot import Bot
from rat import Rat
from rat_knowledge_base import RatKnowledgeBase


class Simulation:
    def __init__(self):
        self.env = ShipEnvironment(size=30)
        self.kb = KnowledgeBase(self.env)
        self.bot = Bot(self.env, self.kb)
        self.rat = Rat(self.env, self.bot.position)
        self.real_detection_probability = None
        self.step_counter = 0
        self.target_cells = []
        self.bfs_paths = []
        self.rat_kb = None

    def calculate_real_detection_probability(self, bot_position, rat_position, alpha):
        distance = abs(bot_position[0] - rat_position[0]) + abs(bot_position[1] - rat_position[1])
        return math.exp(-alpha * (distance - 1))

    def find_matching_probability_cell(self, rat_kb):
        matching_cells = []
        if self.real_detection_probability is None:
            return matching_cells

        for cell, probability in rat_kb.rat_detection_probabilities.items():
            #print(cell)
           # print(probability)
            if math.isclose(probability, self.real_detection_probability, rel_tol=1e-9):
                matching_cells.append(cell)
        return matching_cells


    def print_rat_probabilities_grid(self, rat_kb):
        # Create a grid to represent probabilities
        probabilities_matrix = [
            [
                f"{rat_kb.rat_detection_probabilities.get((r, c), 0):.2f}"
                if self.env.matrix[r][c] == 0 else "0.00"
                for c in range(self.env.size)
            ]
            for r in range(self.env.size)
        ]

        # Print the grid row by row
        print("Rat Probabilities Grid:")
        for row in probabilities_matrix:
            print(" ".join(row))

    def bfs_path(self, start, target):
        queue = deque([(start, [start])])
        visited = set([start])

        while queue:
            current, path = queue.popleft()

            if current == target:
                return path

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dr, current[1] + dc)

                if (0 <= neighbor[0] < self.env.size and 0 <= neighbor[1] < self.env.size
                    and self.env.matrix[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited):
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def run(self):
        sensed_directions = self.bot.sense_directions()
        self.kb.filter_positions(sensed_directions)
        print(f"Bot Location: {self.bot.position}")
        print(f"Rat Location: {self.rat.position}")
        bot_position = self.bot.position
        self.rat_kb = RatKnowledgeBase(self.env, bot_position, alpha=0.5)



        while True:
            move_success = self.bot.move()
            self.step_counter += 1 if move_success else 0

            if not move_success or len(self.kb.possible_positions) == 1:
                if len(self.kb.possible_positions) == 1:
                    bot_position = list(self.kb.possible_positions)[0]

                    rat_kb = RatKnowledgeBase(self.env, bot_position, alpha=0.5)
                    #self.print_rat_probabilities_grid(rat_kb)

                    self.target_cells = [cell for cell, _ in rat_kb.rat_detection_probabilities.items()]
                    #print(self.target_cells)


                    while len(self.target_cells) > 1:

                        self.real_detection_probability = self.calculate_real_detection_probability(
                            self.bot.position, self.rat.position, alpha=0.5
                        )
                        self.target_cells = self.find_matching_probability_cell(rat_kb)
                        rat_kb.filter_to_target_cells(self.target_cells)

                        self.bfs_paths.clear()
                        for target in self.target_cells:
                            path = self.bfs_path(self.bot.position, target)
                            if path:
                                self.bfs_paths.append(path)

                        if self.bfs_paths:
                            chosen_path = random.choice(self.bfs_paths)
                            self.bot.set_target_path(chosen_path, rat_kb)
                            self.bot.move_to_target()

                    if len(self.target_cells) == 1:
                        final_target = self.target_cells[0]
                        final_path = self.bfs_path(self.bot.position, final_target)
                        if final_path:
                            self.bot.set_target_path(final_path, rat_kb)

                    while self.bot.target_path:
                        self.bot.move_to_target()
                        self.step_counter += 1
                    break

        print(f"Final moves taken:{self.step_counter}")
        return self.get_training_data()

    def get_training_data(self):
      if not self.rat_kb:
          raise ValueError("RatKnowledgeBase is not initialized.")


      full_probabilities_grid = [
          [
              self.rat_kb.rat_detection_probabilities.get((r, c), 0)
              for c in range(self.env.size)
          ]
          for r in range(self.env.size)
      ]

      return self.kb.additional_matrix, full_probabilities_grid, self.step_counter

