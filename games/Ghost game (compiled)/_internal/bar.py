import pygame


class Bar():
    def __init__(self, percent_full, size, location, color, background_color, border_percentx, border_percenty):
        self.percent_full = percent_full
        self.size = size
        self.bar_size = (size[0] * percent_full, size[1])
        self.location = location
        self.color = color
        self.background_color = background_color
        self.border_percentx = border_percentx
        self.border_percenty = border_percenty

        self.rect = pygame.Rect((0, 0), size)
        self.background_rect = pygame.Rect((0, 0), size)
        self.bar_rect = pygame.Rect((0, 0), self.bar_size)

        self.background_surface = pygame.Surface(size)
        self.surface = pygame.Surface(self.bar_size)

        self.rect.center = self.location
        self.background_rect.center = self.location

    def load(self, SCREEN):
        #draw bar background
        self.background_rect.center = self.location
        self.background_surface.fill(self.background_color)
        SCREEN.blit(self.background_surface, self.background_rect)

        #draw bar
        self.update_size()

        self.surface.fill(self.color, self.bar_rect)

        SCREEN.blit(self.surface, self.rect)

    def update_size(self):
        self.bar_size = (max(1, self.size[0] * self.percent_full), self.size[1])
        self.bar_rect = pygame.Rect((0, 0), self.bar_size)
        self.surface = pygame.Surface(
            (max(1, self.bar_size[0] * self.border_percentx), max(1, self.bar_size[1] * self.border_percenty)))
        self.rect.center = (self.location[0] + self.size[0] * (1 - self.border_percentx) / 2,
                            self.location[1] + self.size[1] * (1 - self.border_percenty) / 2)

    def update_bar(self):
        self.bar_rect = pygame.Rect((0, 0), self.bar_size)
        self.surface = pygame.Surface(
            (self.bar_size[0] * self.border_percentx, self.bar_size[1] * self.border_percenty))

    def set_percent_full(self, percent):
        self.percent_full = percent
