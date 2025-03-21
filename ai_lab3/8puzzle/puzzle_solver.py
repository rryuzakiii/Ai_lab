import heapq
from copy import deepcopy
import random

# Goal state of the 8-puzzle
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Define possible moves (Up, Down, Left, Right)
MOVES = {
    'Up': (-1, 0),
    'Down': (1, 0),
    'Left': (0, -1),
    'Right': (0, 1)
}

def generate_random_puzzle():
    """
    Generate a random 8-puzzle initial state.
    """
    numbers = list(range(9))  # Numbers 0 to 8
    random.shuffle(numbers)
    puzzle = [numbers[i:i+3] for i in range(0, 9, 3)]
    return puzzle

def is_solvable(puzzle):
    """
    Check if the given puzzle is solvable by counting inversions.
    A puzzle is solvable if the number of inversions is even.
    """
    flat_puzzle = [tile for row in puzzle for tile in row if tile != 0]
    inversions = 0
    for i in range(len(flat_puzzle)):
        for j in range(i + 1, len(flat_puzzle)):
            if flat_puzzle[i] > flat_puzzle[j]:
                inversions += 1
    return inversions % 2 == 0

def manhattan_distance(puzzle):
    """
    Calculate the Manhattan Distance heuristic for a given puzzle.
    """
    distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != 0:  # Ignore the blank tile
                goal_row, goal_col = (puzzle[i][j] - 1) // 3, (puzzle[i][j] - 1) % 3
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance

def misplaced_tiles(puzzle):
    """
    Calculate the Misplaced Tiles heuristic for a given puzzle.
    """
    count = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != 0 and puzzle[i][j] != GOAL_STATE[i][j]:
                count += 1
    return count

def find_blank_position(puzzle):
    """
    Find the position of the blank tile (0) in the puzzle.
    """
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] == 0:
                return (i, j)
    return None

def expand_state(puzzle):
    """
    Generate all possible states from the current state by moving the blank tile.
    """
    blank_row, blank_col = find_blank_position(puzzle)
    possible_states = []
    
    for move, (dr, dc) in MOVES.items():
        new_row, new_col = blank_row + dr, blank_col + dc
        
        # Check if the move is valid
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            # Create a new state by swapping the blank tile with the target tile
            new_puzzle = deepcopy(puzzle)
            new_puzzle[blank_row][blank_col], new_puzzle[new_row][new_col] = new_puzzle[new_row][new_col], new_puzzle[blank_row][blank_col]
            possible_states.append((new_puzzle, move))
    
    return possible_states

def reconstruct_path(initial_puzzle, path):
    """
    Reconstruct the sequence of puzzle states from the initial state using the path of moves.
    """
    current_puzzle = deepcopy(initial_puzzle)
    state_sequence = [deepcopy(current_puzzle)]

    for move in path:
        blank_row, blank_col = find_blank_position(current_puzzle)
        dr, dc = MOVES[move]
        new_row, new_col = blank_row + dr, blank_col + dc
        current_puzzle[blank_row][blank_col], current_puzzle[new_row][new_col] = (
            current_puzzle[new_row][new_col],
            current_puzzle[blank_row][blank_col],
        )
        state_sequence.append(deepcopy(current_puzzle))

    return state_sequence

def a_star_search(initial_puzzle, heuristic):
    """
    Solve the 8-puzzle using A* search with the given heuristic.
    Returns the list of puzzle states leading to the solution.
    """
    open_list = []
    heapq.heappush(open_list, (heuristic(initial_puzzle), 0, initial_puzzle, []))  # (f(n), g(n), puzzle, path)
    closed_set = set()
    
    while open_list:
        _, g, current_puzzle, path = heapq.heappop(open_list)

        if current_puzzle == GOAL_STATE:
            return reconstruct_path(initial_puzzle, path)  # Return full state sequence
        
        puzzle_tuple = tuple(tuple(row) for row in current_puzzle)
        if puzzle_tuple in closed_set:
            continue
        
        closed_set.add(puzzle_tuple)
        
        for (new_puzzle, move) in expand_state(current_puzzle):
            new_puzzle_tuple = tuple(tuple(row) for row in new_puzzle)
            if new_puzzle_tuple not in closed_set:
                heapq.heappush(open_list, (g + 1 + heuristic(new_puzzle), g + 1, new_puzzle, path + [move]))
    
    return None  # No solution found

def greedy_best_first_search(initial_puzzle, heuristic):
    """
    Solve the 8-puzzle using Greedy Best-First Search.
    Returns the list of puzzle states leading to the solution.
    """
    open_list = []
    heapq.heappush(open_list, (heuristic(initial_puzzle), initial_puzzle, []))  # (h(n), puzzle, path)
    closed_set = set()
    
    while open_list:
        _, current_puzzle, path = heapq.heappop(open_list)

        if current_puzzle == GOAL_STATE:
            return reconstruct_path(initial_puzzle, path)  # Return full state sequence
        
        puzzle_tuple = tuple(tuple(row) for row in current_puzzle)
        if puzzle_tuple in closed_set:
            continue
        
        closed_set.add(puzzle_tuple)
        
        for (new_puzzle, move) in expand_state(current_puzzle):
            new_puzzle_tuple = tuple(tuple(row) for row in new_puzzle)
            if new_puzzle_tuple not in closed_set:
                heapq.heappush(open_list, (heuristic(new_puzzle), new_puzzle, path + [move]))
    
    return None  # No solution found
