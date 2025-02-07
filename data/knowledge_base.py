# knowledge_base.py
import numpy as np
GRID_SIZE = 30 
class KnowledgeBase:
    def __init__(self, env):
        self.env = env
        self.open_cells_info = self.initialize_open_cells_info()
        self.possible_positions = set(self.open_cells_info.keys())
        self.additional_matrix = None
        self.count = 0

    def initialize_open_cells_info(self):
        open_cells_info = {}
        for r in range(1, self.env.size - 1):
            for c in range(1, self.env.size - 1):
                if self.env.matrix[r][c] == 0:
                    open_cells_info[(r, c)] = self.get_open_neighbors(r, c)
        return open_cells_info

    def get_open_neighbors(self, row, col):
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.env.size and 0 <= nc < self.env.size:
                neighbors.append(1 if self.env.matrix[nr][nc] == 0 else 0)
            else:
                neighbors.append(0)
        return tuple(neighbors)

    def filter_positions(self, sensed_directions):
        self.possible_positions = {
            pos for pos in self.possible_positions if self.open_cells_info[pos] == sensed_directions
        }

    def calculate_direction_probabilities(self):
        direction_counts = [0, 0, 0, 0]
        for pos in self.possible_positions:
            for i, open_state in enumerate(self.open_cells_info[pos]):
                direction_counts[i] += open_state

        total_open = sum(direction_counts)
        if total_open == 0:
            return None

        return [count / total_open for count in direction_counts]

    def update_possible_positions(self, dr, dc):

        new_possible_positions = set()
        for pos in self.possible_positions:
            new_pos = (pos[0] + dr, pos[1] + dc)
            if 0 <= new_pos[0] < self.env.size and 0 <= new_pos[1] < self.env.size:
                if self.env.matrix[new_pos[0]][new_pos[1]] == 0:
                    new_possible_positions.add(new_pos)
        self.possible_positions = new_possible_positions
        num_new_positions = len(self.possible_positions)
        # print(f"Number of new possible positions: {num_new_positions}")
        if self.count == 0 and num_new_positions < 5:
          self.count = 1
          self.additional_matrix = self.create_additional_matrix()
        # self.possible_positions = new_possible_positions


    def create_additional_matrix(self):
        # Create a 30x30 matrix based on specific criteria
        # For example, mark cells with few possible new positions
        additional_matrix = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.float32)
        for pos in self.possible_positions:
            # Example logic: mark cells with less connectivity
            # print("***")
            # print(pos)
            # print("***")
            additional_matrix[pos[0], pos[1]] = 1.0
        return additional_matrix

    def enforce_stricter_filtering(self, oscillating_position):
        if oscillating_position in self.possible_positions:
            self.possible_positions.remove(oscillating_position)


