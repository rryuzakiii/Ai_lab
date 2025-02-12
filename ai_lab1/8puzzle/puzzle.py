import heapq

class PuzzleSolver:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def manhattan_distance(self, state):
        distance = 0
        for i in range(1, 3):  # Only 1 (goal) is considered
            if i in state:
                x1, y1 = divmod(state.index(i), 3)
                x2, y2 = divmod(self.goal_state.index(i), 3)
                distance += abs(x1 - x2) + abs(y1 - y2)
        return distance

    def expand_moves(self, state):
        neighbors = []
        blank_idx = state.index(0)
        x, y = divmod(blank_idx, 3)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                neighbor_idx = nx * 3 + ny
                if state[neighbor_idx] != 2:
                    new_state = state[:]
                    new_state[blank_idx], new_state[neighbor_idx] = new_state[neighbor_idx], new_state[blank_idx]
                    neighbors.append(new_state)

        return neighbors

    def a_star(self):
        """A* Search algorithm."""
        open_list = []
        heapq.heappush(open_list, (0, self.initial_state, 0))
        closed_list = set()

        while open_list:
            _, current_state, g = heapq.heappop(open_list)

            if current_state == self.goal_state:
                return g  # Return the cost

            if tuple(current_state) in closed_list:
                continue

            closed_list.add(tuple(current_state))

            for neighbor in self.expand_moves(current_state):
                if tuple(neighbor) not in closed_list:
                    h = self.manhattan_distance(neighbor)
                    heapq.heappush(open_list, (g + h, neighbor, g + 1))

        return -1  # No solution

    def greedy_best_first(self):
        """Greedy Best-First Search algorithm."""
        open_list = []
        heapq.heappush(open_list, (self.manhattan_distance(self.initial_state), self.initial_state))
        closed_list = set()

        while open_list:
            _, current_state = heapq.heappop(open_list)

            if current_state == self.goal_state:
                return True

            if tuple(current_state) in closed_list:
                continue

            closed_list.add(tuple(current_state))

            for neighbor in self.expand_moves(current_state):
                if tuple(neighbor) not in closed_list:
                    h = self.manhattan_distance(neighbor)
                    heapq.heappush(open_list, (h, neighbor))

        return False