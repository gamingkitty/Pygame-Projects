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
    circle_radius = 10
    player_position = (screen_width / 2, screen_height/ 2)
    player_velocity = (0, 0)
    player_acceleration = (0, 0)
    is_w_held = False
    is_s_held = False
    is_a_held = False
    is_d_held = False

    # Main Game Loop
    while True:
        screen.fill(black)
        delta_time = clock.tick(fps) / 1000
        # Handle entities
        for entity in entities:
            entity.load(screen, delta_time, entities)

        # Enter your code here in the loop
        pygame.draw.circle(screen, white, player_position, circle_radius)

        player_velocity = (player_velocity[0] + player_acceleration[0] * delta_time,
                           player_velocity[1] + player_acceleration[1] * delta_time)
        player_position = (player_position[0] + player_velocity[0] * delta_time,
                           player_position[1] + player_velocity[1] * delta_time)

        player_velocity = (player_velocity[0] * delta_time * 58, player_velocity[1] * delta_time * 58)

        # Handle key presses and other events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    is_w_held = True
                    player_acceleration = (player_acceleration[0], player_acceleration[1] - 500)
                elif event.key == pygame.K_s:
                    is_s_held = True
                    player_acceleration = (player_acceleration[0], player_acceleration[1] + 500)
                elif event.key == pygame.K_a:
                    is_a_held = True
                    player_acceleration = (player_acceleration[0] - 500, player_acceleration[1])
                elif event.key == pygame.K_d:
                    is_d_held = True
                    player_acceleration = (player_acceleration[0] + 500, player_acceleration[1])
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    is_w_held = False
                    player_acceleration = (player_acceleration[0], player_acceleration[1] + 500)
                elif event.key == pygame.K_s:
                    is_s_held = False
                    player_acceleration = (player_acceleration[0], player_acceleration[1] - 500)
                elif event.key == pygame.K_a:
                    is_a_held = False
                    player_acceleration = (player_acceleration[0] + 500, player_acceleration[1])
                elif event.key == pygame.K_d:
                    is_d_held = False
                    player_acceleration = (player_acceleration[0] - 500, player_acceleration[1])

        # Update the screen
        pygame.display.flip()


if __name__ == "__main__":
    main()
