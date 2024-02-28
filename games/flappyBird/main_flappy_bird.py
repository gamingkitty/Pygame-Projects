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


def draw_text(screen, text, color, size, x, y, aligned="center"):
    font = pygame.font.Font("flappy.ttf", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if aligned == "center":
        text_rect.center = (x, y)
    elif aligned == "topleft":
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


def death_screen(screen, darken_surface, color, score):
    screen.blit(darken_surface, (0, 0))
    draw_text(screen, "Game Over!", color, 100, screen.get_width()/2, screen.get_height()/2.7)
    draw_text(screen, "Final Score: " + str(score), color, 80, screen.get_width()/2, screen.get_height()/1.8)


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
    dark_red = (183, 60, 47)

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
    add_pole_cooldown = 100
    add_pole_timer = 100
    pole_width = 127
    pole_height = 504

    bird_player = player.Player(["Sprites/flappy_bird_up.png", "Sprites/flappy_bird_middle.png",
                                 "Sprites/flappy_bird_down.png"], (68, 48), (400, 100))
    # For death screen
    darken_surface = pygame.Surface((screen_width, screen_height))
    darken_surface.set_alpha(128)
    darken_surface.fill((0, 0, 0))

    # Main Game Loop
    while True:
        print(bird_player.score )
        screen.blit(background_img, background_rect)
        delta_time = clock.tick(fps) / 1000
        if not bird_player.dead:
            ground_rect.centerx -= 300 * delta_time
        if -ground_rect.centerx >= screen_width:
            ground_rect.centerx = 0
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
                if not entity.point_given and entity.top_rect.x < bird_player.rect.centerx < entity.top_rect.x + pole_width:
                    bird_player.score += 1
                    entity.point_given = True
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
                y = random.randrange(-(pole_height//2), 0)
                entities.append(pole.Pole((screen_width, y), 250-2 * bird_player.score, False))
            else:
                add_pole_timer += 1
        # Load bird player last because it should be in front of poles
        bird_player.load(screen, delta_time, bird_player)
        # Print the score only if the player hasn't died
        if not bird_player.dead:
            draw_text(screen, str(bird_player.score), black, 100, screen_width/2, screen_height/6)
        # Handle key presses and other events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not bird_player.dead:
                    if event.key == pygame.K_SPACE:
                        bird_player.velocity_y = -400

        screen.blit(ground_img, ground_rect)

        if bird_player.dead:
            death_screen(screen, darken_surface, dark_red, bird_player.score)
        # Update the screen
        pygame.display.flip()


if __name__ == "__main__":
    main()