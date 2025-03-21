import heapq
import random
from copy import deepcopy
from collections import deque

# Goal state for 8-puzzle
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Movement directions
MOVES = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}

# Generate a random puzzle
def generate_random_puzzle():
    numbers = list(range(9))
    random.shuffle(numbers)
    return [numbers[i:i+3] for i in range(0, 9, 3)]

# Check if puzzle is solvable
def is_solvable(puzzle):
    flattened = [num for row in puzzle for num in row if num != 0]
    inversions = sum(1 for i in range(len(flattened)) for j in range(i + 1, len(flattened)) if flattened[i] > flattened[j])
    return inversions % 2 == 0

# Heuristic functions
def manhattan_distance(puzzle):
    return sum(abs(i - (puzzle[i][j] - 1) // 3) + abs(j - (puzzle[i][j] - 1) % 3) for i in range(3) for j in range(3) if puzzle[i][j] != 0)

def misplaced_tiles(puzzle):
    return sum(1 for i in range(3) for j in range(3) if puzzle[i][j] and puzzle[i][j] != GOAL_STATE[i][j])

# Find blank position
def find_blank_position(puzzle):
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == 0:
                return (i, j)

# Expand possible moves
def expand_state(puzzle):
    blank_x, blank_y = find_blank_position(puzzle)
    new_states = []
    for move, (dx, dy) in MOVES.items():
        new_x, new_y = blank_x + dx, blank_y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_puzzle = deepcopy(puzzle)
            new_puzzle[blank_x][blank_y], new_puzzle[new_x][new_y] = new_puzzle[new_x][new_y], new_puzzle[blank_x][blank_y]
            new_states.append((new_puzzle, move))
    return new_states

# Reconstruct solution path
def reconstruct_path(initial_puzzle, path):
    current_puzzle = deepcopy(initial_puzzle)
    sequence = [deepcopy(current_puzzle)]
    for move in path:
        blank_x, blank_y = find_blank_position(current_puzzle)
        dx, dy = MOVES[move]
        new_x, new_y = blank_x + dx, blank_y + dy
        current_puzzle[blank_x][blank_y], current_puzzle[new_x][new_y] = current_puzzle[new_x][new_y], current_puzzle[blank_x][blank_y]
        sequence.append(deepcopy(current_puzzle))
    return sequence, len(path)

# A* Search Algorithm
def a_star_search(puzzle, heuristic):
    open_list = [(heuristic(puzzle), 0, puzzle, [])]
    heapq.heapify(open_list)
    visited = set()

    while open_list:
        _, g, current_puzzle, path = heapq.heappop(open_list)
        if current_puzzle == GOAL_STATE:
            return reconstruct_path(puzzle, path)

        puzzle_tuple = tuple(map(tuple, current_puzzle))
        if puzzle_tuple in visited:
            continue
        visited.add(puzzle_tuple)

        for new_puzzle, move in expand_state(current_puzzle):
            heapq.heappush(open_list, (g + 1 + heuristic(new_puzzle), g + 1, new_puzzle, path + [move]))

    return None, 0

# Breadth-First Search (BFS)
def bfs(puzzle):
    queue = deque([(puzzle, [])])
    visited = set()

    while queue:
        current_puzzle, path = queue.popleft()
        if current_puzzle == GOAL_STATE:
            return reconstruct_path(puzzle, path)

        puzzle_tuple = tuple(map(tuple, current_puzzle))
        if puzzle_tuple in visited:
            continue
        visited.add(puzzle_tuple)

        for new_puzzle, move in expand_state(current_puzzle):
            queue.append((new_puzzle, path + [move]))

    return None, 0

# Depth-First Search (DFS)
def dfs(puzzle):
    stack = [(puzzle, [])]
    visited = set()

    while stack:
        current_puzzle, path = stack.pop()
        if current_puzzle == GOAL_STATE:
            return reconstruct_path(puzzle, path)

        puzzle_tuple = tuple(map(tuple, current_puzzle))
        if puzzle_tuple in visited:
            continue
        visited.add(puzzle_tuple)

        for new_puzzle, move in reversed(expand_state(current_puzzle)):
            stack.append((new_puzzle, path + [move]))

    return None, 0

# Print the puzzle state in a readable format
def print_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(str(tile) if tile != 0 else " " for tile in row))
    print("-" * 10)

# Menu to choose algorithm
def choose_algorithm():
    print("\nSelect Algorithm:")
    print("1. A* Search")
    print("2. Breadth-First Search (BFS)")
    print("3. Depth-First Search (DFS)")

    choice = input("Enter choice (1/2/3): ")
    if choice == "1":
        return "A*"
    elif choice == "2":
        return "BFS"
    elif choice == "3":
        return "DFS"
    else:
        print("Invalid choice, defaulting to A* Search.")
        return "A*"

# Menu to choose heuristic
def choose_heuristic():
    print("\nSelect Heuristic for A* Search:")
    print("1. Manhattan Distance")
    print("2. Misplaced Tiles")

    choice = input("Enter choice (1/2): ")
    if choice == "1":
        return manhattan_distance
    elif choice == "2":
        return misplaced_tiles
    else:
        print("Invalid choice, defaulting to Manhattan Distance.")
        return manhattan_distance

if __name__ == "__main__":
    initial_puzzle = generate_random_puzzle()

    # Ensure the puzzle is solvable
    while not is_solvable(initial_puzzle):
        initial_puzzle = generate_random_puzzle()

    print("\nInitial Puzzle State:")
    print_puzzle(initial_puzzle)

    algorithm = choose_algorithm()
    heuristic = None

    if algorithm == "A*":
        heuristic = choose_heuristic()
        solution_steps, path_cost = a_star_search(initial_puzzle, heuristic)
    elif algorithm == "BFS":
        solution_steps, path_cost = bfs(initial_puzzle)
    elif algorithm == "DFS":
        solution_steps, path_cost = dfs(initial_puzzle)

    # Print the solution
    if solution_steps:
        print("\nSolution Found!")
        for step_num, step in enumerate(solution_steps):
            print(f"Step {step_num}:")
            print_puzzle(step)

        print(f"Total Path Cost: {path_cost}")
    else:
        print("No solution found.")
