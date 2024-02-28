import pygame
import math
import sys
import os


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


class Medpack(pygame.sprite.Sprite):
    def __init__(self, heal_amount, size=(32, 38)):
        #stats
        self.heal_amount = heal_amount

        #misc
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.image.load(resource_path("Sprites/medpack.png"))

    def load(self, SCREEN):
        SCREEN.blit(self.image, self.rect)

    def heal(self, character):
        character.hp += self.heal_amount
        if character.hp > character.max_hp:
            character.hp = character.max_hp
