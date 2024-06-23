from tkinter import Tk
import pygame
import random


import time

start_time = time.time()

# Measure elapsed time in seconds since the program started
elapsed_seconds = time.time()

pygame.init()



WHITE = (255, 255, 255)


root = Tk()
M_WIDTH = root.winfo_vrootwidth()
M_HEIGHT = root.winfo_screenheight()

M_WIDTH = M_WIDTH * (0.9)
M_HEIGHT = M_HEIGHT * (0.82)

CANDY_SIZE = 60


ROWS, COLUMNS = (round(M_HEIGHT/CANDY_SIZE) -1), round(M_WIDTH/CANDY_SIZE -1)

print(ROWS)
print(COLUMNS)

FPS = 60

screen = pygame.display.set_mode((M_WIDTH, M_HEIGHT))
pygame.display.set_caption("Candy Crush")

# Load candy images
candies = [
"Blue",
"Orange",
"Green",
"Yellow",
"Red",
"Purple",
"Green",
"Orange-Striped-Horizontal",
"Orange-Striped-Vertical",
"Orange-Wrapped",
"Orange",
"Purple-Striped-Horizontal",
"Purple-Striped-Vertical",
"Purple-Wrapped",
"Purple",
"Red-Striped-Horizontal",
"Red-Striped-Vertical",
"Red-Wrapped",
"Red",
"Yellow-Striped-Horizontal",
"Yellow-Striped-Vertical",
"Yellow-Wrapped",
"Yellow"]

images = {candy: pygame.image.load(f"./images/{candy}.png")
          for candy in candies}
blank_image = pygame.image.load("./images/blank.png")

background = pygame.image.load('./images/background.jpg').convert()


board = []

score2 = 0

clock = pygame.time.Clock()

# Variables to track mouse click and drag
dragging = False
drag_start = None
drag_end = None


def initialize_board():
    global board
    board = [[random.choice(candies) for _ in range(COLUMNS)]
             for _ in range(ROWS)]


def check_valid():
    for r in range(ROWS):
        for c in range(COLUMNS - 2):
            if board[r][c] == board[r][c + 1] == board[r][c + 2]:
                return True
    for c in range(COLUMNS):
        for r in range(ROWS - 2):
            if board[r][c] == board[r + 1][c] == board[r + 2][c]:
                return True
    return False


def crush_candy_IF_MATCHES():
    global score2

    for r in range(ROWS):
        for c in range(COLUMNS - 2):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] != "blank":
                board[r][c] = board[r][c + 1] = board[r][c + 2] = "blank"
                return True
    for c in range(COLUMNS):
        for r in range(ROWS - 2):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] != "blank":
                board[r][c] = board[r + 1][c] = board[r + 2][c] = "blank"
                return True
    return False

def slide_candy():
    for c in range(COLUMNS):
        ind = ROWS - 1
        for r in range(ROWS - 1, -1, -1):
            if board[r][c] != "blank":
                board[ind][c] = board[r][c]
                ind -= 1
        for r in range(ind, -1, -1):
            board[r][c] = "blank"


def generate_candy():
    for c in range(COLUMNS):
        if board[0][c] == "blank":
            board[0][c] = random.choice(candies)


def draw_board():
    for r in range(ROWS):
        for c in range(COLUMNS):
            candy = board[r][c]
            if candy != "blank":
                screen.blit(images[candy], (c * CANDY_SIZE, r * CANDY_SIZE))



def get_candy_at_pos(x, y):
    row = y // CANDY_SIZE
    col = x // CANDY_SIZE
    if row < ROWS and col < COLUMNS:
        return (row, col)
    return None


def handle_mouse_events(event):
    global dragging, drag_start, drag_end

    if event.type == pygame.MOUSEBUTTONDOWN:
        if not dragging:
            pos = pygame.mouse.get_pos()
            candy_pos = get_candy_at_pos(pos[0], pos[1])
            if candy_pos:
                drag_start = candy_pos
                dragging = True

    elif event.type == pygame.MOUSEBUTTONUP:
        if dragging:
            pos = pygame.mouse.get_pos()
            candy_pos = get_candy_at_pos(pos[0], pos[1])
            if candy_pos:
                drag_end = candy_pos
                swap_candies(drag_start, drag_end)
            dragging = False


def swap_candies(pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    if abs(r1 - r2) + abs(c1 - c2) == 1:  # Ensure candies are adjacent
        board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
        if not check_valid():
            # Invalid move, swap back
            board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]



def main():
    global score2

    initialize_board()

    score2 = 0
    
    running = True
    while running:

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score2}", True, (0, 0, 0))
        screen.blit(text, ((M_WIDTH / 2) - (text.get_width()/2), (M_HEIGHT) - text.get_height() - 10))  # Adjust position as needed


        draw_board()
        pygame.display.flip()

        screen.blit(background, (0, 0))

        slide_candy()
        generate_candy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                handle_mouse_events(event)


        clock.tick(FPS)
        
        # start of the timer game loads and adds score
        # that is what we do not want

        # so we let the game run for 3+ seconds for the game to run
        # then we allow adding scores

        if crush_candy_IF_MATCHES():
            if(time.time() - start_time) > 3:
                score2 += 10

    
    pygame.quit()

if __name__ == "__main__":
    main()
