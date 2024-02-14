import pygame


# Player class for flappy bird.
class Player:
    def __init__(self, sprite, size, starting_position):
        # Rect: Position, size
        # The rectangle determines the position of the sprite and most everything. It also acts as a hit box.
        self.rect = pygame.Rect(starting_position, size)
        self.sprite = pygame.image.load(sprite)
        self.sprite = pygame.transform.scale(self.sprite, size)
        self.type = "Player"

        self.velocity_y = 0
        self.velocity_x = 0

        # Gravity
        self.acceleration_y = 650
        self.acceleration_x = 0

    # Loads the entity
    def load(self, screen, delta_time, entities):
        # If time between frames is high, then it should accelerate the same amount as if there were a lot of frames with
        # a short time in between. So we multiply by delta_time to ensure this is the case. (Basically riemann sum of acceleration
        # with respect to time to get velocity)
        self.velocity_y += self.acceleration_y * delta_time
        self.velocity_x += self.acceleration_x * delta_time

        # Similar situation with velocity.
        self.rect.centery += self.velocity_y * delta_time
        self.rect.centerx += self.velocity_x * delta_time
        if self.velocity_y > 100:
            screen.blit(pygame.transform.rotate(self.sprite, -20), self.rect)
        elif self.velocity_y < -100:
            screen.blit(pygame.transform.rotate(self.sprite, 20), self.rect)
        else:
            screen.blit(self.sprite, self.rect)

    # Determines whether another entity is overlapping this entity
    def has_collided(self, other_entity):
        return self.rect.colliderect(other_entity.rect)
