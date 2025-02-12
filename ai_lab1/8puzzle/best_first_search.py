# File: best_first_search.py
import heapq

def best_first_search(grid, start, goal):
    """Best-First Search to find the treasure using Manhattan distance."""
    def manhattan_distance(cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    visited = set()

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        if current == goal:
            return True  # Goal found

        if current in visited:
            continue

        visited.add(current)

        # Explore neighbors (up, down, left, right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0])
                    and neighbor not in visited and grid[neighbor[0]][neighbor[1]] != 2):
                heuristic = manhattan_distance(neighbor, goal)
                heapq.heappush(priority_queue, (heuristic, neighbor))

    return False 