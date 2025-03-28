import pygame
import os
from nqueens_solver import hill_climbing

WINDOW_WIDTH = 1000 
WINDOW_HEIGHT = 1000 
STATUS_BAR_HEIGHT = 50  
FONT_SIZE = 24

# Colors
WHITE = (118, 150, 86)
BLACK = (238, 238, 210)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BACKGROUND_COLOR = (30, 30, 30)  

def load_queen_image(cell_size):
    """
    Load and scale the queen image to fit the cell size.
    """
    print("Current Working Directory:", os.getcwd())
    
    queen_image_path = os.path.join(os.getcwd(), "queen.png")
    print("Loading queen image from:", queen_image_path)
    
    try:
        queen_image = pygame.image.load(queen_image_path)
        queen_image = pygame.transform.scale(queen_image, (cell_size, cell_size))
        return queen_image
    except FileNotFoundError:
        print(f"Error: The file 'queen.png' was not found at {queen_image_path}.")
        print("Please ensure the file exists in the working directory.")
        exit(1)

def draw_chessboard(screen, n, state, queen_image, cell_size):
    """
    Draw the chessboard and place the queens.
    """
    for row in range(n):
        for col in range(n):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(
                screen,
                color,
                (
                    (WINDOW_WIDTH - n * cell_size) // 2 + col * cell_size,  # Center the chessboard horizontally
                    (WINDOW_HEIGHT - STATUS_BAR_HEIGHT - n * cell_size) // 2 + row * cell_size,  # Center the chessboard vertically (above the status bar)
                    cell_size,
                    cell_size,
                ),
            )
            if state[row] == col:
                screen.blit(
                    queen_image,
                    (
                        (WINDOW_WIDTH - n * cell_size) // 2 + col * cell_size,  # Center the queen horizontally
                        (WINDOW_HEIGHT - STATUS_BAR_HEIGHT - n * cell_size) // 2 + row * cell_size,  # Center the queen vertically (above the status bar)
                    ),
                )

def update_gui(screen, n, state, conflicts, queen_image, cell_size):
    """
    Update the GUI with the current state of the N-Queens problem.
    """
    screen.fill(BACKGROUND_COLOR)
    
    draw_chessboard(screen, n, state, queen_image, cell_size)
    
    font = pygame.font.SysFont("Arial", FONT_SIZE)
    status_text = font.render(f"Conflicts: {conflicts}", True, WHITE)
    screen.blit(status_text, (10, WINDOW_HEIGHT - STATUS_BAR_HEIGHT + 10))  # Position the status bar at the bottom
    
    pygame.display.flip()
    pygame.time.delay(200)  
def main():
    pygame.init()
    
    n = int(input("Enter the number of queens (N): "))
    
    cell_size = min(WINDOW_WIDTH // n, (WINDOW_HEIGHT - STATUS_BAR_HEIGHT) // n)
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("N-Queens Solver")
    
    queen_image = load_queen_image(cell_size)
    
    final_state, final_conflicts = hill_climbing(
        n,
        callback=lambda state, conflicts: update_gui(screen, n, state, conflicts, queen_image, cell_size),
    )
    
    if final_conflicts == 0:
        print("Solution Found!")
    else:
        print(f"No solution found. Best configuration with conflicts: {final_conflicts}")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()