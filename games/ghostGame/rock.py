import pygame
import math


class Rock(pygame.sprite.Sprite):
    def __init__(self, attack_power, attack_speed, rock_time, size=(74, 74)):
        #stats
        self.attack_speed = attack_speed
        self.attack_power = attack_power
        self.rock_time = rock_time
        self.velocity_x = 0
        self.velocity_y = 0

        #misc
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.image.load("Sprites/Rock.png")
        self.image = pygame.transform.scale(self.image, size)

        #timers
        self.attack_cooldown = 0

    def load(self, SCREEN, paused):
        SCREEN.blit(self.image, self.rect)
        if not paused:
            self.rock_time -= 1
            self.rect.centerx += self.velocity_x
            self.rect.centery += self.velocity_y

            if -0.1 < self.velocity_y < 0.1:
                self.velocity_y = 0
            elif self.velocity_y > 0:
                self.velocity_y -= 0.05
            elif self.velocity_y < 0:
                self.velocity_y += 0.05

            if -0.1 < self.velocity_x < 0.1:
                self.velocity_x = 0
            elif self.velocity_x > 0:
                self.velocity_x -= 0.05
            elif self.velocity_x < 0:
                self.velocity_x += 0.05

    def attack(self, character):
        if self.is_overlapping(character) and self.attack_cooldown <= 0:
            character.take_damage(self.attack_power)
            self.attack_cooldown = self.attack_speed
        elif self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def is_overlapping(self, character):
        return self.rect.colliderect(character.rect)
