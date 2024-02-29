import pygame
import button


def draw_text(text, color, size, x, y, SCREEN, aligned="center"):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if aligned == "center":
        text_rect.center = (x, y)
    elif aligned == "topleft":
        text_rect.topleft = (x, y)
    SCREEN.blit(text_surface, text_rect)


class ShopItem():
    def __init__(self, price, price_increase, display_text, text_color, font_size, background_color, size, location, upgrade_type, upgrade_amount, max_amount, screen_scaler):
        self.price = price
        self.price_increase = price_increase
        self.upgrade_type = upgrade_type
        self.upgrade_amount = upgrade_amount
        self.maxed = False
        self.max_amount = max_amount
        self.text_color = text_color
        self.background_color = background_color
        self.size = size
        self.original_size = size
        self.original_text = display_text
        self.location = location
        self.font_size = font_size

        self.screen_scaler = screen_scaler

        font = pygame.font.Font(None, font_size)
        item_image = pygame.Surface(size)
        item_image.fill(background_color)
        item_image.blit(font.render(display_text, True, text_color), item_image.get_rect())
        item_image = pygame.transform.scale(item_image, size)
        self.item_image = item_image
        self.button = button.Button(item_image, size, location)
        self.bought = 0

    def load(self, SCREEN):
        self.button.load(SCREEN)
        draw_text(str(self.bought), self.text_color, self.font_size, self.location[0] + 40 + self.size[0]/2, self.location[1], SCREEN)
        if not self.maxed:
            draw_text("(" + str(self.price) + ")", self.text_color, self.font_size, self.location[0] - 30 - self.size[0]/2, self.location[1], SCREEN)

    def buy(self, player):
        if self.upgrade_type == "hp":
            player.max_hp += self.upgrade_amount
            player.hp += self.upgrade_amount
        elif self.upgrade_type == "attack":
            player.attack_power += self.upgrade_amount
        elif self.upgrade_type == "speed":
            player.speed += self.upgrade_amount
        elif self.upgrade_type == "pierce":
            player.pierce += self.upgrade_amount
        elif self.upgrade_type == "attack_speed":
            player.scream_delay -= self.upgrade_amount
        elif self.upgrade_type == "max_bullets":
            player.max_bullets += self.upgrade_amount
        elif self.upgrade_type == "shield_unlock":
            player.has_shield = True

        player.upgrade_points -= self.price
        self.price += self.price_increase
        self.bought += 1

        if self.bought >= self.max_amount:
            self.size = (133, 40)
            self.set_text("Maxed")

            self.maxed = True

    def set_text(self, text):
        font = pygame.font.Font(None, int(self.font_size * self.screen_scaler))
        item_image = pygame.Surface(self.size)
        item_image.fill(self.background_color)
        item_image.blit(font.render(text, True, self.text_color), item_image.get_rect())
        self.button = button.Button(item_image, self.size, self.location)

