import pygame


# Player class for flappy bird.
class Pole:
    def __init__(self, starting_position, size_between, point_given, size):
        # Rect: Position, size
        # The rectangle determines the position of the sprite and most everything. It also acts as a hit box.
        self.top_img = pygame.transform.scale(pygame.image.load("Sprites/pole_top.png"), size)
        self.bottom_img = pygame.transform.scale(pygame.image.load("Sprites/pole_bottom.png"), size)
        self.top_rect = pygame.Rect(starting_position, self.top_img.get_size())
        self.bottom_rect = pygame.Rect((starting_position[0], starting_position[1] + self.top_img.get_size()[1] + size_between),
                                       self.bottom_img.get_size())
        self.point_given = point_given
        self.type = "pole"

    # Loads the entity
    def load(self, screen, delta_time, bird_player):
        if not bird_player.dead:
            self.top_rect.centerx -= 300 * delta_time
            self.bottom_rect.centerx -= 300 * delta_time
        screen.blit(self.top_img, self.top_rect)
        screen.blit(self.bottom_img, self.bottom_rect)

    # Determines whether another entity is overlapping this entity
    def has_collided(self, other_entity):
        return self.top_rect.colliderect(other_entity.rect) or self.bottom_rect.colliderect(other_entity.rect)