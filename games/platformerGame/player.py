import pygame


class Player:
    def __init__(self, size, starting_position):
        self.rect = pygame.rect.Rect(starting_position, size)
        self.image = pygame

        self.velocity_y = 0
        self.velocity_x = 0

        self.acceleration_y = 0
        self.acceleration_x = 0

    def load(self):
        print("hi")
