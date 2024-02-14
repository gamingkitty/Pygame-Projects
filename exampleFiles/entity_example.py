import pygame


# This class is an example enemy class to show you how you might code an entity.
# You could use built in pygame sprite feature, but I find that complex and you don't really need it ever.
class Enemy:
    def __init__(self, sprite):
        # Rect: Position, size
        # The rectangle determines the position of the sprite and most everything. It also acts as a hitbox.
        self.rect = pygame.Rect((0, 0), (32, 32))
        self.health = 100
        self.attack = 10
        self.sprite = sprite
        self.type = "Enemy"

    # Loads the entity and updates everything. Delta time is useful for movement to stay consistent even with lag.
    def load(self, screen, delta_time, entities):
        screen.blit(self.sprite, self.rect)
        for entity in entities:
            if entity.type == "Player":
                entity.take_damage(self.attack)

    # Determines whether another entity is overlapping this entity
    def has_collided(self, other_entity):
        return self.rect.colliderect(other_entity.rect)

    # Deals damage to the entity
    def take_damage(self, damage):
        self.health -= damage
