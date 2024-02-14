import pygame
import math


class Scream(pygame.sprite.Sprite):
    def __init__(self, power, speed, pierce, size= (32, 32)):
        super(Scream, self).__init__()
        #stats
        self.power = power
        self.speed = speed
        self.pierce = pierce

        #misc
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.image.load("Sprites/screem.png")
        self.angle = 0
        self.damaged = []

    def load(self, SCREEN):
        rotated_image = pygame.transform.rotate(self.image, -int(self.angle * 180 / math.pi) + 180)
        image_rect = rotated_image.get_rect(center=self.rect.center)
        SCREEN.blit(rotated_image, image_rect)

    def move(self):
        self.rect.centerx += math.cos(self.angle) * self.speed
        self.rect.centery += math.sin(self.angle) * self.speed
