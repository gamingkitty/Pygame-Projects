import pygame
import math


class Medpack(pygame.sprite.Sprite):
    def __init__(self, heal_amount, size=(32, 38)):
        #stats
        self.heal_amount = heal_amount

        #misc
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.image.load("Sprites/medpack.png")
        self.image = pygame.transform.scale(self.image, size)

    def load(self, SCREEN):
        SCREEN.blit(self.image, self.rect)

    def heal(self, character):
        character.hp += self.heal_amount
        if character.hp > character.max_hp:
            character.hp = character.max_hp
