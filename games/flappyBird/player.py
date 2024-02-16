import pygame


# Player class for flappy bird.
class Player:
    def __init__(self, sprites, size, starting_position):
        # Rect: Position, size
        # The rectangle determines the position of the sprite and most everything. It also acts as a hit box.
        self.rect = pygame.Rect(starting_position, size)
        self.sprites = [pygame.transform.scale(pygame.image.load(sprite), size) for sprite in sprites]
        self.current_sprite = 0
        self.type = "Player"

        self.velocity_y = 0
        self.velocity_x = 0

        # Gravity
        self.acceleration_y = 1000
        self.acceleration_x = 0
        self.animation_cooldown = 5
        self.animation_timer = 0

        self.dead = False

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
        if self.rect.centery >= screen.get_height() - 100 - self.rect.size[0]/2:
            screen.blit(pygame.transform.rotate(self.sprites[1], -90), self.rect)
            self.rect.centery = screen.get_height() - 100 - self.rect.size[0]/2
            self.velocity_y = 0
            self.acceleration_y = 0
            self.dead = True
        elif self.velocity_y > 500:
            screen.blit(pygame.transform.rotate(self.sprites[self.current_sprite], max(-((self.velocity_y-500) ** 2)/1000, -90)), self.rect)
        else:
            screen.blit(pygame.transform.rotate(self.sprites[self.current_sprite], 20), self.rect)
        if not self.dead:
            if self.animation_timer >= self.animation_cooldown:
                self.current_sprite += 1
                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0
                self.animation_timer = 0
            else:
                self.animation_timer += 1

    # Determines whether another entity is overlapping this entity
    def has_collided(self, other_entity):
        return self.rect.colliderect(other_entity.rect)
