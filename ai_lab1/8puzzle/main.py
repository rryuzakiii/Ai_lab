from best_first_search import best_first_search
from puzzle import PuzzleSolver

if __name__ == "__main__":
    # Example Usage for Best-First Search
    grid = [
        [0, 2, 2],
        [0, 0, 0],
        [0, 0, 1]  # 1 is the goal
    ]
    start = (0, 0)
    goal = (2, 2)
    print("Goal Found:", best_first_search(grid, start, goal))

    # Example Usage for 8-Puzzle Solver
    initial_state = [1, 0, 2, 0, 0, 0, 0, 2, 0]  # 1 is goal, 0 is blank, 2 is wall
    goal_state = [0, 0, 2, 0, 1, 0, 0, 2, 0]
    puzzle_solver = PuzzleSolver(initial_state, goal_state)

    print("A* Cost:", puzzle_solver.a_star())
    print("GBFS Solvable:", puzzle_solver.greedy_best_first())
