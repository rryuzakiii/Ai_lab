import random

def generate_maze(rows, cols, block_density=0.1):
    """
    Generate a maze grid with paths (0), blocks (1), and a treasure (t).
    
    :param rows: Number of rows in the grid.
    :param cols: Number of columns in the grid.
    :param block_density: Density of blocks (0.1 means 10% of cells are blocks).
    :return: A 2D list representing the maze.
    """
    # Initialize the grid with paths (0)
    maze = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Randomly place blocks (1) based on block_density
    for i in range(rows):
        for j in range(cols):
            if random.random() < block_density:
                maze[i][j] = 1
    
    # Randomly place the treasure (t)
    while True:
        treasure_row = random.randint(0, rows - 1)
        treasure_col = random.randint(0, cols - 1)
        if maze[treasure_row][treasure_col] == 0:  # Ensure treasure is placed on a path
            maze[treasure_row][treasure_col] = 't'
            break
    
    return maze

def print_maze(maze):
    """
    Print the maze in a readable format.
    
    :param maze: The maze grid to print.
    """
    for row in maze:
        print(" ".join(str(cell) for cell in row))

if __name__ == "__main__":
    rows = 10
    cols = 10
    block_density = 0.1  
    maze = generate_maze(rows, cols, block_density)
    print_maze(maze)

    import heapq

def manhattan_distance(x1, y1, x2, y2):
    """
    Calculate the Manhattan distance between two points (x1, y1) and (x2, y2).
    """
    return abs(x1 - x2) + abs(y1 - y2)

def find_treasure(maze, start_row=0, start_col=0):
    """
    Find the treasure in the maze using Best-First Search with Manhattan distance as the heuristic.
    
    :param maze: The maze grid.
    :param start_row: Starting row index.
    :param start_col: Starting column index.
    :return: The path to the treasure as a list of coordinates, or None if no path is found.
    """
    rows = len(maze)
    cols = len(maze[0])
    
    # Find the position of the treasure
    treasure_pos = None
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 't':
                treasure_pos = (i, j)
                break
        if treasure_pos:
            break
    
    if not treasure_pos:
        return None  
    
    treasure_row, treasure_col = treasure_pos
    
    heap = []
    heapq.heappush(heap, (manhattan_distance(start_row, start_col, treasure_row, treasure_col), start_row, start_col, [(start_row, start_col)]))
    
    # Visited cells to avoid revisiting
    visited = set()
    visited.add((start_row, start_col))
    
    # Directions for moving in the grid (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while heap:
        _, current_row, current_col, path = heapq.heappop(heap)
        
        # Check if the current cell is the treasure
        if maze[current_row][current_col] == 't':
            return path
        
        # Explore neighbors
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            
            # Check if the new cell is within bounds and not a block or visited
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if maze[new_row][new_col] != 1 and (new_row, new_col) not in visited:
                    visited.add((new_row, new_col))
                    heuristic = manhattan_distance(new_row, new_col, treasure_row, treasure_col)
                    heapq.heappush(heap, (heuristic, new_row, new_col, path + [(new_row, new_col)]))
    
    return None  # No path to the treasure

# Example usage
if __name__ == "__main__":
    # Generate a maze
    rows = 10
    cols = 10
    block_density = 0.1
    maze = generate_maze(rows, cols, block_density)
    print("Generated Maze:")
    print_maze(maze)
    
    # Find the treasure
    start_row, start_col = 0, 0  # Start from the top-left corner
    path = find_treasure(maze, start_row, start_col)
    
    if path:
        print("\nPath to the treasure:")
        for step in path:
            print(f"({step[0]}, {step[1]})")
    else:
        print("\nNo path to the treasure found.")

import heapq
import time

def manhattan_distance(x1, y1, x2, y2):
    """
    Calculate the Manhattan distance between two points (x1, y1) and (x2, y2).
    """
    return abs(x1 - x2) + abs(y1 - y2)

def find_treasure(maze, start_row=0, start_col=0, visualize=True):
    """
    Find the treasure in the maze using Best-First Search with Manhattan distance as the heuristic.
    
    :param maze: The maze grid.
    :param start_row: Starting row index.
    :param start_col: Starting column index.
    :param visualize: Whether to visualize the search process.
    :return: The path to the treasure as a list of coordinates, or None if no path is found.
    """
    rows = len(maze)
    cols = len(maze[0])
    
    # Find the position of the treasure
    treasure_pos = None
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 't':
                treasure_pos = (i, j)
                break
        if treasure_pos:
            break
    
    if not treasure_pos:
        return None  # No treasure in the maze
    
    treasure_row, treasure_col = treasure_pos
    
    # Priority queue for Best-First Search: (heuristic, row, col, path)
    heap = []
    heapq.heappush(heap, (manhattan_distance(start_row, start_col, treasure_row, treasure_col), start_row, start_col, [(start_row, start_col)]))
    
    # Visited cells to avoid revisiting
    visited = set()
    visited.add((start_row, start_col))
    
    # Directions for moving in the grid (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Create a copy of the maze for visualization
    if visualize:
        maze_copy = [row.copy() for row in maze]
    
    while heap:
        _, current_row, current_col, path = heapq.heappop(heap)
        
        # Check if the current cell is the treasure
        if maze[current_row][current_col] == 't':
            if visualize:
                # Mark the final path with *
                for (r, c) in path:
                    if maze_copy[r][c] != 't':  # Don't overwrite the treasure
                        maze_copy[r][c] = '*'
                print("Final Path:")
                print_maze(maze_copy)
            return path
        
        # Mark the current cell as visited
        if visualize and maze_copy[current_row][current_col] != 't':
            maze_copy[current_row][current_col] = '#'
            print(f"Step {len(path)}:")
            print_maze(maze_copy)
            time.sleep(1)  # Pause for visualization
        
        # Explore neighbors
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            
            # Check if the new cell is within bounds and not a block or visited
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if maze[new_row][new_col] != 1 and (new_row, new_col) not in visited:
                    visited.add((new_row, new_col))
                    heuristic = manhattan_distance(new_row, new_col, treasure_row, treasure_col)
                    heapq.heappush(heap, (heuristic, new_row, new_col, path + [(new_row, new_col)]))
    
    return None  # No path to the treasure

def print_maze(maze):
    """
    Print the maze in a readable format.
    
    :param maze: The maze grid to print.
    """
    for row in maze:
        print(" ".join(str(cell) for cell in row))
    print()

# Example usage
if __name__ == "__main__":
    # Generate a maze
    rows = 10
    cols = 10
    block_density = 0.1
    maze = generate_maze(rows, cols, block_density)
    print("Generated Maze:")
    print_maze(maze)
    
    # Find the treasure
    start_row, start_col = 0, 0  # Start from the top-left corner
    path = find_treasure(maze, start_row, start_col, visualize=True)
    
    if path:
        print("\nPath to the treasure:")
        for step in path:
            print(f"({step[0]}, {step[1]})")
    else:
        print("\nNo path to the treasure found.")