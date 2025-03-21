import random

def generate_random_state(n):
    """
    Generate a random initial state for the N-Queens problem.
    Each queen is placed in a random column of its row.
    """
    return [random.randint(0, n-1) for _ in range(n)]

def calculate_conflicts(state):
    """
    Calculate the number of conflicts (attacks) in the current state.
    """
    n = len(state)
    conflicts = 0

    for i in range(n):
        for j in range(i + 1, n):
            # Check if queens are in the same column
            if state[i] == state[j]:
                conflicts += 1
            # Check if queens are on the same diagonal
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1

    return conflicts

def get_neighbors(state):
    """
    Generate all possible neighboring states by moving each queen to a different column in its row.
    """
    neighbors = []
    n = len(state)

    for i in range(n):
        for j in range(n):
            if j != state[i]:  # Avoid generating the same state
                neighbor = list(state)
                neighbor[i] = j
                neighbors.append(neighbor)

    return neighbors

def hill_climbing(n, callback=None):
    """
    Solve the N-Queens problem using the Hill Climbing Algorithm.
    
    :param n: Number of queens.
    :param callback: A callback function to update the GUI.
    :return: The final state and the number of conflicts.
    """
    current_state = generate_random_state(n)
    current_conflicts = calculate_conflicts(current_state)

    while True:
        # Generate all neighbors
        neighbors = get_neighbors(current_state)
        if not neighbors:
            break

        # Find the neighbor with the minimum conflicts
        best_neighbor = None
        best_conflicts = current_conflicts

        for neighbor in neighbors:
            neighbor_conflicts = calculate_conflicts(neighbor)
            if neighbor_conflicts < best_conflicts:
                best_neighbor = neighbor
                best_conflicts = neighbor_conflicts

        # If no better neighbor exists, stop
        if best_conflicts >= current_conflicts:
            break

        # Move to the best neighbor
        current_state = best_neighbor
        current_conflicts = best_conflicts

        # Update the GUI
        if callback:
            callback(current_state, current_conflicts)
    
    return current_state, current_conflicts