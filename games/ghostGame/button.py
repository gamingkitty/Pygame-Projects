import math
import sys
import pygame
import sprite_sheet


def draw_button_outline(surface, top_left, overlay, length, height, color, scale):
    scale = math.ceil(2 * scale)
    pygame.draw.rect(surface, color, (top_left[0] + 4 * scale, top_left[1], length - 8 * scale, scale))
    pygame.draw.rect(surface, color, (top_left[0] + 2 * scale, top_left[1] + scale, 2 * scale, scale))
    pygame.draw.rect(surface, color, (top_left[0] + length - 4 * scale, top_left[1] + scale, 2 * scale, scale))
    pygame.draw.rect(surface, color, (top_left[0] + scale, top_left[1] + 2 * scale, scale, 2 * scale))
    pygame.draw.rect(surface, color, (top_left[0] + length - 2 * scale, top_left[1] + 2 * scale, scale, 2 * scale)) # start
    pygame.draw.rect(surface, color, (top_left[0], top_left[1] + 4 * scale, scale, height - 8 * scale))
    pygame.draw.rect(surface, color, (top_left[0] + length - scale, top_left[1] + 4 * scale, scale, height - 8 * scale))
    pygame.draw.rect(surface, color, (top_left[0] + length - 2 * scale, top_left[1] + height - 4 * scale, scale, 2 * scale))
    pygame.draw.rect(surface, color, (top_left[0] + scale, top_left[1] + height - 4 * scale, scale, 2 * scale))
    pygame.draw.rect(surface, color, (top_left[0] + length - 4 * scale, top_left[1] + height - 2 * scale, 2 * scale, scale))
    pygame.draw.rect(surface, color, (top_left[0] + 2 * scale, top_left[1] + height - 2 * scale, 2 * scale, scale))
    pygame.draw.rect(surface, color, (top_left[0] + 4 * scale, top_left[1] + height - scale, length - 8 * scale, scale))
    surface.blit(overlay, top_left)


def make_button(text, font, padding, text_color, border_color, size, scale):
    padding = (padding + 1) * scale
    button_surface = pygame.surface.Surface((font.size(text)[0] + padding * 2, 3 * (font.size(text)[1] + padding * 2)), pygame.SRCALPHA)
    button_surface.blit(font.render(text, False, text_color), (padding, padding))
    button_surface.blit(font.render(text, False, text_color), (padding, padding * 3 + font.size(text)[1]))
    button_surface.blit(font.render(text, False, text_color), (padding, padding * 5 + 2 * font.size(text)[1]))

    overlay_color = (37, 37, 37)

    overlay = pygame.surface.Surface((button_surface.get_size()[0], button_surface.get_size()[1] // 3), pygame.SRCALPHA)
    overlay_scale = math.ceil(2 * scale)
    pygame.draw.rect(overlay, overlay_color, (4 * overlay_scale, 0, overlay.get_size()[0] - 8 * overlay_scale, overlay_scale))
    pygame.draw.rect(overlay, overlay_color, (2 * overlay_scale, overlay_scale, overlay.get_size()[0] - 4 * overlay_scale, overlay_scale))
    pygame.draw.rect(overlay, overlay_color, (overlay_scale, 2 * overlay_scale, overlay.get_size()[0] - 2 * overlay_scale, 2 * overlay_scale))
    pygame.draw.rect(overlay, overlay_color, (0, 4 * overlay_scale, overlay.get_size()[0], overlay.get_size()[1] - 8 * overlay_scale))
    pygame.draw.rect(overlay, overlay_color, (overlay_scale, overlay.get_size()[1] - 4 * overlay_scale, overlay.get_size()[0] - 2 * overlay_scale, 2 * overlay_scale))
    pygame.draw.rect(overlay, overlay_color, (2 * overlay_scale, overlay.get_size()[1] - 2 * overlay_scale, overlay.get_size()[0] - 4 * overlay_scale, overlay_scale))
    pygame.draw.rect(overlay, overlay_color, (4 * overlay_scale, overlay.get_size()[1] - overlay_scale, overlay.get_size()[0] - 8 * overlay_scale, overlay_scale))


    overlay.set_alpha(0)
    draw_button_outline(button_surface, (0, 0), overlay, button_surface.get_size()[0], overlay.get_height(), border_color, scale)
    overlay.set_alpha(50)
    draw_button_outline(button_surface, (0, overlay.get_height() + 1), overlay, button_surface.get_size()[0], overlay.get_height(), border_color, scale)
    overlay.set_alpha(77)
    draw_button_outline(button_surface, (0, 2 * overlay.get_height() + 1), overlay, button_surface.get_size()[0], overlay.get_height(), border_color, scale)
    button_surface = pygame.transform.scale(button_surface, (size[0], size[1] * 3))
    return sprite_sheet.SpriteSheet("", size, math.ceil(scale), 0, button_surface)


class Button:
    def __init__(self, scale, location, button_sheet, size, update_on_hover=False):
        self.scale = scale
        self.rect = pygame.Rect((0, 0), (scale * size[0], scale * size[1]))
        self.rect.center = location
        self.default_location = location
        self.original_size = size
        self.button_sheet = button_sheet
        self.button_sheet.set_current_frame(0)
        self.update_on_hover = update_on_hover
        self.clicked = False

    def load(self, screen):
        if self.update_on_hover:
            if self.clicked:
                self.button_sheet.set_current_frame(2)
            elif self.is_mouse_hovering():
                self.button_sheet.set_current_frame(1)
            else:
                self.button_sheet.set_current_frame(0)

        screen.blit(self.button_sheet.get_current_frame(), self.rect)

    def is_mouse_hovering(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
