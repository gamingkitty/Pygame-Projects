import pygame
import sys


def main():
    # Colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (28, 128, 28)
    yellow = (230, 230, 0)
    brown = (118, 92, 72)
    gray = (175, 175, 175)
    dark_gray = (99, 102, 106)
    blue = (12, 246, 242)
    aqua = (5, 195, 221)
    red = (255, 0, 0)

    # Initialization of variables and pygame
    pygame.init()
    pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Game')

    screen_width = screen.get_width()
    screen_height = screen.get_height()

    clock = pygame.time.Clock()
    fps = 60

    entities = []
    paused = False

    # You can implement your own player, here there isn't any.
    player = None

    # Main Game Loop
    while True:
        screen.fill(black)
        delta_time = clock.tick(fps)/1000
        # Handle entities
        for entity in entities:
            entity.load(screen, delta_time, entities)

        #Enter your code here in the loop

        # Handle key presses and other events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Update the screen
        pygame.display.flip()


if __name__ == "__main__":
    main()
