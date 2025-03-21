import heapq
from copy import deepcopy

# Goal state of the 8-puzzle
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Define possible moves (Up, Down, Left, Right)
MOVES = {
    'Up': -3,
    'Down': 3,
    'Left': -1,
    'Right': 1
}

def is_solvable(state):
    """
    Check if the given state is solvable by counting inversions.
    A state is solvable if the number of inversions is even.
    """
    inversions = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] != 0 and state[j] != 0 and state[i] > state[j]:
                inversions += 1
    return inversions % 2 == 0

def manhattan_distance(state):
    """
    Calculate the Manhattan Distance heuristic for a given state.
    """
    distance = 0
    for i in range(len(state)):
        if state[i] != 0:  # Ignore the blank tile
            goal_index = GOAL_STATE.index(state[i])
            current_row, current_col = i // 3, i % 3
            goal_row, goal_col = goal_index // 3, goal_index % 3
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def misplaced_tiles(state):
    """
    Calculate the Misplaced Tiles heuristic for a given state.
    """
    count = 0
    for i in range(len(state)):
        if state[i] != 0 and state[i] != GOAL_STATE[i]:
            count += 1
    return count

def get_blank_index(state):
    """
    Find the index of the blank tile (0) in the state.
    """
    return state.index(0)

def expand_state(state):
    """
    Generate all possible states from the current state by moving the blank tile.
    """
    blank_index = get_blank_index(state)
    possible_states = []
    
    for move, delta in MOVES.items():
        new_index = blank_index + delta
        
        # Check if the move is valid
        if 0 <= new_index < len(state):
            # Ensure the move doesn't wrap around the grid
            if (move == 'Left' and new_index % 3 == 2) or (move == 'Right' and new_index % 3 == 0):
                continue
            
            # Create a new state by swapping the blank tile with the target tile
            new_state = deepcopy(state)
            new_state[blank_index], new_state[new_index] = new_state[new_index], new_state[blank_index]
            possible_states.append((new_state, move))
    
    return possible_states

def a_star_search(initial_state, heuristic):
    """
    Solve the 8-puzzle using A* search with the given heuristic.
    """
    open_list = []
    heapq.heappush(open_list, (heuristic(initial_state), 0, initial_state, []))  # (f(n), g(n), state, path)
    closed_set = set()
    
    while open_list:
        _, g, current_state, path = heapq.heappop(open_list)
        
        if current_state == GOAL_STATE:
            return path  # Return the path to the goal
        
        if tuple(current_state) in closed_set:
            continue
        
        closed_set.add(tuple(current_state))
        
        for (new_state, move) in expand_state(current_state):
            if tuple(new_state) not in closed_set:
                heapq.heappush(open_list, (g + 1 + heuristic(new_state)), g + 1, new_state, path + [move]))
    
    return None  # No solution found

def greedy_best_first_search(initial_state, heuristic):
    """
    Solve the 8-puzzle using Greedy Best-First Search with the given heuristic.
    """
    open_list = []
    heapq.heappush(open_list, (heuristic(initial_state), initial_state, []))  # (h(n), state, path)
    closed_set = set()
    
    while open_list:
        _, current_state, path = heapq.heappop(open_list)
        
        if current_state == GOAL_STATE:
            return path  # Return the path to the goal
        
        if tuple(current_state) in closed_set:
            continue
        
        closed_set.add(tuple(current_state))
        
        for (new_state, move) in expand_state(current_state):
            if tuple(new_state) not in closed_set:
                heapq.heappush(open_list, (heuristic(new_state)), new_state, path + [move]))
    
    return None  # No solution found

def print_state(state):
    """
    Print the 3x3 grid representation of the state.
    """
    for i in range(0, 9, 3):
        print(state[i:i+3])

# Example usage
if __name__ == "__main__":
    # Initial state of the puzzle
    initial_state = [1, 2, 3, 4, 0, 5, 7, 8, 6]
    
    # Check if the puzzle is solvable
    if not is_solvable(initial_state):
        print("The puzzle is not solvable.")
    else:
        print("Initial State:")
        print_state(initial_state)
        
        # Solve using A* with Manhattan Distance
        print("\nSolving using A* with Manhattan Distance...")
        path = a_star_search(initial_state, manhattan_distance)
        if path:
            print("Solution Path:", path)
        else:
            print("No solution found.")
        
        # Solve using Greedy Best-First Search with Misplaced Tiles
        print("\nSolving using Greedy Best-First Search with Misplaced Tiles...")
        path = greedy_best_first_search(initial_state, misplaced_tiles)
        if path:
            print("Solution Path:", path)
        else:
            print("No solution found.")