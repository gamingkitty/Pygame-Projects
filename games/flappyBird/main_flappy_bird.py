import pygame
import sys
import player
import random
import pole


def make_tiled_image(image, width, height):
    x_cursor = 0
    y_cursor = 0
    tiled_image = pygame.Surface((width, height))
    while y_cursor < height:
        while x_cursor < width:
            tiled_image.blit(image, (x_cursor, y_cursor))
            x_cursor += image.get_width()
        y_cursor += image.get_height()
        x_cursor = 0
    return tiled_image


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

    background_rect = pygame.Rect((0, 0), (screen_width, screen_height))
    background_img = pygame.image.load("Sprites/background.png")
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

    ground_rect = pygame.Rect((0, screen_height - 100), (screen_width, 75))
    ground_img = pygame.image.load("Sprites/ground.png")
    ground_img = make_tiled_image(ground_img, screen_width * 3, 100)

    clock = pygame.time.Clock()
    fps = 60

    entities = []
    paused = False

    # Helpers for poles
    add_pole_cooldown = 150
    add_pole_timer = 0
    pole_width = 127
    pole_height = 504

    bird_player = player.Player(["Sprites/flappy_bird_up.png", "Sprites/flappy_bird_middle.png",
                                 "Sprites/flappy_bird_down.png"], (68, 48), (400, 100))

    # Main Game Loop
    while True:
        screen.blit(background_img, background_rect)
        delta_time = clock.tick(fps) / 1000
        if not bird_player.dead:
            ground_rect.centerx -= 200 * delta_time
        if -ground_rect.centerx >= screen_width:
            ground_rect.centerx = 0
        bird_player.load(screen, delta_time, bird_player)
        # Handle entities
        remove_at = []
        index = 0
        for entity in entities:
            entity.load(screen, delta_time, bird_player)
            if entity.type == "pole":
                if entity.top_rect.centerx + pole_width < 0:
                   remove_at.append(index)
                if entity.has_collided(bird_player):
                    bird_player.dead = True
            index += 1
        num_removed = 0
        for index in remove_at:
            entities.pop(index - num_removed)
            num_removed += 1

        # Display poles
        # Add new poles and pole timer iteration
        if not bird_player.dead:
            if add_pole_timer >= add_pole_cooldown:
                add_pole_timer = 0
                y = random.randrange(-pole_height + 75, 0)
                entities.append(pole.Pole((screen_width, y), 250))
            else:
                add_pole_timer += 1
            # Handle key presses and other events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not bird_player.dead:
                    if event.key == pygame.K_SPACE:
                        bird_player.velocity_y = -400

        screen.blit(ground_img, ground_rect)
        # Update the screen
        pygame.display.flip()


if __name__ == "__main__":
    main()
