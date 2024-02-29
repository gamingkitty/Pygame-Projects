import pygame


class Button():
    def __init__(self, image, size, location):
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = location
        self.image = image
        self.image = pygame.transform.scale(self.image, size)

    def load(self, SCREEN):
        SCREEN.blit(self.image, self.rect)

    def is_mouse_hovering(self):
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos)
