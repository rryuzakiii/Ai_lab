import pygame
from puzzle_solver import (
    generate_random_puzzle,
    is_solvable,
    manhattan_distance,
    misplaced_tiles,
    a_star_search,
    greedy_best_first_search,
)

# Constants
CELL_SIZE = 150  # Adjusted cell size
WINDOW_WIDTH = 3 * CELL_SIZE
WINDOW_HEIGHT = 3 * CELL_SIZE + 200  # Extra space for dropdowns and buttons below the puzzle
FONT_SIZE = 24
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 40
DROPDOWN_WIDTH = 200
DROPDOWN_HEIGHT = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BACKGROUND_COLOR = (30, 30, 30)
DROPDOWN_COLOR = (100, 100, 100)

def draw_puzzle(screen, puzzle):
    """
    Draw the 8-puzzle on the screen.
    """
    for i in range(3):
        for j in range(3):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE), 2)
            if puzzle[i][j] != 0:
                font = pygame.font.SysFont("Arial", FONT_SIZE)
                text = font.render(str(puzzle[i][j]), True, WHITE)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

def draw_dropdown(screen, x, y, width, height, options, selected_option, is_open):
    """
    Draw a dropdown menu.
    """
    pygame.draw.rect(screen, DROPDOWN_COLOR, (x, y, width, height))
    font = pygame.font.SysFont("Arial", FONT_SIZE)
    text = font.render(selected_option, True, WHITE)
    screen.blit(text, (x + 10, y + 10))
    
    if is_open:
        for i, option in enumerate(options):
            option_rect = pygame.Rect(x, y + (i + 1) * height, width, height)
            pygame.draw.rect(screen, DROPDOWN_COLOR, option_rect)
            text = font.render(option, True, WHITE)
            screen.blit(text, (x + 10, y + (i + 1) * height + 10))

def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("8-Puzzle Solver")
    clock = pygame.time.Clock()

    # Initial state
    initial_puzzle = generate_random_puzzle()
    while not is_solvable(initial_puzzle):
        initial_puzzle = generate_random_puzzle()

    # Heuristic and algorithm options
    heuristic_options = ["Manhattan Distance", "Misplaced Tiles"]
    algorithm_options = ["A* Search", "Greedy Best-First Search"]

    # Selected options
    selected_heuristic = heuristic_options[0]
    selected_algorithm = algorithm_options[0]

    # Dropdown states
    heuristic_dropdown_open = False
    algorithm_dropdown_open = False

    # Solution tracking
    solution_steps = []
    current_step = 0
    solving = False
    current_puzzle = deepcopy(initial_puzzle)

    while True:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # Toggle heuristic dropdown
                if 10 <= x <= 10 + DROPDOWN_WIDTH and 3 * CELL_SIZE + 10 <= y <= 3 * CELL_SIZE + 10 + DROPDOWN_HEIGHT:
                    heuristic_dropdown_open = not heuristic_dropdown_open
                    algorithm_dropdown_open = False
                elif heuristic_dropdown_open:
                    for i, option in enumerate(heuristic_options):
                        if 3 * CELL_SIZE + 10 + (i + 1) * DROPDOWN_HEIGHT <= y <= 3 * CELL_SIZE + 10 + (i + 2) * DROPDOWN_HEIGHT:
                            selected_heuristic = option
                            heuristic_dropdown_open = False

                # Toggle algorithm dropdown
                elif 220 <= x <= 220 + DROPDOWN_WIDTH and 3 * CELL_SIZE + 10 <= y <= 3 * CELL_SIZE + 10 + DROPDOWN_HEIGHT:
                    algorithm_dropdown_open = not algorithm_dropdown_open
                    heuristic_dropdown_open = False
                elif algorithm_dropdown_open:
                    for i, option in enumerate(algorithm_options):
                        if 3 * CELL_SIZE + 10 + (i + 1) * DROPDOWN_HEIGHT <= y <= 3 * CELL_SIZE + 10 + (i + 2) * DROPDOWN_HEIGHT:
                            selected_algorithm = option
                            algorithm_dropdown_open = False

                # Solve button
                elif 10 <= x <= 10 + BUTTON_WIDTH and 3 * CELL_SIZE + 70 <= y <= 3 * CELL_SIZE + 70 + BUTTON_HEIGHT and not solving:
                    solving = True
                    heuristic_func = manhattan_distance if selected_heuristic == "Manhattan Distance" else misplaced_tiles
                    solution_steps = a_star_search(initial_puzzle, heuristic_func) if selected_algorithm == "A* Search" else greedy_best_first_search(initial_puzzle, heuristic_func)
                    current_step = 0
                    solving = False

        # Animate the solution step-by-step
        if solution_steps and current_step < len(solution_steps):
            current_puzzle = solution_steps[current_step]
            current_step += 1
            pygame.time.delay(500)

        # Draw the puzzle
        draw_puzzle(screen, current_puzzle)

        # Draw dropdowns
        draw_dropdown(screen, 10, 3 * CELL_SIZE + 10, DROPDOWN_WIDTH, DROPDOWN_HEIGHT, heuristic_options, selected_heuristic, heuristic_dropdown_open)
        draw_dropdown(screen, 220, 3 * CELL_SIZE + 10, DROPDOWN_WIDTH, DROPDOWN_HEIGHT, algorithm_options, selected_algorithm, algorithm_dropdown_open)

        # Draw solve button
        pygame.draw.rect(screen, GRAY, (10, 3 * CELL_SIZE + 70, BUTTON_WIDTH, BUTTON_HEIGHT))
        font = pygame.font.SysFont("Arial", FONT_SIZE)
        text = font.render("Solve", True, BLACK)
        screen.blit(text, (35, 3 * CELL_SIZE + 80))

        pygame.display.flip()
        clock.tick(30)
