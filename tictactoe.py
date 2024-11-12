import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen setup
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe")

# Colors
background_color = (28, 170, 156)
line_color = (23, 145, 135)
circle_color = (242, 235, 211)
cross_color = (84, 84, 84)

# Game variables
board = [[None, None, None], [None, None, None], [None, None, None]]
player = "X"
game_over = False
winning_line = None

# Grid settings
cell_size = 200
line_width = 15
circle_radius = 60
circle_width = 15
cross_width = 25
space = 55

# Font
font = pygame.font.Font(None, 72)

def draw_lines():
    # Vertical lines
    pygame.draw.line(screen, line_color, (cell_size, 0), (cell_size, height), line_width)
    pygame.draw.line(screen, line_color, (cell_size * 2, 0), (cell_size * 2, height), line_width)
    # Horizontal lines
    pygame.draw.line(screen, line_color, (0, cell_size), (width, cell_size), line_width)
    pygame.draw.line(screen, line_color, (0, cell_size * 2), (width, cell_size * 2), line_width)

def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col] == "O":
                pygame.draw.circle(screen, circle_color, (int(col * cell_size + cell_size / 2), int(row * cell_size + cell_size / 2)), circle_radius, circle_width)
            elif board[row][col] == "X":
                pygame.draw.line(screen, cross_color, (col * cell_size + space, row * cell_size + cell_size - space), (col * cell_size + cell_size - space, row * cell_size + space), cross_width)    
                pygame.draw.line(screen, cross_color, (col * cell_size + space, row * cell_size + space), (col * cell_size + cell_size - space, row * cell_size + cell_size - space), cross_width)

def check_winner():
    global game_over, winning_line
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            game_over = True
            winning_line = ("horizontal", row)
            return board[row][0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            game_over = True
            winning_line = ("vertical", col)
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        game_over = True
        winning_line = ("diagonal", "left")
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        game_over = True
        winning_line = ("diagonal", "right")
        return board[0][2]

    return None

def draw_winning_line():
    if winning_line is not None:
        if winning_line[0] == "horizontal":
            y = winning_line[1] * cell_size + cell_size / 2
            pygame.draw.line(screen, circle_color, (15, y), (width - 15, y), line_width)
        elif winning_line[0] == "vertical":
            x = winning_line[1] * cell_size + cell_size / 2
            pygame.draw.line(screen, circle_color, (x, 15), (x, height - 15), line_width)
        elif winning_line[0] == "diagonal":
            if winning_line[1] == "left":
                pygame.draw.line(screen, circle_color, (15, 15), (width - 15, height - 15), line_width)
            elif winning_line[1] == "right":
                pygame.draw.line(screen, circle_color, (15, height - 15), (width - 15, 15), line_width)

def restart_game():
    global board, player, game_over, winning_line
    board = [[None, None, None], [None, None, None]]
    player = "X"
    game_over = False
    winning_line = None

# Main game loop
while True:
    screen.fill(background_color)
    draw_lines()
    draw_figures()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]  # x-coordinate
            mouseY = event.pos[1]  # y-coordinate
            clicked_row = mouseY // cell_size
            clicked_col = mouseX // cell_size

            if board[clicked_row][clicked_col] is None:
                # Simulate a brief "vibration" delay
                time.sleep(0.1)  
                board[clicked_row][clicked_col] = player
                if check_winner() is None:
                    player = "O" if player == "X" else "X"
                else:
                    game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()

    if game_over:
        draw_winning_line()
        text = font.render(f"{check_winner()} wins!", True, circle_color)
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    pygame.display.update()