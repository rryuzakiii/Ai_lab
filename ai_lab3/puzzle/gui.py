import pygame
from mazesolver import generate_maze, find_treasure

# Constants
CELL_SIZE = 40  # Size of each cell in pixels
BLOCK_DENSITY = 0.1  # Density of blocks in the maze
WINDOW_PADDING = 40  # Padding around the maze
STATUS_BAR_HEIGHT = 50  # Height of the status bar
TITLE_HEIGHT = 60  # Height of the title bar

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
GRADIENT_GREEN = (34, 139, 34)
GRADIENT_LIGHT_GREEN = (152, 251, 152)
GRADIENT_LIGHT_BLUE = (135, 206, 250)
BACKGROUND_COLOR = (30, 30, 30)  # Dark background

# Fonts
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)
TITLE_FONT = pygame.font.SysFont("Arial", 36, bold=True)

def draw_maze(screen, maze, path=None, visited=None):
    """
    Draw the maze on the screen with gradient colors and borders.
    """
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            x = j * CELL_SIZE + WINDOW_PADDING
            y = i * CELL_SIZE + TITLE_HEIGHT
            
            if maze[i][j] == 1:  # Block
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
            elif maze[i][j] == 't':  # Treasure
                pygame.draw.rect(screen, GOLD, (x, y, CELL_SIZE, CELL_SIZE))
            elif visited and (i, j) in visited:  # Visited cell
                # Gradient effect for visited cells
                color = (
                    min(GRADIENT_LIGHT_BLUE[0] + (i + j) % 20, 255),  # Ensure value <= 255
                    min(GRADIENT_LIGHT_BLUE[1] + (i + j) % 20, 255),
                    min(GRADIENT_LIGHT_BLUE[2] + (i + j) % 20, 255),
                )
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            else:  # Path
                pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
    
    # Draw the path if it exists
    if path:
        for idx, (r, c) in enumerate(path):
            x = c * CELL_SIZE + WINDOW_PADDING
            y = r * CELL_SIZE + TITLE_HEIGHT
            # Gradient effect for the path
            color = (
                min(GRADIENT_GREEN[0] + idx % 20, 255),  # Ensure value <= 255
                min(GRADIENT_GREEN[1] + idx % 20, 255),
                min(GRADIENT_GREEN[2] + idx % 20, 255),
            )
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

def update_gui(screen, maze, path, visited, path_cost, rows, cols):
    """
    Update the GUI with the current state of the maze.
    """
    screen.fill(BACKGROUND_COLOR)
    
    # Draw title
    title_text = TITLE_FONT.render("Maze Solver", True, WHITE)
    screen.blit(title_text, (WINDOW_PADDING, 10))
    
    # Draw maze
    draw_maze(screen, maze, path, visited)
    
    # Draw status bar
    status_text = FONT.render(f"Path Cost: {path_cost}", True, WHITE)
    screen.blit(status_text, (WINDOW_PADDING, rows * CELL_SIZE + TITLE_HEIGHT + 10))
    
    pygame.display.flip()
    pygame.time.delay(200)  # Pause for visualization

def main():
    # Initialize pygame
    pygame.init()
    
    # Ask the user for maze size
    rows = int(input("Enter the number of rows for the maze: "))
    cols = int(input("Enter the number of columns for the maze: "))
    
    # Calculate window size based on maze size
    WINDOW_WIDTH = cols * CELL_SIZE + 2 * WINDOW_PADDING
    WINDOW_HEIGHT = rows * CELL_SIZE + TITLE_HEIGHT + STATUS_BAR_HEIGHT
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Maze Solver")
    clock = pygame.time.Clock()
    
    # Generate the maze
    maze = generate_maze(rows, cols, BLOCK_DENSITY)
    
    # Find the path to the treasure
    path, path_cost = find_treasure(
        maze, 0, 0, callback=lambda maze, path, visited: update_gui(screen, maze, path, visited, len(path) - 1 if path else 0, rows, cols)
    )
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Draw the maze
        screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title_text = TITLE_FONT.render("Maze Solver", True, WHITE)
        screen.blit(title_text, (WINDOW_PADDING, 10))
        
        # Draw maze
        draw_maze(screen, maze, path)
        
        # Draw status bar
        status_text = FONT.render(f"Path Cost: {path_cost}", True, WHITE)
        screen.blit(status_text, (WINDOW_PADDING, rows * CELL_SIZE + TITLE_HEIGHT + 10))
        
        # Update the display
        pygame.display.flip()
        clock.tick(30)
    
    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    main()