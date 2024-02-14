import pygame
import sys
import player


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

    bird_player = player.Player("Sprites/flappy_bird.png", (34, 24), (100, 100))
    entities.append(bird_player)

    # Main Game Loop
    while True:
        screen.fill(black)
        delta_time = clock.tick(fps)/1000

        # Handle entities
        for entity in entities:
            entity.load(screen, delta_time, entities)

        # Handle key presses and other events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_player.velocity_y = -400

        # Update the screen
        pygame.display.flip()


if __name__ == "__main__":
    main()
