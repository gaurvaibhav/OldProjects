import pygame
import random
import os
import sys


pygame.init()
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLACK = (  0,   0,   0)

SNAKE_SIZE     = 30
INIT_VELOCITY  = 5
FPS            = 60

HISCORE_FILE = "hiscore.txt"

game_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake by Vaibhav")
clock = pygame.time.Clock()
font  = pygame.font.SysFont(None, 55)

def load_background(path):
    """Attempt to load and scale a background image; return None on failure."""
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
    except pygame.error:
        return None

bgimg = load_background("back.jpg")

def text_screen(text, color, x, y):
    """Render text onto the game window."""
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x, y])

def plot_snake(snk_list):
    """Draw the snake on the game window."""
    for x, y in snk_list:
        pygame.draw.rect(game_window, WHITE, [x, y, SNAKE_SIZE, SNAKE_SIZE])

def welcome():
    """Show welcome screen; wait for SPACE to start."""
    while True:
        game_window.fill((233, 210, 229))
        text_screen("Welcome to Snakes", BLACK, 260, 250)
        text_screen("Press Space Bar To Play", BLACK, 232, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return 

        pygame.display.update()
        clock.tick(FPS)

def gameloop():
    """Main game loop: handles gameplay until game over."""
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    score = 0

    if not os.path.exists(HISCORE_FILE):
        with open(HISCORE_FILE, "w") as f:
            f.write("0")
    with open(HISCORE_FILE, "r") as f:
        hiscore = int(f.read())

    food_x = random.randint(20, SCREEN_WIDTH // 2)
    food_y = random.randint(20, SCREEN_HEIGHT // 2)

    while not exit_game:
        if game_over:
            with open(HISCORE_FILE, "w") as f:
                f.write(str(hiscore))

            game_window.fill(BLACK)
            text_screen("Game Over! Press Enter To Continue", RED, 100, 250)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = INIT_VELOCITY
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -INIT_VELOCITY
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = -INIT_VELOCITY
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = INIT_VELOCITY
                        velocity_x = 0
                    elif event.key == pygame.K_q:
                        score += 10 

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 25 and abs(snake_y - food_y) < 25:
                score += 10
                snk_length += 5
                food_x = random.randint(20, SCREEN_WIDTH // 2)
                food_y = random.randint(20, SCREEN_HEIGHT // 2)
                if score > hiscore:
                    hiscore = score

            game_window.fill(WHITE)
            if bgimg:
                game_window.blit(bgimg, (0, 0))

            text_screen(f"Score: {score}  Hiscore: {hiscore}", RED, 5, 5)
            pygame.draw.rect(game_window, RED, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])

            head = [snake_x, snake_y]
            snk_list.append(head)
            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True

            if (snake_x < 0 or snake_x > SCREEN_WIDTH 
             or snake_y < 0 or snake_y > SCREEN_HEIGHT):
                game_over = True

            plot_snake(snk_list)
            pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    sys.exit()

def main():
    """Run welcome screen then game loop, repeat until exit."""
    while True:
        welcome()
        gameloop()

if __name__ == "__main__":
    main()
